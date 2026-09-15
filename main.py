"""FastAPI backend for the code typing race: lobbies, chat and live progress."""
import asyncio
import json
import logging
import os
import random
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    File,
    Query,
    Request,
    Response,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

import db
import library
from library import (
    catalog,
    count_matching,
    pick_snippet,
    setting_int,
)
from snippets import (
    LANGUAGES,
    LEVEL_IDS,
    TOPIC_IDS,
    clean_ids,
    languages,
    levels,
    parse_ids,
    topics,
)

LANGUAGE_IDS = {lid for lid, _ in LANGUAGES}

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Load .env if present (uploaded through the panel's Files tab in production).
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:  # dotenv is optional; real env vars still win
    pass

log = logging.getLogger("coderace")


def env_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, "").strip() or default)
    except ValueError:
        return default


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "info").upper())
    await run_in_threadpool(db.setup)
    # Push the seed snippets and default settings, then read them back.
    await run_in_threadpool(library.seed)
    await run_in_threadpool(library.refresh, True)
    log.info("snippet library loaded from the %s", library.source())
    yield
    await run_in_threadpool(db.close)


app = FastAPI(
    title=os.environ.get("APP_TITLE", "Code Typing Race"),
    lifespan=lifespan,
)

LOBBY_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
MAX_RACE_SECONDS = 1800


def countdown_seconds() -> int:
    return max(0, min(30, setting_int("countdown_seconds", 5)))


def chat_limit() -> int:
    return max(1, setting_int("chat_history", 100))  # [:-0] would wipe the log


def playlist_size() -> int:
    return max(1, min(60, setting_int("playlist_size", 12)))


def default_race_seconds() -> int:
    return max(0, min(MAX_RACE_SECONDS, setting_int("race_seconds", 0)))


def clean_duration(value) -> int:
    """0 means classic: the race ends when the snippet is finished."""
    try:
        return max(0, min(MAX_RACE_SECONDS, int(float(value))))
    except (TypeError, ValueError):
        return 0

COOKIE_NAME = "cr_token"
COOKIE_MAX_AGE = 60 * 60 * 24 * 730  # two years


def new_code() -> str:
    while True:
        code = "".join(random.choice(LOBBY_CODE_ALPHABET) for _ in range(5))
        if code not in lobbies:
            return code


def client_ip(request) -> str:
    """Real client IP behind the panel's proxy."""
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:45]
    real = request.headers.get("x-real-ip", "").strip()
    if real:
        return real[:45]
    return (request.client.host if request.client else "")[:45]


def set_token_cookie(response: Response, token: str, secure: bool) -> None:
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=secure,
        path="/",
    )


async def current_user(request: Request) -> Optional[dict]:
    """The recognised player for this request, or None."""
    if not db.enabled():
        return None
    token = request.cookies.get(COOKIE_NAME, "")
    if not token:
        return None
    return await run_in_threadpool(db.find_by_token, token)


class Player:
    def __init__(self, pid: str, name: str, ws: WebSocket):
        self.id = pid
        self.name = name
        self.ws = ws
        self.uid: Optional[int] = None
        self.avatar = 0  # avatar version; 0 means no image
        self.ip = ""
        self.ready = False
        self.idx = 0  # index into the timed-mode playlist
        self.chars = 0  # correct characters typed across the whole race
        self.snips = 0  # snippets completed
        self.progress = 0.0
        self.wpm = 0.0
        self.acc = 100.0
        self.finished = False
        self.place: Optional[int] = None
        self.time: Optional[float] = None

    def reset(self) -> None:
        self.ready = False
        self.idx = 0
        self.chars = 0
        self.snips = 0
        self.progress = 0.0
        self.wpm = 0.0
        self.acc = 100.0
        self.finished = False
        self.place = None
        self.time = None

    def public(self) -> dict:
        return {
            "id": self.id,
            "uid": self.uid,
            "avatar": self.avatar,
            "name": self.name,
            "ready": self.ready,
            "idx": self.idx,
            "chars": self.chars,
            "snips": self.snips,
            "progress": round(self.progress, 4),
            "wpm": round(self.wpm, 1),
            "acc": round(self.acc, 1),
            "finished": self.finished,
            "place": self.place,
            "time": round(self.time, 2) if self.time is not None else None,
        }


