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
from snippets import (
    LANGUAGES,
    LEVEL_IDS,
    SNIPPETS,
    TOPIC_IDS,
    catalog,
    clean_ids,
    count_matching,
    languages,
    levels,
    parse_ids,
    pick_snippet,
    topics,
)

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
    yield
    await run_in_threadpool(db.close)


app = FastAPI(
    title=os.environ.get("APP_TITLE", "Code Typing Race"),
    lifespan=lifespan,
)

COUNTDOWN_SECONDS = env_int("COUNTDOWN_SECONDS", 5)
CHAT_HISTORY = max(1, env_int("CHAT_HISTORY", 100))  # [:-0] would wipe the log
LOBBY_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

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
        self.progress = 0.0
        self.wpm = 0.0
        self.acc = 100.0
        self.finished = False
        self.place: Optional[int] = None
        self.time: Optional[float] = None

    def reset(self) -> None:
        self.ready = False
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
    ):
        self.code = code
        self.language = language if language in SNIPPETS else "python"
        self.levels: List[str] = clean_ids(levels_filter, LEVEL_IDS)
        self.topics: List[str] = clean_ids(topics_filter, TOPIC_IDS)
        self.snip = pick_snippet(self.language, "", self.levels, self.topics)
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
        self.snip = pick_snippet(self.language, avoid, self.levels, self.topics)

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
        del self.chat[: -CHAT_HISTORY]
        await self.broadcast(msg)

    def cancel_task(self) -> None:
        if self.task and not self.task.done():
            self.task.cancel()
        self.task = None

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
            for n in range(COUNTDOWN_SECONDS, 0, -1):
                await self.broadcast({"t": "countdown", "n": n})
                await asyncio.sleep(1)
            self.state = "racing"
            self.start_ts = time.time()
            await self.broadcast({"t": "go", "start_ts": self.start_ts})
            await self.push_state()
        except asyncio.CancelledError:
            pass

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
        if self.state == "racing" and racers and all(p.finished for p in racers):
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


# ---------- lobbies ----------
@app.get("/api/lobby/new")
async def api_new_lobby(lang: str = "python", levels: str = "", topics: str = ""):
    code = new_code()
    lobbies[code] = Lobby(
        code,
        lang,
        parse_ids(levels, LEVEL_IDS),
        parse_ids(topics, TOPIC_IDS),
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
):
    code = code.upper()
    await websocket.accept()

    lobby = lobbies.get(code)
    if lobby is None:
        if not create:
            await websocket.send_text(json.dumps({"t": "error", "code": "no_lobby"}))
            await websocket.close()
            return
        lobby = Lobby(code, lang, parse_ids(levels, LEVEL_IDS), parse_ids(topics, TOPIC_IDS))
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
                del lobby.chat[: -CHAT_HISTORY]
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
                if value in SNIPPETS:
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
                await lobby.broadcast(
                    {
                        "t": "prog",
                        "id": pid,
                        "p": round(player.progress, 4),
                        "wpm": round(player.wpm, 1),
                        "acc": round(player.acc, 1),
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
                lobby.finish_count += 1
                player.place = lobby.finish_count
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
    return {"ok": True, "lobbies": len(lobbies), "db": db.enabled()}


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
