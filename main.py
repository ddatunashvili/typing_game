"""FastAPI backend for the code typing race: lobbies, chat and live progress."""
import asyncio
import json
import os
import random
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from snippets import LANGUAGES, SNIPPETS, random_snippet

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Load .env if present (uploaded through the panel's Files tab in production).
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:  # dotenv is optional; real env vars still win
    pass


def env_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, "").strip() or default)
    except ValueError:
        return default


app = FastAPI(title=os.environ.get("APP_TITLE", "Code Typing Race"))

COUNTDOWN_SECONDS = env_int("COUNTDOWN_SECONDS", 5)
CHAT_HISTORY = max(1, env_int("CHAT_HISTORY", 100))  # [:-0] would wipe the log
LOBBY_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def new_code() -> str:
    while True:
        code = "".join(random.choice(LOBBY_CODE_ALPHABET) for _ in range(5))
        if code not in lobbies:
            return code


class Player:
    def __init__(self, pid: str, name: str, ws: WebSocket):
        self.id = pid
        self.name = name
        self.ws = ws
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
    def __init__(self, code: str, language: str = "python"):
        self.code = code
        self.language = language if language in SNIPPETS else "python"
        self.snippet = random_snippet(self.language)
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

    def snapshot(self) -> dict:
        return {
            "t": "state",
            "code": self.code,
            "language": self.language,
            "state": self.state,
            "host": self.host,
            "snippet": self.snippet,
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
        self.snippet = random_snippet(self.language, avoid=self.snippet)
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


@app.get("/api/languages")
async def api_languages():
    return [{"id": lid, "label": label} for lid, label in LANGUAGES]


@app.get("/api/snippet")
async def api_snippet(lang: str = "python", avoid: str = ""):
    return {"language": lang, "snippet": random_snippet(lang, avoid=avoid)}


@app.get("/api/lobby/new")
async def api_new_lobby(lang: str = "python"):
    code = new_code()
    lobbies[code] = Lobby(code, lang)
    return {"code": code}


@app.get("/api/lobby/{code}")
async def api_lobby(code: str):
    lobby = lobbies.get(code.upper())
    if not lobby:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return lobby.snapshot()


@app.websocket("/ws/{code}")
async def ws_lobby(
    websocket: WebSocket,
    code: str,
    name: str = Query("Guest"),
    pid: str = Query(""),
    create: int = Query(0),
    lang: str = Query("python"),
):
    code = code.upper()
    await websocket.accept()

    lobby = lobbies.get(code)
    if lobby is None:
        if not create:
            await websocket.send_text(json.dumps({"t": "error", "code": "no_lobby"}))
            await websocket.close()
            return
        lobby = Lobby(code, lang)
        lobbies[code] = lobby

    pid = pid or uuid.uuid4().hex[:12]
    name = (name or "Guest").strip()[:18] or "Guest"
    taken = {p.name for p in lobby.players.values() if p.id != pid}
    base, suffix = name, 2
    while name in taken:
        name = base + str(suffix)
        suffix += 1

    player = Player(pid, name, websocket)
    if lobby.state in ("racing", "countdown"):
        player.finished = True  # late joiner spectates this round
    lobby.players[pid] = player
    if pid not in lobby.order:
        lobby.order.append(pid)
    if lobby.host is None or lobby.host not in lobby.players:
        lobby.host = pid

    await websocket.send_text(
        json.dumps({"t": "hello", "id": pid, "name": name, "code": code})
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
                    lobby.snippet = random_snippet(value)
                    await lobby.push_state()
                    await lobby.system("language set to " + value)

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
                player.wpm = max(0.0, float(msg.get("wpm", 0)))
                player.acc = max(0.0, min(100.0, float(msg.get("acc", 100))))
                player.time = max(0.0, float(msg.get("time", 0)))
                lobby.finish_count += 1
                player.place = lobby.finish_count
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
    return {"ok": True, "lobbies": len(lobbies)}


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