class Lobby:
    def __init__(
        self,
        code: str,
        language: str = "python",
        levels_filter: Optional[List[str]] = None,
        topics_filter: Optional[List[str]] = None,
        duration: Optional[int] = None,
    ):
        self.code = code
        self.language = language if language in LANGUAGE_IDS else "python"
        self.levels: List[str] = clean_ids(levels_filter, LEVEL_IDS)
        self.topics: List[str] = clean_ids(topics_filter, TOPIC_IDS)
        # 0 = classic (one snippet), >0 = timed run through a playlist
        self.duration = clean_duration(
            default_race_seconds() if duration is None else duration
        )
        self.timer: Optional[asyncio.Task] = None
        self.ends_at: float = 0.0
        self.snip: dict = {}
        self.playlist: List[dict] = []
        self.reroll()  # fills snip + playlist to match the mode
        self.players: Dict[str, Player] = {}
        self.order: List[str] = []
        self.host: Optional[str] = None
        self.state = "waiting"  # waiting | countdown | racing | finished
        self.start_ts: float = 0.0
        self.task: Optional[asyncio.Task] = None
        self.chat: List[dict] = []
        self.finish_count = 0

    def roster(self) -> List[Player]:
        return [self.players[pid] for pid in self.order if pid in self.players]

    def reroll(self, avoid: str = "") -> None:
        """Pick what the next race will use: one snippet, or a whole playlist."""
        if self.duration > 0:
            self.playlist = library.playlist(
                self.language, playlist_size(), self.levels, self.topics
            )
            self.snip = self.playlist[0]
        else:
            self.snip = pick_snippet(self.language, avoid, self.levels, self.topics)
            self.playlist = [self.snip]

    def snapshot(self) -> dict:
        return {
            "t": "state",
            "code": self.code,
            "language": self.language,
            "levels": self.levels,
            "topics": self.topics,
            "state": self.state,
            "host": self.host,
            "snippet": self.snip["code"],
            "level": self.snip["level"],
            "topic": self.snip["topic"],
            "matches": count_matching(self.language, self.levels, self.topics),
            "duration": self.duration,
            "ends_at": self.ends_at,
            "playlist": [
                {"code": s["code"], "level": s["level"], "topic": s["topic"]}
                for s in self.playlist
            ],
            "start_ts": self.start_ts,
            "players": [p.public() for p in self.roster()],
        }

    async def broadcast(self, message: dict, skip: Optional[str] = None) -> None:
        payload = json.dumps(message)
        dead = []
        for pid, player in list(self.players.items()):
            if pid == skip:
                continue
            try:
                await player.ws.send_text(payload)
            except Exception:
                dead.append(pid)
        for pid in dead:
            self.players.pop(pid, None)

    async def push_state(self) -> None:
        await self.broadcast(self.snapshot())

    async def system(self, text: str) -> None:
        msg = {"t": "chat", "name": None, "text": text, "sys": True, "ts": time.time()}
        self.chat.append(msg)
        del self.chat[: -chat_limit()]
        await self.broadcast(msg)

    def cancel_task(self) -> None:
        if self.task and not self.task.done():
            self.task.cancel()
        self.task = None
        if self.timer and not self.timer.done():
            self.timer.cancel()
        self.timer = None
        self.ends_at = 0.0

    async def start_race(self) -> None:
        if self.state in ("countdown", "racing"):
            return
        self.reroll(avoid=self.snip["code"])
        for player in self.players.values():
            player.reset()
        self.finish_count = 0
        self.state = "countdown"
        await self.push_state()
        self.cancel_task()
        self.task = asyncio.create_task(self._countdown())

    async def _countdown(self) -> None:
        try:
            for n in range(countdown_seconds(), 0, -1):
                await self.broadcast({"t": "countdown", "n": n})
                await asyncio.sleep(1)
            self.state = "racing"
            self.start_ts = time.time()
            if self.duration > 0:
                self.ends_at = self.start_ts + self.duration
                self.timer = asyncio.create_task(self._clock())
            await self.broadcast(
                {"t": "go", "start_ts": self.start_ts, "ends_at": self.ends_at}
            )
            await self.push_state()
        except asyncio.CancelledError:
            pass

    async def _clock(self) -> None:
        """Timed mode: the server ends the race, so every racer stops together."""
        try:
            await asyncio.sleep(max(0.0, self.ends_at - time.time()))
            if self.state != "racing":
                return
            await self.finish_timed()
        except asyncio.CancelledError:
            pass

    async def finish_timed(self) -> None:
        """Rank by characters typed, then accuracy, and close the race."""
        racers = [p for p in self.roster()]
        ranked = sorted(racers, key=lambda p: (-p.chars, -p.acc))
        for i, player in enumerate(ranked, start=1):
            player.finished = True
            if player.place is None:
                player.place = i
            if player.time is None:
                player.time = float(self.duration)
        self.state = "finished"
        self.ends_at = 0.0
        await self.broadcast({"t": "time_up"})
        await self.push_state()
        for player in ranked:
            if player.uid and db.enabled():
                try:
                    await run_in_threadpool(
                        db.record_race,
                        player.uid,
                        self.language,
                        "mixed" if len(self.playlist) > 1 else self.snip["level"],
                        "mixed" if len(self.playlist) > 1 else self.snip["topic"],
                        player.wpm,
                        player.acc,
                        float(self.duration),
                        player.place,
                        self.code,
                        player.ip,
                    )
                except Exception as exc:
                    log.warning("could not record timed race: %s", exc)

    async def reset_to_lobby(self) -> None:
        self.cancel_task()
        self.state = "waiting"
        self.start_ts = 0.0
        self.finish_count = 0
        for player in self.players.values():
            player.reset()
        await self.push_state()

    async def maybe_finish(self) -> None:
        racers = self.roster()
        if self.state != "racing" or not racers:
            return
        if not all(p.finished for p in racers):
            return
        # Timed mode: everyone exhausted the playlist before the clock ran out.
        if self.duration > 0:
            self.cancel_task()
            await self.finish_timed()
            return
        self.state = "finished"
        await self.push_state()


lobbies: Dict[str, Lobby] = {}


# ---------- catalog ----------
@app.get("/api/languages")
async def api_languages():
    return languages()


@app.get("/api/meta")
async def api_meta():
    """Everything the picker needs: languages, levels, topics and counts."""
    return {
        "languages": languages(),
        "levels": levels(),
        "topics": topics(),
        "catalog": catalog(),
        "accounts": db.enabled(),
        "settings": library.settings(),
        "race_seconds": default_race_seconds(),
        "source": library.source(),
    }


@app.get("/api/snippet")
async def api_snippet(
    lang: str = "python",
    avoid: str = "",
    levels: str = "",
    topics: str = "",
):
    wanted_levels = parse_ids(levels, LEVEL_IDS)
    wanted_topics = parse_ids(topics, TOPIC_IDS)
    chosen = pick_snippet(lang, avoid, wanted_levels, wanted_topics)
    return {
        "language": lang,
        "snippet": chosen["code"],
        "level": chosen["level"],
        "topic": chosen["topic"],
        "matches": count_matching(lang, wanted_levels, wanted_topics),
    }


@app.get("/api/playlist")
async def api_playlist(
    lang: str = "python",
    size: int = 12,
    levels: str = "",
    topics: str = "",
):
    """An ordered run of snippets, for a timed solo session."""
    wanted_levels = parse_ids(levels, LEVEL_IDS)
    wanted_topics = parse_ids(topics, TOPIC_IDS)
    run = library.playlist(lang, size, wanted_levels, wanted_topics)
    return {
        "language": lang,
        "matches": count_matching(lang, wanted_levels, wanted_topics),
        "playlist": [
            {"code": s["code"], "level": s["level"], "topic": s["topic"]} for s in run
        ],
    }


@app.get("/api/config")
async def api_config():
    """Effective settings, and where the snippet library is being read from."""
    return {
        "settings": library.settings(),
        "source": library.source(),
        "snippets": sum(len(v) for v in library.all_snippets().values()),
        "stored_in_db": db.enabled(),
    }


# ---------- lobbies ----------
@app.get("/api/lobby/new")
async def api_new_lobby(
    lang: str = "python",
    levels: str = "",
    topics: str = "",
    duration: int = -1,
):
    code = new_code()
    lobbies[code] = Lobby(
        code,
        lang,
        parse_ids(levels, LEVEL_IDS),
        parse_ids(topics, TOPIC_IDS),
        None if duration < 0 else duration,
    )
    return {"code": code}


@app.get("/api/lobby/{code}")
async def api_lobby(code: str):
    lobby = lobbies.get(code.upper())
    if not lobby:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return lobby.snapshot()


# ---------- accounts ----------
@app.get("/api/me")
async def api_me(request: Request):
    if not db.enabled():
        return {"accounts": False, "user": None}
    row = await current_user(request)
    if row is None:
        return {"accounts": True, "user": None}
    await run_in_threadpool(db.seen, int(row["id"]), client_ip(request))
    return {"accounts": True, "user": db.public_user(row)}


@app.post("/api/register")
async def api_register(request: Request):
    if not db.enabled():
        return JSONResponse({"error": "accounts_disabled"}, status_code=503)

    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    name = db.clean_name(str(body.get("name", "")))
    if not name:
        return JSONResponse({"error": "name_required"}, status_code=400)

    ip = client_ip(request)
    existing = await current_user(request)
    if existing is not None:
        # Already recognised: treat a second register as a rename.
        await run_in_threadpool(db.rename, int(existing["id"]), name)
        await run_in_threadpool(db.seen, int(existing["id"]), ip)
        row = await run_in_threadpool(db.find_by_token, request.cookies[COOKIE_NAME])
        return {"user": db.public_user(row)}

    token, user = await run_in_threadpool(db.register, name, ip)
    response = JSONResponse({"user": user})
    set_token_cookie(response, token, request.url.scheme == "https")
    return response


@app.post("/api/profile")
async def api_profile(request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    name = db.clean_name(str(body.get("name", "")))
    if not name:
        return JSONResponse({"error": "name_required"}, status_code=400)
    await run_in_threadpool(db.rename, int(user["id"]), name)
    row = await run_in_threadpool(db.find_by_token, request.cookies[COOKIE_NAME])
    return {"user": db.public_user(row)}


@app.post("/api/avatar")
async def api_set_avatar(request: Request, file: UploadFile = File(...)):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)

    data = await file.read(db.AVATAR_MAX_BYTES + 1)
    if not data:
        return JSONResponse({"error": "empty_file"}, status_code=400)
    if len(data) > db.AVATAR_MAX_BYTES:
        return JSONResponse({"error": "too_large", "max": db.AVATAR_MAX_BYTES}, status_code=413)

    mime = db.sniff_avatar(data)
    if mime is None:
        return JSONResponse({"error": "unsupported_type"}, status_code=415)

    version = await run_in_threadpool(db.set_avatar, int(user["id"]), data, mime)
    return {"avatar_version": version}


@app.delete("/api/avatar")
async def api_clear_avatar(request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    await run_in_threadpool(db.clear_avatar, int(user["id"]))
    return {"ok": True}


@app.get("/api/avatar/{user_id}")
async def api_get_avatar(user_id: int):
    if not db.enabled():
        return JSONResponse({"error": "accounts_disabled"}, status_code=404)
    found = await run_in_threadpool(db.get_avatar, user_id)
    if found is None:
        return JSONResponse({"error": "no_avatar"}, status_code=404)
    data, mime = found
    return Response(
        content=data,
        media_type=mime,
        headers={"Cache-Control": "public, max-age=604800"},
    )


@app.get("/api/leaderboard")
async def api_leaderboard(limit: int = 10):
    if not db.enabled():
        return {"rows": []}
    return {"rows": await run_in_threadpool(db.leaderboard, limit)}


@app.post("/api/race")
async def api_race(request: Request):
    """Record a solo result; lobby races are recorded server-side."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    try:
        wpm = max(0.0, min(400.0, float(body.get("wpm", 0))))
        acc = max(0.0, min(100.0, float(body.get("acc", 100))))
        seconds = max(0.0, min(7200.0, float(body.get("seconds", 0))))
    except (TypeError, ValueError):
        return JSONResponse({"error": "bad_values"}, status_code=400)

    await run_in_threadpool(
        db.record_race,
        int(user["id"]),
        str(body.get("language", ""))[:20],
        str(body.get("level", ""))[:10],
        str(body.get("topic", ""))[:24],
        wpm,
        acc,
        seconds,
        None,
        None,
        client_ip(request),
    )
    return {"ok": True}


# ---------- websocket ----------
@app.websocket("/ws/{code}")
async def ws_lobby(
    websocket: WebSocket,
    code: str,
    name: str = Query("Guest"),
    pid: str = Query(""),
    create: int = Query(0),
    lang: str = Query("python"),
    levels: str = Query(""),
    topics: str = Query(""),
    duration: int = Query(-1),
):
    code = code.upper()
    await websocket.accept()

    lobby = lobbies.get(code)
    if lobby is None:
        if not create:
            await websocket.send_text(json.dumps({"t": "error", "code": "no_lobby"}))
            await websocket.close()
            return
        lobby = Lobby(
            code,
            lang,
            parse_ids(levels, LEVEL_IDS),
            parse_ids(topics, TOPIC_IDS),
            None if duration < 0 else duration,
        )
        lobbies[code] = lobby

    pid = pid or uuid.uuid4().hex[:12]
    ip = client_ip(websocket)

    # A recognised player races under their saved profile name.
    account = None
    if db.enabled():
        token = websocket.cookies.get(COOKIE_NAME, "")
        if token:
            account = await run_in_threadpool(db.find_by_token, token)
    if account is not None:
        name = account["name"]
        await run_in_threadpool(db.seen, int(account["id"]), ip)

    name = (name or "Guest").strip()[:18] or "Guest"
    taken = {p.name for p in lobby.players.values() if p.id != pid}
    base, suffix = name, 2
    while name in taken:
        name = base + str(suffix)
        suffix += 1

    player = Player(pid, name, websocket)
    player.ip = ip
    if account is not None:
        player.uid = int(account["id"])
        player.avatar = int(account.get("avatar_version") or 0) if account.get("avatar_mime") else 0
    if lobby.state in ("racing", "countdown"):
        player.finished = True  # late joiner spectates this round
    lobby.players[pid] = player
    if pid not in lobby.order:
        lobby.order.append(pid)
    if lobby.host is None or lobby.host not in lobby.players:
        lobby.host = pid

    await websocket.send_text(
        json.dumps({"t": "hello", "id": pid, "name": name, "code": code, "uid": player.uid})
    )
    for msg in lobby.chat[-40:]:
        await websocket.send_text(json.dumps(msg))
    await lobby.push_state()
    await lobby.system(name + " joined")

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            kind = msg.get("t")

            if kind == "chat":
                text = str(msg.get("text", "")).strip()[:400]
                if not text:
                    continue
                out = {
                    "t": "chat",
                    "name": player.name,
                    "id": pid,
                    "uid": player.uid,
                    "avatar": player.avatar,
                    "text": text,
                    "ts": time.time(),
                }
                lobby.chat.append(out)
                del lobby.chat[: -chat_limit()]
                await lobby.broadcast(out)

            elif kind == "ready":
                player.ready = bool(msg.get("v"))
                await lobby.push_state()
                racers = lobby.roster()
                if (
                    lobby.state == "waiting"
                    and len(racers) > 1
                    and all(p.ready for p in racers)
                ):
                    await lobby.start_race()

            elif kind == "lang":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                value = str(msg.get("v", "python"))
                if value in LANGUAGE_IDS:
                    lobby.language = value
                    lobby.reroll()
                    await lobby.push_state()
                    await lobby.system("language set to " + value)

            elif kind == "filters":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                lobby.levels = clean_ids(msg.get("levels"), LEVEL_IDS)
                lobby.topics = clean_ids(msg.get("topics"), TOPIC_IDS)
                lobby.reroll()
                await lobby.push_state()
                await lobby.system(
                    "levels: %s · topics: %s"
                    % (
                        ", ".join(lobby.levels) or "any",
                        ", ".join(lobby.topics) or "any",
                    )
                )

            elif kind == "duration":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                lobby.duration = clean_duration(msg.get("v", 0))
                lobby.reroll()
                await lobby.push_state()
                await lobby.system(
                    "race time: %s"
                    % ("%ds" % lobby.duration if lobby.duration else "one snippet")
                )

            elif kind == "start":
                if pid == lobby.host:
                    await lobby.start_race()

            elif kind == "again":
                if pid == lobby.host:
                    await lobby.reset_to_lobby()

            elif kind == "progress":
                if lobby.state != "racing" or player.finished:
                    continue
                player.progress = max(0.0, min(1.0, float(msg.get("p", 0))))
                player.wpm = max(0.0, float(msg.get("wpm", 0)))
                player.acc = max(0.0, min(100.0, float(msg.get("acc", 100))))
                player.idx = max(0, min(len(lobby.playlist) - 1, int(msg.get("idx", 0))))
                player.chars = max(0, min(2_000_000, int(msg.get("chars", 0))))
                player.snips = max(0, min(len(lobby.playlist), int(msg.get("snips", 0))))
                await lobby.broadcast(
                    {
                        "t": "prog",
                        "id": pid,
                        "p": round(player.progress, 4),
                        "wpm": round(player.wpm, 1),
                        "acc": round(player.acc, 1),
                        "idx": player.idx,
                        "chars": player.chars,
                        "snips": player.snips,
                    },
                    skip=pid,
                )

            elif kind == "finish":
                if player.finished:
                    continue
                player.finished = True
                player.progress = 1.0
                player.wpm = max(0.0, min(400.0, float(msg.get("wpm", 0))))
                player.acc = max(0.0, min(100.0, float(msg.get("acc", 100))))
                player.time = max(0.0, float(msg.get("time", 0)))
                player.chars = max(0, min(2_000_000, int(msg.get("chars", player.chars))))
                player.snips = max(0, min(len(lobby.playlist), int(msg.get("snips", player.snips))))
                lobby.finish_count += 1
                player.place = lobby.finish_count
                if lobby.duration > 0:
                    # The clock still decides the race; this racer just ran out of
                    # playlist. Skip the per-snippet bookkeeping below.
                    await lobby.system(
                        "%s cleared all %d snippets" % (player.name, player.snips)
                    )
                    await lobby.push_state()
                    await lobby.maybe_finish()
                    continue
                if player.uid and db.enabled():
                    try:
                        await run_in_threadpool(
                            db.record_race,
                            player.uid,
                            lobby.language,
                            lobby.snip["level"],
                            lobby.snip["topic"],
                            player.wpm,
                            player.acc,
                            player.time,
                            player.place,
                            lobby.code,
                            player.ip,
                        )
                    except Exception as exc:
                        log.warning("could not record race: %s", exc)
                await lobby.system(
                    "%s finished #%d at %.0f wpm" % (player.name, player.place, player.wpm)
                )
                await lobby.push_state()
                await lobby.maybe_finish()

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        lobby.players.pop(pid, None)
        if pid in lobby.order:
            lobby.order.remove(pid)
        if lobby.players:
            if lobby.host == pid:
                lobby.host = lobby.order[0] if lobby.order else next(iter(lobby.players))
            await lobby.system(player.name + " left")
            await lobby.push_state()
            await lobby.maybe_finish()
        else:
            lobby.cancel_task()
            lobbies.pop(code, None)


@app.get("/healthz")
async def healthz():
    return {
        "ok": True,
        "lobbies": len(lobbies),
        "db": db.enabled(),
        "snippets": sum(len(v) for v in library.all_snippets().values()),
        "library": library.source(),
    }


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    # The game panel assigns the port; never hardcode it.
    port = env_int("SERVER_PORT", env_int("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=os.environ.get("LOG_LEVEL", "info"),
        proxy_headers=True,
        forwarded_allow_ips="*",
        ws_ping_interval=env_int("WS_PING_INTERVAL", 20),
        ws_ping_timeout=env_int("WS_PING_TIMEOUT", 20),
    )
