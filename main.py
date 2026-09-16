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
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
)
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

import achievements
import bots
import db
import library
import rating
import social
from library import (
    catalog,
    count_matching,
    pick_snippet,
    setting_int,
)
from snippets import (
    LANGUAGES,
    normalize,
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
    # Every database call goes through run_in_threadpool, against a server that
    # answers in ~170ms. The default pool is 40 threads; a burst of finishing
    # races - persistence plus achievement checks is ~10 queries per player -
    # filled it, and every other request queued behind them (the feed took
    # 20 seconds during one such burst). More threads is the right fix for
    # I/O-bound waits: each one is idle on a socket, not burning a core.
    try:
        import anyio.to_thread as _threads

        limiter = _threads.current_default_thread_limiter()
        before = limiter.total_tokens
        limiter.total_tokens = max(before, env_int("THREAD_POOL", 120))
        log.info("thread pool: %d -> %d", before, limiter.total_tokens)
    except Exception as exc:  # anyio internals moved: keep the default
        log.warning("could not resize the thread pool: %s", exc)
    keeper = asyncio.create_task(house_keeper())
    yield
    keeper.cancel()
    await run_in_threadpool(db.close)


app = FastAPI(
    title=os.environ.get("APP_TITLE", "Code Typing Race"),
    lifespan=lifespan,
)

LOBBY_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
MAX_RACE_SECONDS = 1800

# Classic mode ends when everyone has finished, which means one racer who stops
# typing holds the whole lobby open. Once the first player is home the rest get
# this long to finish, and then the race closes without them. Joining midway is
# allowed now, so an idle straggler is a good deal more likely than it was.
LAST_CALL_SECONDS = env_int("LAST_CALL_SECONDS", 60)


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

# Absolute origin used in canonical / Open Graph tags. Social scrapers reject
# relative image URLs, so this has to be the real public address.
SITE_URL = os.environ.get("SITE_URL", "https://coderace.renode.space").rstrip("/")

# Re-attach a visitor who has no cookie to the last account seen from their IP.
# Everyone behind one NAT shares an address, so this cannot tell apart people in
# the same house or office - they land on the same profile. Set to 0 to make the
# cookie the only identity.
IP_AUTOLOGIN = (os.environ.get("IP_AUTOLOGIN", "1").strip().lower()
                not in ("0", "false", "no", "off"))

_index_cache: Dict[str, object] = {"mtime": None, "html": ""}


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
    def __init__(self, pid: str, name: str, ws: Optional[WebSocket]):
        self.id = pid
        self.name = name
        self.ws = ws  # None for a bot: nothing to send to
        self.bot: Optional[dict] = None
        self.rating = rating.START_RATING
        self.stars = 0
        self.delta = 0
        self.pos = 0  # caret position in the current snippet
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
        self.gave_up = False
        self.place: Optional[int] = None
        self.time: Optional[float] = None
        # Keystroke timeline, and the post it belongs to once that exists.
        # Whichever of the two arrives second does the write.
        self.replay: Optional[list] = None
        self.post_id: Optional[int] = None

    def reset(self) -> None:
        self.ready = bool(self.bot)  # bots are always up for a race
        self.pos = 0
        self.stars = 0
        self.delta = 0
        self.idx = 0
        self.chars = 0
        self.snips = 0
        self.progress = 0.0
        self.wpm = 0.0
        self.acc = 100.0
        self.finished = False
        self.gave_up = False
        self.place = None
        self.time = None
        self.replay = None
        self.post_id = None

    def public(self) -> dict:
        return {
            "id": self.id,
            "uid": self.uid,
            "avatar": self.avatar,
            "name": self.name,
            "bot": bool(self.bot),
            "slug": (self.bot or {}).get("slug"),
            "rating": int(self.rating),
            "rank": rating.rank_for(self.rating),
            "stars": self.stars,
            "delta": self.delta,
            "ready": self.ready,
            "pos": self.pos,
            "idx": self.idx,
            "chars": self.chars,
            "snips": self.snips,
            "progress": round(self.progress, 4),
            "wpm": round(self.wpm, 1),
            "acc": round(self.acc, 1),
            "finished": self.finished,
            "gave_up": self.gave_up,
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
        private: bool = False,
        key: str = "",
        title: str = "",
        strict: bool = False,
        ranked: bool = True,
        suggest: bool = False,
        limit: int = 0,
        house: bool = False,
    ):
        self.code = code
        # 0 means no limit. Counts racers only - a spectator takes no seat.
        self.limit = max(0, min(32, int(limit or 0)))
        # A house lobby is one the server opened. It is listed while empty and
        # is not torn down when the last person leaves, so the browser is never
        # a blank page for whoever arrives first.
        self.house = bool(house)
        # Strict: no auto-skipping of leading indentation, every space typed.
        self.strict = bool(strict)
        # Suggestions: Tab completes the language keyword under the caret.
        self.suggest = bool(suggest)
        # Unranked: the race is recorded in full, it just does not move Elo.
        self.ranked = bool(ranked)
        # A private lobby is hidden from the browser unless it has a key, in
        # which case it is listed as locked and the key is the way in. The code
        # on its own is never enough for a keyed lobby.
        self.private = bool(private)
        self.key = str(key or "")[:24]
        self.title = str(title or "")[:40]
        self.watchers: Dict[str, Player] = {}
        self.language = language if language in LANGUAGE_IDS else "python"
        self.levels: List[str] = clean_ids(levels_filter, LEVEL_IDS)
        self.topics: List[str] = clean_ids(topics_filter, library.topic_ids())
        # 0 = classic (one snippet), >0 = timed run through a playlist
        self.duration = clean_duration(
            default_race_seconds() if duration is None else duration
        )
        self.timer: Optional[asyncio.Task] = None
        self.ends_at: float = 0.0
        self.snip: dict = {}
        self.playlist: List[dict] = []
        self.bag = library.Bag()
        self.bot_tasks: List[asyncio.Task] = []
        # once a race has a level, later snippets stick to it until the
        # filters change, so difficulty does not jump around mid-session
        self.level_lock: Optional[str] = None
        self.reroll()  # fills snip + playlist to match the mode
        self.players: Dict[str, Player] = {}
        self.order: List[str] = []
        self.host: Optional[str] = None
        self.state = "waiting"  # waiting | countdown | racing | finished
        self.start_ts: float = 0.0
        self.task: Optional[asyncio.Task] = None
        self.chat: List[dict] = []
        self.finish_count = 0
        self.last_call: Optional[asyncio.Task] = None

    def add_bot(self, slug: str) -> Optional[Player]:
        """Seat a bot. Returns None for an unknown slug or a duplicate."""
        bot = bots.get(slug)
        if bot is None:
            return None
        if any(p.bot and p.bot["slug"] == bot["slug"] for p in self.players.values()):
            return None
        pid = "bot-" + bot["slug"]
        player = Player(pid, bot["name"], None)
        player.bot = bot
        player.rating = int(bot["rating"])
        player.ready = True
        player.acc = float(bot["acc"])
        if self.state in ("racing", "countdown"):
            player.finished = True  # it can join the next one
        self.players[pid] = player
        if pid not in self.order:
            self.order.append(pid)
        return player

    def remove_bot(self, slug: str) -> bool:
        pid = "bot-" + (slug or "")
        if pid not in self.players:
            return False
        self.players.pop(pid, None)
        if pid in self.order:
            self.order.remove(pid)
        return True

    def humans(self) -> List[Player]:
        return [p for p in self.roster() if not p.bot]

    def full(self, pid: str = "") -> bool:
        """Is there a seat left? A player rejoining their own seat always fits."""
        if not self.limit:
            return False
        seated = [p for p in self.roster() if p.id != pid]
        return len(seated) >= self.limit

    def watcher_list(self) -> List[dict]:
        return [
            {"id": w.id, "name": w.name, "uid": w.uid, "avatar": w.avatar}
            for w in self.watchers.values()
        ]

    def listing(self) -> dict:
        """One row for the lobby browser. Never leaks the key itself."""
        racers = self.roster()
        host = self.players.get(self.host or "")
        return {
            "code": self.code,
            "title": self.title,
            "language": self.language,
            "levels": self.levels,
            "topics": self.topics,
            "duration": self.duration,
            "state": self.state,
            "private": self.private,
            "locked": bool(self.key),
            "strict": self.strict,
            "ranked": self.ranked,
            "suggest": self.suggest,
            "limit": self.limit,
            "house": self.house,
            "host": host.name if host else "",
            "players": len(racers),
            "humans": len([p for p in racers if not p.bot]),
            "bots": len([p for p in racers if p.bot]),
            "watchers": len(self.watchers),
            "names": [p.name for p in racers][:8],
        }

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
            # shuffled deck, pinned to the level this lobby is already on
            self.snip = self.bag.deal(
                self.language, self.levels, self.topics, self.level_lock
            )
            self.playlist = [self.snip]
        self.level_lock = self.snip.get("level") or None

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
            "output": self.snip.get("output") or "",
            "matches": count_matching(self.language, self.levels, self.topics),
            "duration": self.duration,
            "ends_at": self.ends_at,
            "playlist": [
                {
                    "code": s["code"],
                    "level": s["level"],
                    "topic": s["topic"],
                    "output": s.get("output") or "",
                }
                for s in self.playlist
            ],
            "start_ts": self.start_ts,
            "private": self.private,
            "locked": bool(self.key),
            "title": self.title,
            "strict": self.strict,
            "ranked": self.ranked,
            "suggest": self.suggest,
            "limit": self.limit,
            "house": self.house,
            "players": [p.public() for p in self.roster()],
            "watchers": self.watcher_list(),
        }

    async def broadcast(self, message: dict, skip: Optional[str] = None) -> None:
        """Send to every racer and every spectator watching this lobby."""
        payload = json.dumps(message)
        dead = []
        for pid, player in list(self.players.items()):
            if pid == skip or player.ws is None:
                continue
            try:
                await player.ws.send_text(payload)
            except Exception:
                dead.append(pid)
        for pid in dead:
            self.players.pop(pid, None)
        gone = []
        for wid, watcher in list(self.watchers.items()):
            if wid == skip or watcher.ws is None:
                continue
            try:
                await watcher.ws.send_text(payload)
            except Exception:
                gone.append(wid)
        for wid in gone:
            self.watchers.pop(wid, None)

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
        if self.last_call and not self.last_call.done():
            self.last_call.cancel()
        self.last_call = None
        self.ends_at = 0.0
        for task in self.bot_tasks:
            if not task.done():
                task.cancel()
        self.bot_tasks = []

    async def start_race(self) -> None:
        if self.state in ("countdown", "racing"):
            return
        self.reroll(avoid=self.snip["code"])
        for player in self.players.values():
            player.reset()
        self.finish_count = 0
        self.state = "countdown"
        await self.push_state()
        asyncio.create_task(announce_lobbies())
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
            for player in self.roster():
                if player.bot and not player.finished:
                    self.bot_tasks.append(
                        asyncio.create_task(self._drive_bot(player))
                    )
            await self.broadcast(
                {"t": "go", "start_ts": self.start_ts, "ends_at": self.ends_at}
            )
            await self.push_state()
        except asyncio.CancelledError:
            pass

    async def _drive_bot(self, player: Player) -> None:
        """Type on the bot's behalf: roughly its target wpm, with hesitations."""
        bot = player.bot or {}
        chars_per_sec = max(1.0, float(bot.get("wpm", 40)) * 5.0 / 60.0)
        stumble = float(bot.get("stumble", 0.05))
        player.acc = float(bot.get("acc", 96.0))
        tick = 0.25
        pos = 0.0
        lines = list(bots.roasts(bot.get("slug", "")))
        random.shuffle(lines)
        # first jab lands a couple of seconds in, then every so often
        next_roast = time.time() + random.uniform(2.5, 5.0)
        try:
            while self.state == "racing" and not player.finished:
                await asyncio.sleep(tick)
                if self.state != "racing":
                    return
                if random.random() < stumble:
                    await asyncio.sleep(random.uniform(0.15, 0.6))
                pos += chars_per_sec * tick * random.uniform(0.82, 1.18)

                current = self.playlist[min(player.idx, len(self.playlist) - 1)]
                length = max(1, len(current["code"]))

                if pos >= length:
                    player.chars += length
                    player.snips += 1
                    pos = 0.0
                    if self.duration > 0 and player.idx + 1 < len(self.playlist):
                        player.idx += 1
                    else:
                        await self._bot_finish(player)
                        return

                now = time.time()
                if lines and now >= next_roast:
                    await self.broadcast(
                        {
                            "t": "chat",
                            "name": player.name,
                            "id": player.id,
                            "slug": bot.get("slug"),
                            "bot": True,
                            "text": lines.pop(),
                            "ts": now,
                        }
                    )
                    next_roast = now + random.uniform(6.0, 13.0)

                elapsed = max(0.5, now - self.start_ts)
                player.pos = int(pos)
                player.progress = min(1.0, pos / length)
                player.wpm = ((player.chars + pos) / 5.0) / (elapsed / 60.0)
                await self.broadcast(
                    {
                        "t": "prog",
                        "id": player.id,
                        "p": round(player.progress, 4),
                        "wpm": round(player.wpm, 1),
                        "acc": round(player.acc, 1),
                        "pos": player.pos,
                        "idx": player.idx,
                        "chars": player.chars,
                        "snips": player.snips,
                    }
                )
        except asyncio.CancelledError:
            pass

    async def _bot_finish(self, player: Player) -> None:
        player.finished = True
        player.progress = 1.0
        player.pos = 0
        player.time = max(0.1, time.time() - self.start_ts)
        elapsed = max(0.5, player.time)
        player.wpm = (player.chars / 5.0) / (elapsed / 60.0)
        if self.duration > 0:
            await self.system("%s cleared the playlist" % player.name)
            await self.push_state()
            await self.maybe_finish()
            return
        self.finish_count += 1
        player.place = self.finish_count
        await self.system(
            "%s finished #%d at %.0f wpm" % (player.name, player.place, player.wpm)
        )
        self.arm_last_call()
        await self.push_state()
        await self.maybe_finish()

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
        # Anyone who resigned sorts below everyone still typing, however far
        # they had got before they quit.
        ranked = sorted(racers, key=lambda p: (p.gave_up, -p.chars, -p.acc))
        for i, player in enumerate(ranked, start=1):
            player.finished = True
            player.place = i
            if player.time is None:
                player.time = float(self.duration)
        self.state = "finished"
        self.ends_at = 0.0
        await self.broadcast({"t": "time_up"})
        await self.score_race()
        await self.push_state()

    def arm_last_call(self) -> None:
        """Start the countdown that closes a classic race on the stragglers."""
        if self.duration > 0 or self.state != "racing":
            return  # timed mode already has a clock of its own
        if self.last_call and not self.last_call.done():
            return
        self.last_call = asyncio.create_task(self._last_call())

    async def _last_call(self) -> None:
        try:
            await self.system(
                "first one home - %ds left for everyone else" % LAST_CALL_SECONDS
            )
            await asyncio.sleep(LAST_CALL_SECONDS)
            if self.state != "racing":
                return
            stragglers = [p for p in self.roster() if not p.finished]
            if not stragglers:
                return
            for player in stragglers:
                # They did not complete the snippet, so they score as if they
                # had stopped - but they are out of time, not out of nerve.
                player.gave_up = True
                player.finished = True
                if player.time is None:
                    player.time = max(0.0, time.time() - self.start_ts)
            await self.system("time called - the race is closed")
            await self.push_state()
            await self.maybe_finish()
        except asyncio.CancelledError:
            pass

    async def resign(self, player: Player) -> None:
        """A racer gives up: they stop, but the race carries on without them.

        No place is handed out here. Whoever is still typing keeps claiming the
        next real finishing position, and the quitters are slotted in behind
        them once the race closes.
        """
        if self.state != "racing" or player.finished:
            return
        player.gave_up = True
        player.finished = True
        player.time = max(0.0, time.time() - self.start_ts)
        await self.system("%s gave up" % player.name)
        await self.push_state()
        await self.maybe_finish()

    def seat_quitters(self) -> None:
        """Give every resigner a place, behind the racers who finished."""
        quitters = [p for p in self.roster() if p.place is None]
        quitters.sort(key=lambda p: -p.progress)
        for i, player in enumerate(quitters, start=self.finish_count + 1):
            player.place = i

    async def reset_to_lobby(self) -> None:
        self.cancel_task()
        self.state = "waiting"
        self.start_ts = 0.0
        self.finish_count = 0
        for player in self.players.values():
            player.reset()
        await self.push_state()

    async def score_race(self) -> None:
        """Settle the race in memory, show it, then write it down."""
        racers = self.roster()
        if not racers:
            return
        self.settle(racers)
        await self.push_state()
        asyncio.create_task(self.persist(racers))

    def settle(self, racers: List[Player]) -> None:
        """Stars and Elo. Pure bookkeeping - no database, no waiting."""

        length = max(1, len(self.snip.get("code", "")))
        if self.duration > 0:
            length = max(1, sum(len(s["code"]) for s in self.playlist[: max(1, 1)]))

        # In timed mode the distance actually covered is what matters, not the
        # length of one snippet.
        for player in racers:
            if player.bot:
                player.stars = rating.BOT_STARS  # synthetic accuracy: no stars
                continue
            span = max(1, player.chars) if self.duration > 0 else length
            errors = max(0, int(round(span * (100.0 - player.acc) / 100.0)))
            completed = bool(player.finished) and not player.gave_up
            player.stars = rating.stars(
                player.acc, errors, span, completed, player.place == 1
            )

        # Elo: guests and bots are opposition but keep no rating of their own.
        entries = [
            {
                "key": p.id,
                "rating": float(p.rating),
                "place": p.place,
                "provisional": bool(p.bot) or not p.uid,
            }
            for p in racers
        ]
        # Two conditions have to hold for anyone's rating to move: the lobby is
        # ranked, and at least two rated players were in it. A bot types at a
        # fixed synthetic speed, so beating one says nothing about you and must
        # not be worth rating - and the same goes for a lobby of one.
        rated = [p for p in racers if p.uid and not p.bot]
        contested = self.ranked and len(rated) > 1
        deltas = rating.race_deltas(entries) if contested and len(entries) > 1 else {}
        for player in racers:
            player.delta = int(deltas.get(player.id, 0))
            if player.delta:
                player.rating = rating.apply_delta(player.rating, player.delta)

    def replay_codes(self) -> List[str]:
        return [s.get("code", "") for s in self.playlist]

    async def keep_replay(self, player: Player) -> None:
        """Write the replay once both the timeline and the post exist."""
        if not player.replay or not player.post_id or not player.uid:
            return
        events, player.replay = player.replay, None
        try:
            await run_in_threadpool(
                db.save_replay,
                player.post_id,
                player.uid,
                self.language,
                self.replay_codes(),
                events,
                float(player.time or 0.0),
            )
        except Exception as exc:
            log.warning("could not save replay for %s: %s", player.name, exc)

    async def persist(self, racers: List[Player]) -> None:
        """Write the race to the database and hand out anything it unlocked."""
        if not db.enabled():
            return
        level = "mixed" if len(self.playlist) > 1 else self.snip.get("level", "")
        topic = "mixed" if len(self.playlist) > 1 else self.snip.get("topic", "")
        # who each racer was up against, for the post text
        names = [p.name for p in racers]
        for player in racers:
            if player.bot or not player.uid:
                continue
            others = ", ".join(n for n in names if n != player.name)[:255]
            try:
                await run_in_threadpool(
                    db.record_race,
                    player.uid,
                    self.language,
                    level,
                    topic,
                    player.wpm,
                    player.acc,
                    float(player.time or 0.0),
                    player.place,
                    self.code,
                    player.ip,
                    player.stars,
                    player.delta,
                )
            except Exception as exc:
                log.warning("could not record race for %s: %s", player.name, exc)

            # the same race also lands on their profile as a post
            try:
                player.post_id = await run_in_threadpool(
                    social.add_post,
                    player.uid,
                    self.language,
                    level,
                    topic,
                    player.wpm,
                    player.acc,
                    float(player.time or 0.0),
                    player.place,
                    player.stars,
                    player.delta,
                    others,
                    "",
                    "race",
                )
            except Exception as exc:
                log.warning("could not post race for %s: %s", player.name, exc)
            await self.keep_replay(player)

            # Anything this result has just unlocked. Done after the race is
            # recorded, so the totals it reads already include this race.
            beat_better = any(
                o is not player
                and o.place is not None
                and player.place is not None
                and player.place < o.place
                and o.rating - player.rating >= 200
                for o in racers
            )
            try:
                fresh = await run_in_threadpool(
                    achievements.award,
                    player.uid,
                    {"beat_better": beat_better, "rivals": len(names) - 1},
                )
            except Exception as exc:
                log.warning("could not award achievements: %s", exc)
                fresh = []
            if fresh:
                await self.broadcast(
                    {"t": "awards", "id": player.id, "awards": fresh}
                )
                for item in fresh:
                    await self.system(
                        "%s unlocked %s %s" % (player.name, item["icon"], item["name"])
                    )

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
        self.seat_quitters()
        await self.score_race()
        await self.push_state()
        asyncio.create_task(announce_lobbies())


lobbies: Dict[str, Lobby] = {}

# Ten rooms the server keeps open so the lobby browser is never empty. One per
# entry, refreshed daily; a room somebody is sitting in is left alone.
HOUSE_LOBBY_COUNT = env_int("HOUSE_LOBBIES", 10)
HOUSE_REFRESH_SECONDS = env_int("HOUSE_LOBBY_REFRESH", 86400)

HOUSE_PLAN = [
    {"title": "Warm-up", "lang": "python", "levels": ["very-easy"], "duration": 0},
    {"title": "Coffee break", "lang": "javascript", "levels": ["easy"], "duration": 60},
    {"title": "Sprint", "lang": "typescript", "levels": ["easy"], "duration": 30},
    {"title": "Steady pace", "lang": "go", "levels": ["medium"], "duration": 120},
    {"title": "Deep end", "lang": "rust", "levels": ["hard"], "duration": 0,
     "strict": True},
    {"title": "Curly braces", "lang": "java", "levels": ["medium"], "duration": 60},
    {"title": "Systems", "lang": "c", "levels": ["medium"], "duration": 0},
    {"title": "Query hour", "lang": "sql", "levels": [], "duration": 60},
    {"title": "Front of house", "lang": "css", "levels": [], "duration": 60},
    {"title": "Shell session", "lang": "bash", "levels": [], "duration": 30,
     "ranked": False},
]


def house_lobbies() -> List[Lobby]:
    return [lobby for lobby in lobbies.values() if lobby.house]


def stock_house() -> int:
    """Top the house rooms back up to `HOUSE_LOBBY_COUNT`. Returns how many opened."""
    wanted = max(0, min(len(HOUSE_PLAN), HOUSE_LOBBY_COUNT))
    have = {lobby.title for lobby in house_lobbies()}
    opened = 0
    for plan in HOUSE_PLAN[:wanted]:
        if plan["title"] in have:
            continue
        code = new_code()
        lobbies[code] = Lobby(
            code,
            plan.get("lang", "python"),
            clean_ids(plan.get("levels"), LEVEL_IDS),
            [],
            plan.get("duration", 0),
            title=plan["title"],
            strict=bool(plan.get("strict")),
            ranked=plan.get("ranked", True),
            limit=int(plan.get("limit", 0)),
            house=True,
        )
        opened += 1
    return opened


async def house_keeper() -> None:
    """Open the house rooms at startup, then refresh them once a day.

    A refresh only touches rooms nobody is in: the point is a fresh snippet on
    an idle room, not throwing anyone out of a race they are in the middle of.
    """
    try:
        opened = stock_house()
        log.info("house lobbies open: %d", opened)
        await announce_lobbies()
        while True:
            await asyncio.sleep(HOUSE_REFRESH_SECONDS)
            retired = 0
            for lobby in house_lobbies():
                if lobby.players or lobby.watchers:
                    continue
                lobby.cancel_task()
                lobbies.pop(lobby.code, None)
                retired += 1
            opened = stock_house()
            log.info("house lobbies refreshed: %d retired, %d opened", retired, opened)
            await announce_lobbies()
    except asyncio.CancelledError:
        pass
    except Exception as exc:
        log.warning("house keeper stopped: %s", exc)


# ---------- live notification hub ----------
# One socket per open tab, keyed by account. Everything that used to arrive on
# the 20-second heartbeat poll (invitations, the online list, a decline) is
# pushed down this instead, so a challenge lands the moment it is sent.
hub: Dict[int, List[WebSocket]] = {}


def hub_add(uid: int, ws: WebSocket) -> None:
    hub.setdefault(uid, []).append(ws)


def hub_drop(uid: int, ws: WebSocket) -> None:
    sockets = hub.get(uid)
    if not sockets:
        return
    if ws in sockets:
        sockets.remove(ws)
    if not sockets:
        hub.pop(uid, None)


def hub_online() -> set:
    return set(hub.keys())


def mark_seen(uid: Optional[int], ip: str) -> None:
    """Record activity without making the caller wait for the database."""
    if not uid or not db.enabled():
        return
    asyncio.create_task(run_in_threadpool(db.seen, int(uid), ip))


async def notify(uid: Optional[int], payload: dict) -> None:
    """Send to every tab this account has open. Dead sockets are dropped."""
    if not uid:
        return
    sockets = list(hub.get(int(uid)) or ())
    if not sockets:
        return
    text = json.dumps(payload)
    for ws in sockets:
        try:
            await ws.send_text(text)
        except Exception:
            hub_drop(int(uid), ws)


async def notify_all(payload: dict, skip: Optional[int] = None) -> None:
    for uid in list(hub.keys()):
        if skip is not None and uid == skip:
            continue
        await notify(uid, payload)


async def push_challenges(uid: Optional[int]) -> None:
    """Re-send one account's invitation list. Cheap enough to call on any change."""
    if not uid or not db.enabled() or int(uid) not in hub:
        return
    data = await run_in_threadpool(social.challenges_for, int(uid))
    await notify(int(uid), {"t": "challenges", **data})


async def announce_presence() -> None:
    """Tell every open tab the online list moved, so it refetches once."""
    await notify_all({"t": "presence"})


async def announce_lobbies() -> None:
    """Nudge anyone sitting on the lobby browser to refetch the list."""
    await notify_all({"t": "lobbies"})




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
        "topics": library.all_topics(),
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
    level: str = "",
):
    wanted_levels = parse_ids(levels, LEVEL_IDS)
    wanted_topics = parse_ids(topics, library.topic_ids())
    pinned = level if level in LEVEL_IDS else None
    chosen = pick_snippet(lang, avoid, wanted_levels, wanted_topics, pinned)
    return {
        "language": lang,
        "snippet": chosen["code"],
        "level": chosen["level"],
        "topic": chosen["topic"],
        "output": chosen.get("output") or "",
        "matches": count_matching(lang, wanted_levels, wanted_topics, pinned),
    }


@app.get("/api/playlist")
async def api_playlist(
    lang: str = "python",
    size: int = 12,
    levels: str = "",
    topics: str = "",
    level: str = "",
    unique: int = 0,
):
    """An ordered run of snippets, for a timed solo session."""
    wanted_levels = parse_ids(levels, LEVEL_IDS)
    wanted_topics = parse_ids(topics, library.topic_ids())
    pinned = level if level in LEVEL_IDS else None
    run = library.playlist(
        lang, size, wanted_levels, wanted_topics, pinned, unique=bool(unique)
    )
    return {
        "language": lang,
        "matches": count_matching(lang, wanted_levels, wanted_topics, pinned),
        "playlist": [
            {
                "code": s["code"],
                "level": s["level"],
                "topic": s["topic"],
                "output": s.get("output") or "",
            }
            for s in run
        ],
    }


@app.get("/api/bots")
async def api_bots():
    """The bot roster, for the challenge list."""
    return {"bots": bots.roster(), "ranks": rating.ranks()}


CACHE_WEEK = {"Cache-Control": "public, max-age=604800"}


def _bot_image(slug: str, card: bool = False) -> Response:
    """Imported artwork when it exists, otherwise a generated identicon."""
    bot = bots.get(slug)
    seed = bot["slug"] if bot else (slug or "unknown")
    path = bots.card_art(seed) if card else bots.art(seed)
    if path is not None:
        return FileResponse(path, media_type=bots.media_type(path), headers=CACHE_WEEK)
    return Response(
        content=bots.avatar_svg(seed),
        media_type="image/svg+xml",
        headers=CACHE_WEEK,
    )


@app.get("/api/bot-avatar/{slug}")
async def api_bot_avatar(slug: str):
    # tolerate the old .svg suffix from a cached page
    return _bot_image(slug[:-4] if slug.endswith(".svg") else slug)


@app.get("/api/bot-card/{slug}")
async def api_bot_card(slug: str):
    return _bot_image(slug, card=True)


@app.get("/api/rankings")
async def api_rankings(limit: int = 50, request: Request = None):
    """The rankings board: real players, plus where the viewer sits."""
    rows: List[dict] = []
    if db.enabled():
        rows = await run_in_threadpool(db.leaderboard, limit)
    me = None
    if request is not None:
        user = await current_user(request)
        if user is not None:
            me = db.public_user(user)
    return {
        "rows": rows,
        "me": me,
        "bots": bots.roster(),
        "ranks": rating.ranks(),
        "accounts": db.enabled(),
    }


# ---------- player-submitted snippets ----------
@app.post("/api/snippets")
async def api_submit_snippet(request: Request):
    """Add a snippet of your own, optionally under a brand new topic."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    uid = int(user["id"])

    try:
        body = await request.json()
    except Exception:
        body = {}

    language = str(body.get("language", "")).strip()
    level = str(body.get("level", "")).strip()
    code = str(body.get("code", ""))
    output = str(body.get("output", ""))
    public = bool(body.get("public", True))

    if language not in LANGUAGE_IDS:
        return JSONResponse({"error": "bad_language"}, status_code=400)
    if level not in LEVEL_IDS:
        return JSONResponse({"error": "bad_level"}, status_code=400)

    cleaned = normalize(code)
    if len(cleaned) < 20:
        return JSONResponse({"error": "too_short", "min": 20}, status_code=400)
    if len(cleaned) > 4000:
        return JSONResponse({"error": "too_long", "max": 4000}, status_code=413)

    used = await run_in_threadpool(social.snippets_today, uid)
    if used >= social.SNIPPETS_PER_DAY:
        return JSONResponse(
            {"error": "rate_limited", "per_day": social.SNIPPETS_PER_DAY},
            status_code=429,
        )

    # a player may invent a topic instead of picking an existing one
    topic = str(body.get("topic", "")).strip()
    new_topic = str(body.get("new_topic", "")).strip()
    if new_topic:
        made = await run_in_threadpool(social.add_topic, new_topic, uid)
        if made is None:
            return JSONResponse({"error": "bad_topic"}, status_code=400)
        topic = made["id"]
        # the cached topic list predates this one, so re-read it before validating
        await run_in_threadpool(library.refresh_topics)
    if topic not in library.topic_ids():
        return JSONResponse({"error": "bad_topic"}, status_code=400)

    snippet_id = await run_in_threadpool(
        social.submit_snippet,
        uid,
        language,
        level,
        topic,
        cleaned,
        normalize(output) if output else "",
        public,
    )
    if snippet_id is None:
        return JSONResponse({"error": "duplicate"}, status_code=409)

    await run_in_threadpool(library.invalidate)
    return {
        "id": snippet_id,
        "topic": topic,
        "public": public,
        "remaining_today": max(0, social.SNIPPETS_PER_DAY - used - 1),
    }


@app.get("/api/snippets/mine")
async def api_my_snippets(request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    rows = await run_in_threadpool(social.my_snippets, int(user["id"]))
    return {"snippets": rows, "per_day": social.SNIPPETS_PER_DAY}


@app.post("/api/snippets/{snippet_id}/status")
async def api_snippet_status(snippet_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    ok = await run_in_threadpool(
        social.set_snippet_status, snippet_id, int(user["id"]), bool(body.get("public"))
    )
    if not ok:
        return JSONResponse({"error": "not_found"}, status_code=404)
    await run_in_threadpool(library.invalidate)
    return {"ok": True}


@app.delete("/api/snippets/{snippet_id}")
async def api_delete_snippet(snippet_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    ok = await run_in_threadpool(social.delete_snippet, snippet_id, int(user["id"]))
    if not ok:
        return JSONResponse({"error": "not_found"}, status_code=404)
    await run_in_threadpool(library.invalidate)
    return {"ok": True}


@app.post("/api/topics")
async def api_add_topic(request: Request):
    """Create a topic without submitting a snippet for it yet."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    made = await run_in_threadpool(
        social.add_topic, str(body.get("label", "")), int(user["id"])
    )
    if made is None:
        return JSONResponse({"error": "bad_topic"}, status_code=400)
    await run_in_threadpool(library.invalidate)
    return {"topic": made}


# ---------- profiles, feed, reactions, comments ----------
@app.get("/api/profile/{user_id}")
async def api_profile_page(user_id: int, request: Request):
    if not db.enabled():
        return JSONResponse({"error": "accounts_disabled"}, status_code=404)
    who = await run_in_threadpool(social.profile, user_id)
    if who is None:
        return JSONResponse({"error": "not_found"}, status_code=404)
    viewer = await current_user(request)
    viewer_id = int(viewer["id"]) if viewer else None
    posts = await run_in_threadpool(social.feed, 20, None, user_id, viewer_id)
    return {"profile": who, "posts": posts, "me": viewer_id == user_id}


@app.get("/api/feed")
async def api_feed(request: Request, limit: int = 30, before: int = 0):
    if not db.enabled():
        return {"posts": []}
    viewer = await current_user(request)
    viewer_id = int(viewer["id"]) if viewer else None
    posts = await run_in_threadpool(social.feed, limit, before or None, None, viewer_id)
    return {"posts": posts}


@app.post("/api/posts/{post_id}/react")
async def api_react(post_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    try:
        value = int(body.get("value", 0))
    except (TypeError, ValueError):
        value = 0
    return await run_in_threadpool(social.react, post_id, int(user["id"]), value)


@app.get("/api/posts/{post_id}/comments")
async def api_get_comments(post_id: int):
    if not db.enabled():
        return {"comments": []}
    rows = await run_in_threadpool(social.comments, post_id)
    return {"comments": rows}


@app.post("/api/posts/{post_id}/comments")
async def api_add_comment(post_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    uid = int(user["id"])

    try:
        body = await request.json()
    except Exception:
        body = {}
    text = str(body.get("body", "")).strip()
    if not text:
        return JSONResponse({"error": "empty"}, status_code=400)
    if len(text) > social.MAX_BODY:
        return JSONResponse(
            {"error": "too_long", "max": social.MAX_BODY}, status_code=413
        )

    recent = await run_in_threadpool(social.comments_last_hour, uid)
    if recent >= social.COMMENTS_PER_HOUR:
        return JSONResponse(
            {"error": "rate_limited", "per_hour": social.COMMENTS_PER_HOUR},
            status_code=429,
        )

    comment_id = await run_in_threadpool(social.add_comment, post_id, uid, text)
    if comment_id is None:
        return JSONResponse({"error": "empty"}, status_code=400)
    rows = await run_in_threadpool(social.comments, post_id)
    return {"id": comment_id, "comments": rows}


@app.delete("/api/comments/{comment_id}")
async def api_delete_comment(comment_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    ok = await run_in_threadpool(social.delete_comment, comment_id, int(user["id"]))
    if not ok:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return {"ok": True}


@app.delete("/api/posts/{post_id}")
async def api_delete_post(post_id: int, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    ok = await run_in_threadpool(social.delete_post, post_id, int(user["id"]))
    if not ok:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return {"ok": True}


# ---------- reports ----------
@app.post("/api/report")
async def api_report(request: Request):
    """Report a post, comment, snippet or player. Self-moderating by count."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}

    kind = str(body.get("kind", "")).strip()
    reason = str(body.get("reason", "")).strip()
    if kind not in social.REPORT_KINDS:
        return JSONResponse(
            {"error": "bad_kind", "kinds": list(social.REPORT_KINDS)}, status_code=400
        )
    if reason not in social.REPORT_REASONS:
        return JSONResponse(
            {"error": "bad_reason", "reasons": list(social.REPORT_REASONS)},
            status_code=400,
        )
    try:
        target = int(body.get("id", 0))
    except (TypeError, ValueError):
        target = 0
    if target <= 0:
        return JSONResponse({"error": "bad_target"}, status_code=400)

    result = await run_in_threadpool(
        social.add_report,
        kind,
        target,
        int(user["id"]),
        reason,
        str(body.get("note", "")),
        client_ip(request),
    )
    if result.get("hidden") and kind == "snippet":
        await run_in_threadpool(library.invalidate)
    return result


# ---------- find players and challenges ----------
@app.get("/api/players")
async def api_players(request: Request, limit: int = 40):
    if not db.enabled():
        return {"players": [], "accounts": False}
    rows = await run_in_threadpool(social.players, limit)
    viewer = await current_user(request)
    viewer_id = int(viewer["id"]) if viewer else None
    # whoever is sitting in a lobby right now counts as busy
    racing = {}
    for lobby in lobbies.values():
        for p in lobby.roster():
            if p.uid:
                racing[p.uid] = lobby
    # An open notification socket is a better "online" signal than last_seen_at:
    # it drops the instant the tab closes instead of five minutes later.
    live = hub_online()
    for row in rows:
        seat = racing.get(row["id"])
        row["racing"] = seat is not None
        # A spectate link only makes sense for a lobby anyone may walk into.
        row["watch"] = seat.code if seat is not None and not seat.key else ""
        row["state"] = seat.state if seat is not None else ""
        row["me"] = row["id"] == viewer_id
        if row["id"] in live:
            row["online"] = True
            row["idle"] = 0
    return {"players": rows, "accounts": True}


@app.post("/api/heartbeat")
async def api_heartbeat(request: Request):
    """Fallback presence ping for a browser whose notification socket is down."""
    user = await current_user(request)
    if user is None:
        return {"online": False, "challenges": {"incoming": [], "outgoing": []}}
    uid = int(user["id"])
    mark_seen(uid, client_ip(request))
    pending = await run_in_threadpool(social.challenges_for, uid)
    return {"online": True, "challenges": pending}


@app.get("/api/challenges")
async def api_challenges(request: Request):
    user = await current_user(request)
    if user is None:
        return {"incoming": [], "outgoing": []}
    return await run_in_threadpool(social.challenges_for, int(user["id"]))


def open_lobby(code: str, lang: str, levels_ids, topics_ids, duration: int) -> Lobby:
    """Create the lobby for an invitation, reusing one that is already up."""
    lobby = lobbies.get(code)
    if lobby is None:
        lobby = Lobby(code, lang, list(levels_ids), list(topics_ids), duration)
        lobbies[code] = lobby
    return lobby


@app.post("/api/challenge")
async def api_challenge(request: Request):
    """Open a lobby and invite another player into it."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    uid = int(user["id"])

    try:
        body = await request.json()
    except Exception:
        body = {}
    try:
        target = int(body.get("to", 0))
    except (TypeError, ValueError):
        target = 0
    if target <= 0 or target == uid:
        return JSONResponse({"error": "bad_target"}, status_code=400)

    other = await run_in_threadpool(social.name_of, target)
    if other is None:
        return JSONResponse({"error": "no_such_player"}, status_code=404)

    lang = str(body.get("lang") or "python")
    if lang not in LANGUAGE_IDS:
        lang = "python"
    wanted_levels = parse_ids(str(body.get("levels", "")), LEVEL_IDS)
    wanted_topics = parse_ids(str(body.get("topics", "")), library.topic_ids())
    duration = clean_duration(body.get("duration", 0))

    # One live invitation per pair: a second click replaces the first rather
    # than stacking another toast on the other player.
    await run_in_threadpool(social.cancel_open, uid, target)

    code = new_code()
    open_lobby(code, lang, wanted_levels, wanted_topics, duration)

    challenge_id = await run_in_threadpool(
        social.add_challenge,
        uid,
        target,
        code,
        lang,
        ",".join(wanted_levels),
        ",".join(wanted_topics),
        duration,
    )
    # Both sides repaint straight away: the target gets the toast, the sender
    # gets the "waiting for them" row. Off the response path, so the challenger
    # is in their lobby before either list has finished rebuilding.
    asyncio.create_task(push_challenges(target))
    asyncio.create_task(push_challenges(uid))
    return {
        "id": challenge_id,
        "code": code,
        "to": {"id": target, "name": other["name"], "online": target in hub_online()},
    }


@app.post("/api/challenges/{challenge_id}/{action}")
async def api_challenge_action(challenge_id: int, action: str, request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    if action not in ("accept", "decline", "cancel"):
        return JSONResponse({"error": "bad_action"}, status_code=400)

    status = {"accept": "accepted", "decline": "declined", "cancel": "cancelled"}[action]
    row = await run_in_threadpool(
        social.set_challenge_status, challenge_id, int(user["id"]), status
    )
    if row is None:
        return JSONResponse({"error": "not_found"}, status_code=404)

    sender = int(row["from_id"])
    target = int(row["to_id"])
    code = str(row["lobby"])

    if status == "accepted":
        # The sender's lobby is gone if their tab closed or reloaded between the
        # invitation and the answer. Rebuild it from the invitation's own
        # settings instead of failing with "that lobby has already closed".
        if code not in lobbies:
            code = new_code()
            open_lobby(
                code,
                str(row.get("language") or "python"),
                parse_ids(str(row.get("levels") or ""), LEVEL_IDS),
                parse_ids(str(row.get("topics") or ""), library.topic_ids()),
                clean_duration(row.get("duration") or 0),
            )
            await run_in_threadpool(social.set_lobby, challenge_id, code)
        # the sender may be sitting on another screen: send them into the lobby
        await notify(
            sender,
            {
                "t": "challenge_accepted",
                "id": int(row["id"]),
                "code": code,
                "by": user["name"],
            },
        )
    elif status == "declined":
        await notify(
            sender,
            {"t": "challenge_declined", "id": int(row["id"]), "by": user["name"]},
        )
    else:
        await notify(target, {"t": "challenge_cancelled", "id": int(row["id"])})

    asyncio.create_task(push_challenges(sender))
    asyncio.create_task(push_challenges(target))
    return {"id": int(row["id"]), "lobby": code, "status": status}


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
    bot: str = "",
    private: int = 0,
    key: str = "",
    title: str = "",
    strict: int = 0,
    ranked: int = 1,
    suggest: int = 0,
    limit: int = 0,
):
    code = new_code()
    lobby = Lobby(
        code,
        lang,
        parse_ids(levels, LEVEL_IDS),
        parse_ids(topics, library.topic_ids()),
        None if duration < 0 else duration,
        private=bool(private),
        key=key,
        title=title,
        strict=bool(strict),
        ranked=bool(ranked),
        suggest=bool(suggest),
        limit=limit,
    )
    lobbies[code] = lobby
    seated = lobby.add_bot(bot) if bot else None
    return {
        "code": code,
        "bot": seated.name if seated else None,
        "private": lobby.private,
        "locked": bool(lobby.key),
    }


@app.get("/api/lobbies")
async def api_lobbies():
    """The lobby browser.

    Public rooms are listed in full. A private room is listed only when it has
    a key - it shows as locked, with no way in but the key - and a private room
    without one stays completely hidden, reachable by its invite link alone.
    """
    open_rooms, locked_rooms = [], []
    for lobby in lobbies.values():
        if not lobby.players and not lobby.watchers and not lobby.house:
            continue  # created but nobody has connected yet
        if lobby.private and not lobby.key:
            continue
        (locked_rooms if lobby.private else open_rooms).append(lobby.listing())
    open_rooms.sort(key=lambda r: (-r["humans"], r["code"]))
    locked_rooms.sort(key=lambda r: r["code"])
    return {"lobbies": open_rooms + locked_rooms, "count": len(open_rooms) + len(locked_rooms)}


@app.post("/api/lobby/{code}/key")
async def api_check_key(code: str, request: Request):
    """Check a key before opening the socket, so a wrong one reads as wrong."""
    lobby = lobbies.get(code.upper())
    if not lobby:
        return JSONResponse({"error": "not_found"}, status_code=404)
    try:
        body = await request.json()
    except Exception:
        body = {}
    if lobby.key and str(body.get("key") or "") != lobby.key:
        return JSONResponse({"error": "bad_key"}, status_code=403)
    return {"ok": True, "code": lobby.code}


@app.get("/api/lobby/{code}")
async def api_lobby(code: str):
    lobby = lobbies.get(code.upper())
    if not lobby:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return lobby.snapshot()


# ---------- accounts ----------
@app.get("/api/me")
async def api_me(request: Request):
    """Who is this. First-time visitors get an account without being asked."""
    if not db.enabled():
        return {"accounts": False, "user": None}

    ip = client_ip(request)
    row = await current_user(request)
    if row is not None:
        await run_in_threadpool(db.seen, int(row["id"]), ip)
        user = db.public_user(row)
        user["settings"] = db.read_settings(row)
        user.update(db.details_of(row))
        return {"accounts": True, "user": user}

    # No cookie. Re-attach to the account last seen from this IP if there is
    # one, so a cleared cookie does not strand someone's rating.
    if IP_AUTOLOGIN:
        existing = await run_in_threadpool(db.find_by_ip, ip)
        if existing is not None:
            uid = int(existing["id"])
            token = await run_in_threadpool(db.add_token, uid)
            await run_in_threadpool(db.seen, uid, ip)
            response = JSONResponse(
                {"accounts": True, "user": db.public_user(existing), "adopted": True}
            )
            set_token_cookie(response, token, request.url.scheme == "https")
            return response

    # Nothing to attach to: mint a profile with a random handle and identicon.
    handle = await run_in_threadpool(db.random_free_name)
    token, user = await run_in_threadpool(db.register, handle, ip)
    response = JSONResponse({"accounts": True, "user": user, "created": True})
    set_token_cookie(response, token, request.url.scheme == "https")
    return response


@app.post("/api/register")
async def api_register(request: Request):
    if not db.enabled():
        return JSONResponse({"error": "accounts_disabled"}, status_code=503)

    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    name = db.clean_name(str(body.get("name", ""))) or db.random_name()
    ip = client_ip(request)
    existing = await current_user(request)
    if existing is not None:
        # Already recognised: treat a second register as a rename.
        if await run_in_threadpool(db.name_taken, name, int(existing["id"])):
            ideas = await run_in_threadpool(
                db.name_suggestions, name, int(existing["id"]), 5
            )
            return JSONResponse(
                {"error": "name_taken", "name": name, "suggestions": ideas},
                status_code=409,
            )
        await run_in_threadpool(db.rename, int(existing["id"]), name)
        await run_in_threadpool(db.seen, int(existing["id"]), ip)
        row = await run_in_threadpool(db.find_by_token, request.cookies[COOKIE_NAME])
        return {"user": db.public_user(row)}

    if IP_AUTOLOGIN:
        same_ip = await run_in_threadpool(db.find_by_ip, ip)
        if same_ip is not None:
            # one account per IP: rename the existing one instead of adding another
            uid = int(same_ip["id"])
            if await run_in_threadpool(db.name_taken, name, uid):
                ideas = await run_in_threadpool(db.name_suggestions, name, uid, 5)
                return JSONResponse(
                    {"error": "name_taken", "name": name, "suggestions": ideas},
                    status_code=409,
                )
            await run_in_threadpool(db.rename, uid, name)
            token = await run_in_threadpool(db.add_token, uid)
            row = await run_in_threadpool(db.find_by_token, token)
            response = JSONResponse({"user": db.public_user(row), "adopted": True})
            set_token_cookie(response, token, request.url.scheme == "https")
            return response

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

    uid = int(user["id"])
    if await run_in_threadpool(db.name_taken, name, uid):
        ideas = await run_in_threadpool(db.name_suggestions, name, uid, 5)
        return JSONResponse(
            {"error": "name_taken", "name": name, "suggestions": ideas},
            status_code=409,
        )

    await run_in_threadpool(db.rename, uid, name)
    # Country, age and gender are optional: a missing or unusable value clears
    # the field rather than failing the save, so a player can always take one
    # back down again.
    await run_in_threadpool(
        db.save_details,
        uid,
        body.get("country"),
        body.get("birth_year"),
        body.get("gender"),
    )
    row = await run_in_threadpool(db.find_by_token, request.cookies[COOKIE_NAME])
    user = db.public_user(row)
    user.update(db.details_of(row))
    return {"user": user}


@app.get("/api/replay/{post_id}")
async def api_replay(post_id: int):
    """One player's run, as a keystroke timeline plus the code it was typed on."""
    if not db.enabled():
        return JSONResponse({"error": "not_found"}, status_code=404)
    found = await run_in_threadpool(db.get_replay, post_id)
    if found is None:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return found


@app.get("/api/achievements")
async def api_achievements(request: Request, user: int = 0):
    """The whole catalogue, marked up for whoever is being looked at."""
    if not db.enabled():
        return {"achievements": [], "earned": 0, "total": 0, "players": 0}
    viewer = await current_user(request)
    target = user or (int(viewer["id"]) if viewer else 0)
    data = await run_in_threadpool(achievements.board, target or None)
    data["user"] = target
    data["me"] = bool(viewer) and target == int(viewer["id"])
    return data


@app.get("/api/settings")
async def api_get_settings(request: Request):
    user = await current_user(request)
    if user is None:
        return {"settings": {}}
    return {"settings": db.read_settings(user)}


@app.post("/api/settings")
async def api_save_settings(request: Request):
    """Store the client preferences (theme, gutter, guides) on the account.

    The browser is the source of truth while offline - localStorage is written
    first - so this only has to make the choice survive a new device.
    """
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    try:
        body = await request.json()
    except Exception:
        body = {}
    if not isinstance(body, dict):
        body = {}
    saved = await run_in_threadpool(db.save_settings, int(user["id"]), body)
    return {"settings": saved}


@app.get("/api/name-check")
async def api_name_check(request: Request, name: str = ""):
    """Live availability check for the profile dialog."""
    wanted = db.clean_name(name)
    if not wanted:
        return {"name": "", "ok": False, "reason": "empty", "suggestions": []}
    if not db.enabled():
        return {"name": wanted, "ok": True, "suggestions": []}

    user = await current_user(request)
    uid = int(user["id"]) if user else None
    taken = await run_in_threadpool(db.name_taken, wanted, uid)
    ideas = (
        await run_in_threadpool(db.name_suggestions, wanted, uid, 5) if taken else []
    )
    return {
        "name": wanted,
        "ok": not taken,
        "reason": "taken" if taken else "free",
        "suggestions": ideas,
    }


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


@app.post("/api/cover")
async def api_set_cover(request: Request, file: UploadFile = File(...)):
    """Upload the profile banner. Same shape as the avatar upload."""
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)

    data = await file.read(db.COVER_MAX_BYTES + 1)
    if not data:
        return JSONResponse({"error": "empty_file"}, status_code=400)
    if len(data) > db.COVER_MAX_BYTES:
        return JSONResponse({"error": "too_large", "max": db.COVER_MAX_BYTES}, status_code=413)

    mime = db.sniff_avatar(data)
    if mime is None:
        return JSONResponse({"error": "unsupported_type"}, status_code=415)

    version = await run_in_threadpool(db.set_cover, int(user["id"]), data, mime)
    return {"cover_version": version}


@app.delete("/api/cover")
async def api_clear_cover(request: Request):
    user = await current_user(request)
    if user is None:
        return JSONResponse({"error": "not_registered"}, status_code=401)
    await run_in_threadpool(db.clear_cover, int(user["id"]))
    return {"ok": True}


@app.get("/api/cover/{user_id}")
async def api_get_cover(user_id: int):
    """The banner, or 404 - a profile without one draws its own gradient."""
    found = await run_in_threadpool(db.get_cover, user_id) if db.enabled() else None
    if found is None:
        return Response(status_code=404)
    data, mime = found
    return Response(content=data, media_type=mime, headers=CACHE_WEEK)


@app.get("/api/avatar/{user_id}")
async def api_get_avatar(user_id: int):
    """The uploaded image, or a generated identicon so nobody is faceless."""
    found = await run_in_threadpool(db.get_avatar, user_id) if db.enabled() else None
    if found is not None:
        data, mime = found
        return Response(content=data, media_type=mime, headers=CACHE_WEEK)
    return Response(
        content=bots.avatar_svg("player-%d" % user_id),
        media_type="image/svg+xml",
        headers=CACHE_WEEK,
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

    length = max(1, int(float(body.get("length", 0) or 0)))
    errors = max(0, int(float(body.get("errors", 0) or 0)))
    # solo has nobody to beat, so there is no win bonus
    earned = rating.stars(acc, errors, length, bool(body.get("completed", True)), False)

    language = str(body.get("language", ""))[:20]
    level = str(body.get("level", ""))[:10]
    topic = str(body.get("topic", ""))[:24]

    await run_in_threadpool(
        db.record_race,
        int(user["id"]),
        language,
        level,
        topic,
        wpm,
        acc,
        seconds,
        None,
        None,
        client_ip(request),
        earned,
        0,  # solo has no opponent, so the rating does not move
    )
    try:
        post_id = await run_in_threadpool(
            social.add_post,
            int(user["id"]),
            language,
            level,
            topic,
            wpm,
            acc,
            seconds,
            None,
            earned,
            0,
            "",
            "",
            "solo",
        )
        snippets = body.get("snippets")
        if post_id and isinstance(body.get("replay"), list) and isinstance(snippets, list):
            await run_in_threadpool(
                db.save_replay,
                int(post_id),
                int(user["id"]),
                language,
                snippets,
                body.get("replay"),
                seconds,
            )
    except Exception as exc:
        log.warning("could not post solo run: %s", exc)
    try:
        fresh = await run_in_threadpool(achievements.award, int(user["id"]))
    except Exception as exc:
        log.warning("could not award achievements: %s", exc)
        fresh = []
    return {
        "ok": True,
        "stars": earned,
        "note": rating.star_note(earned),
        "awards": fresh,
    }


# ---------- websocket ----------
@app.websocket("/ws/user")
async def ws_user(websocket: WebSocket):
    """Per-account notification socket: invitations, presence, race invites.

    It carries no lobby traffic. A tab holds one of these open from the moment
    the account is known until it closes, which is also what marks the player
    online - so the Players list and the invitation badge are both live rather
    than polled.
    """
    await websocket.accept()

    account = None
    if db.enabled():
        token = websocket.cookies.get(COOKIE_NAME, "")
        if token:
            account = await run_in_threadpool(db.find_by_token, token)
    if account is None:
        await websocket.send_text(json.dumps({"t": "error", "code": "no_account"}))
        await websocket.close()
        return

    uid = int(account["id"])
    ip = client_ip(websocket)
    hub_add(uid, websocket)
    first = len(hub.get(uid) or ()) == 1
    mark_seen(uid, ip)

    await websocket.send_text(json.dumps({"t": "ready", "uid": uid, "name": account["name"]}))
    data = await run_in_threadpool(social.challenges_for, uid)
    await websocket.send_text(json.dumps({"t": "challenges", **data}))
    if first:
        await announce_presence()

    async def keepalive() -> None:
        """Hold last_seen_at fresh and keep an idle proxy from closing us."""
        try:
            while True:
                await asyncio.sleep(30)
                mark_seen(uid, ip)
                await websocket.send_text(json.dumps({"t": "ping"}))
        except (asyncio.CancelledError, Exception):
            return

    beat = asyncio.create_task(keepalive())
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            kind = msg.get("t")
            if kind == "pong":
                continue
            if kind == "challenges":
                data = await run_in_threadpool(social.challenges_for, uid)
                await websocket.send_text(json.dumps({"t": "challenges", **data}))
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        beat.cancel()
        hub_drop(uid, websocket)
        if uid not in hub:
            await announce_presence()


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
    spectate: int = Query(0),
    key: str = Query(""),
    private: int = Query(0),
    title: str = Query(""),
    strict: int = Query(0),
    ranked: int = Query(1),
    suggest: int = Query(0),
    limit: int = Query(0),
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
            parse_ids(topics, library.topic_ids()),
            None if duration < 0 else duration,
            private=bool(private),
            key=key,
            title=title,
            strict=bool(strict),
            ranked=bool(ranked),
            suggest=bool(suggest),
            limit=limit,
        )
        lobbies[code] = lobby
    elif lobby.key and lobby.key != key:
        # The code alone does not open a keyed lobby, however it was obtained.
        await websocket.send_text(json.dumps({"t": "error", "code": "bad_key"}))
        await websocket.close()
        return

    pid = pid or uuid.uuid4().hex[:12]
    if not spectate and lobby.full(pid):
        # Watching is still on the table, which is why this only blocks racers.
        await websocket.send_text(
            json.dumps({"t": "error", "code": "full", "limit": lobby.limit})
        )
        await websocket.close()
        return
    ip = client_ip(websocket)

    # A recognised player races under their saved profile name.
    account = None
    if db.enabled():
        token = websocket.cookies.get(COOKIE_NAME, "")
        if token:
            account = await run_in_threadpool(db.find_by_token, token)
    if account is not None:
        name = account["name"]
        mark_seen(int(account["id"]), ip)

    name = (name or "Guest").strip()[:18] or "Guest"
    taken = {p.name for p in lobby.players.values() if p.id != pid}
    taken |= {w.name for w in lobby.watchers.values() if w.id != pid}
    base, suffix = name, 2
    while name in taken:
        name = base + str(suffix)
        suffix += 1

    # ---- spectators ----
    # A watcher gets the same live feed as a racer and can talk in chat, but is
    # not in the roster, so nothing about the race or the scoring changes.
    if spectate:
        watcher = Player(pid, name, websocket)
        watcher.ip = ip
        if account is not None:
            watcher.uid = int(account["id"])
            watcher.avatar = (
                int(account.get("avatar_version") or 0) if account.get("avatar_mime") else 0
            )
        lobby.watchers[pid] = watcher
        await websocket.send_text(
            json.dumps(
                {
                    "t": "hello",
                    "id": pid,
                    "name": name,
                    "code": code,
                    "uid": watcher.uid,
                    "spectator": True,
                }
            )
        )
        for msg in lobby.chat[-40:]:
            await websocket.send_text(json.dumps(msg))
        await lobby.push_state()
        await lobby.system(name + " is watching")
        asyncio.create_task(announce_lobbies())
        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                # Chat is the only thing a spectator may send.
                if msg.get("t") != "chat":
                    continue
                text = str(msg.get("text", "")).strip()[:400]
                if not text:
                    continue
                out = {
                    "t": "chat",
                    "name": watcher.name,
                    "id": pid,
                    "uid": watcher.uid,
                    "avatar": watcher.avatar,
                    "text": text,
                    "watching": True,
                    "ts": time.time(),
                }
                lobby.chat.append(out)
                del lobby.chat[: -chat_limit()]
                await lobby.broadcast(out)
        except WebSocketDisconnect:
            pass
        except Exception:
            pass
        finally:
            lobby.watchers.pop(pid, None)
            if lobby.players or lobby.watchers or lobby.house:
                await lobby.system(name + " stopped watching")
                await lobby.push_state()
            else:
                lobby.cancel_task()
                lobbies.pop(code, None)
        return

    player = Player(pid, name, websocket)
    player.ip = ip
    if account is not None:
        player.uid = int(account["id"])
        player.avatar = int(account.get("avatar_version") or 0) if account.get("avatar_mime") else 0
        player.rating = int(account.get("rating") or rating.START_RATING)
    joined_late = lobby.state in ("racing", "countdown")
    if joined_late:
        # Straight into the race that is already running, rather than sitting
        # the round out. They start at the top of the snippet against a clock
        # that is already going, so they are behind - but watching a race you
        # walked into is not why anyone opens a lobby.
        player.ready = True
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
    await lobby.system(name + (" joined mid-race" if joined_late else " joined"))
    if joined_late and lobby.state == "racing":
        # tell them the race is already on, and where the clock is
        await websocket.send_text(
            json.dumps(
                {"t": "go", "start_ts": lobby.start_ts, "ends_at": lobby.ends_at}
            )
        )
    asyncio.create_task(announce_lobbies())
    asyncio.create_task(announce_presence())

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
                    lobby.level_lock = None
                    lobby.reroll()
                    await lobby.push_state()
                    await lobby.system("language set to " + value)

            elif kind == "filters":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                lobby.levels = clean_ids(msg.get("levels"), LEVEL_IDS)
                lobby.topics = clean_ids(msg.get("topics"), library.topic_ids())
                lobby.level_lock = None  # a new filter may mean a new level
                lobby.reroll()
                await lobby.push_state()
                await lobby.system(
                    "levels: %s · topics: %s"
                    % (
                        ", ".join(lobby.levels) or "any",
                        ", ".join(lobby.topics) or "any",
                    )
                )

            elif kind == "mode":
                # Strict typing and ranked/unranked. Both are settled before the
                # race starts, never during one.
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                if "strict" in msg:
                    lobby.strict = bool(msg.get("strict"))
                if "ranked" in msg:
                    lobby.ranked = bool(msg.get("ranked"))
                if "suggest" in msg:
                    lobby.suggest = bool(msg.get("suggest"))
                if "limit" in msg:
                    try:
                        lobby.limit = max(0, min(32, int(msg.get("limit") or 0)))
                    except (TypeError, ValueError):
                        pass
                await lobby.push_state()
                await lobby.system(
                    "%s · %s · %s"
                    % (
                        "strict typing" if lobby.strict else "indentation auto-skipped",
                        "suggestions on" if lobby.suggest else "no suggestions",
                        "ranked" if lobby.ranked else "unranked",
                    )
                )
                asyncio.create_task(announce_lobbies())

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

            elif kind == "bot":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                seated = lobby.add_bot(str(msg.get("v", "")))
                if seated is not None:
                    await lobby.system(
                        "%s (%d) joined" % (seated.name, seated.rating)
                    )
                    await lobby.push_state()

            elif kind == "unbot":
                if pid != lobby.host or lobby.state in ("countdown", "racing"):
                    continue
                if lobby.remove_bot(str(msg.get("v", ""))):
                    await lobby.push_state()

            elif kind == "start":
                if pid == lobby.host:
                    await lobby.start_race()

            elif kind == "again":
                # Swap in a different snippet and go back to the waiting room.
                if pid == lobby.host:
                    lobby.reroll(avoid=lobby.snip.get("code", ""))
                    await lobby.reset_to_lobby()
                    await lobby.system("new snippet loaded")

            elif kind == "restart":
                # Straight into another race on a different snippet.
                if pid == lobby.host and lobby.state in ("waiting", "finished"):
                    await lobby.start_race()

            elif kind == "replay":
                # The timeline on its own: sent when the clock ended the race
                # or the player gave up, so nothing else carried it.
                player.replay = db.clean_replay(msg.get("events"))
                await lobby.keep_replay(player)

            elif kind == "resign":
                # Give up: stop typing, hand the race to whoever is left.
                if isinstance(msg.get("replay"), list):
                    player.replay = db.clean_replay(msg.get("replay"))
                await lobby.resign(player)

            elif kind == "progress":
                if lobby.state != "racing" or player.finished:
                    continue
                player.progress = max(0.0, min(1.0, float(msg.get("p", 0))))
                player.wpm = max(0.0, float(msg.get("wpm", 0)))
                player.acc = max(0.0, min(100.0, float(msg.get("acc", 100))))
                player.pos = max(0, min(20000, int(msg.get("pos", 0))))
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
                        "pos": player.pos,
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
                if isinstance(msg.get("replay"), list):
                    player.replay = db.clean_replay(msg.get("replay"))
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
                # stars, Elo and the DB write all happen once, in score_race()
                await lobby.system(
                    "%s finished #%d at %.0f wpm" % (player.name, player.place, player.wpm)
                )
                lobby.arm_last_call()
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
        elif lobby.watchers:
            # nobody racing, but people are still watching: keep the room up
            lobby.cancel_task()
            lobby.state = "waiting"
            lobby.host = None
            await lobby.system(player.name + " left - no racers")
            await lobby.push_state()
        elif lobby.house:
            # the house keeps its rooms; reset it and leave it on the board
            lobby.cancel_task()
            lobby.state = "waiting"
            lobby.host = None
            lobby.order = []
            lobby.reroll()
        else:
            lobby.cancel_task()
            lobbies.pop(code, None)
        await announce_lobbies()
        await announce_presence()


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


# Files whose URL gets a build stamp, so a cached copy can never be paired with
# newer markup. Without this a stale app.js against a new index.html throws on
# the first element that no longer exists and the page dies.
VERSIONED = ("app.js", "style.css")


def asset_stamp() -> str:
    newest = 0.0
    for name in VERSIONED:
        try:
            newest = max(newest, (STATIC_DIR / name).stat().st_mtime)
        except OSError:
            pass
    return format(int(newest), "x")


def render_index() -> str:
    """index.html with {{SITE_URL}} and asset stamps filled in."""
    path = STATIC_DIR / "index.html"
    stamp = (path.stat().st_mtime, asset_stamp())
    if _index_cache["mtime"] != stamp:
        html = path.read_text(encoding="utf-8").replace("{{SITE_URL}}", SITE_URL)
        for name in VERSIONED:
            html = html.replace("/static/" + name, "/static/%s?v=%s" % (name, stamp[1]))
        _index_cache["html"] = html
        _index_cache["mtime"] = stamp
    return str(_index_cache["html"])


# ---------- pages ----------
# Every screen has a URL of its own. The same shell is served for all of them,
# but with that page's title, description and canonical written into <head>,
# so a crawler, a link preview and the browser tab all see the page it is - not
# "CodeRace" five times over. The client reads the path and opens the screen.
import html as _html

PAGES = {
    "/": (
        "CodeRace — type real code, race your friends",
        "A multiplayer typing game for real code. 15 languages, 4 difficulty levels, "
        "topic filters, timed races and bot opponents with ratings. Free, no install.",
    ),
    "/lobbies": (
        "Lobbies — CodeRace",
        "Open rooms you can join right now, public and private. Ten house lobbies are "
        "always up, in a different language and level each.",
    ),
    "/players": (
        "Find players — CodeRace",
        "Who is online now on CodeRace. Challenge anyone to a race and the invitation "
        "lands on their screen the moment you click.",
    ),
    "/feed": (
        "Race feed — CodeRace",
        "Every race as it happens: speed, accuracy, language and placing, with "
        "reactions, comments and watchable replays.",
    ),
    "/rankings": (
        "Rankings — CodeRace",
        "The rated ladder, from Rubber Duck to Kernel Hacker. Elo from real races "
        "between real players; bots and solo runs never move it.",
    ),
    "/awards": (
        "Achievements — CodeRace",
        "37 achievements across four tiers, and how rare each one is among the "
        "players who have raced.",
    ),
    "/snippets": (
        "Your snippets — CodeRace",
        "Add code of your own to the library. Public snippets join everyone's "
        "races; private ones stay yours.",
    ),
}


def _page_html(path: str, title: str, description: str, extra: str = "") -> str:
    """The shell with this page's <head> written in."""
    page = render_index()
    canon = SITE_URL + (path if path != "/" else "/")
    t = _html.escape(title, quote=True)
    d = _html.escape(description, quote=True)
    page = page.replace(
        "<title>CodeRace — type real code, race your friends</title>",
        "<title>%s</title>" % t,
        1,
    )
    page = page.replace(
        '<link rel="canonical" href="%s/" />' % SITE_URL,
        '<link rel="canonical" href="%s" />' % _html.escape(canon, quote=True),
        1,
    )
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        start = page.find(attr)
        if start < 0:
            continue
        c0 = page.find('content="', start) + len('content="')
        c1 = page.find('"', c0)
        page = page[:c0] + d + page[c1:]
    for attr in ('property="og:title"', 'name="twitter:title"'):
        start = page.find(attr)
        if start < 0:
            continue
        c0 = page.find('content="', start) + len('content="')
        c1 = page.find('"', c0)
        page = page[:c0] + t + page[c1:]
    page = page.replace(
        '<meta property="og:url" content="%s/" />' % SITE_URL,
        '<meta property="og:url" content="%s" />' % _html.escape(canon, quote=True),
        1,
    )
    if extra:
        page = page.replace("</head>", extra + "\n</head>", 1)
    return page


@app.get("/", response_class=HTMLResponse)
async def index():
    title, desc = PAGES["/"]
    return HTMLResponse(_page_html("/", title, desc))


@app.get("/lobbies", response_class=HTMLResponse)
@app.get("/players", response_class=HTMLResponse)
@app.get("/feed", response_class=HTMLResponse)
@app.get("/rankings", response_class=HTMLResponse)
@app.get("/awards", response_class=HTMLResponse)
@app.get("/snippets", response_class=HTMLResponse)
async def page(request: Request):
    path = request.url.path.rstrip("/") or "/"
    title, desc = PAGES.get(path, PAGES["/"])
    return HTMLResponse(_page_html(path, title, desc))


@app.get("/race/{code}", response_class=HTMLResponse)
async def race_page(code: str):
    """A lobby link. Ephemeral, so it asks not to be indexed."""
    title = "Lobby %s — CodeRace" % _html.escape(code.upper()[:8])
    desc = "Join this CodeRace lobby and race whoever is in it."
    return HTMLResponse(
        _page_html("/race/" + code.upper()[:8], title, desc,
                   '<meta name="robots" content="noindex" />')
    )


@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def profile_page(user_id: int):
    """A public profile, with enough written into the page for a crawler.

    The client fills the screen in, but a crawler - or a link preview - never
    runs it, so the name, rank and the three records go into the title, the
    description and a Person block a search engine can read as data.
    """
    prof = await run_in_threadpool(social.profile, user_id) if db.enabled() else None
    if prof is None:
        return HTMLResponse(
            _page_html("/profile/%d" % user_id, "Player not found — CodeRace",
                       "There is no CodeRace player with that id.",
                       '<meta name="robots" content="noindex" />'),
            status_code=404,
        )
    name = prof["name"]
    title = "%s — %s, %d rating — CodeRace" % (name, prof["rank"], prof["rating"])
    desc = "%s on CodeRace: %s at %d rating. Best %.0f wpm, %d wins in %d races." % (
        name, prof["rank"], prof["rating"], prof["best_wpm"], prof["wins"], prof["races"],
    )
    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "url": "%s/profile/%d" % (SITE_URL, user_id),
        "mainEntity": {
            "@type": "Person",
            "name": name,
            "identifier": str(user_id),
            "image": "%s/api/avatar/%d" % (SITE_URL, user_id),
            "description": desc,
        },
    })
    extra = '<script type="application/ld+json">%s</script>' % ld
    # a crawler that runs no script still sees the substance
    extra += (
        '<noscript><div style="padding:24px;font-family:sans-serif">'
        "<h1>%s</h1><p>%s</p>"
        "<p>Highest WPM: %.2f &middot; Games won: %d &middot; Games played: %d</p>"
        "</div></noscript>"
    ) % (_html.escape(name), _html.escape(desc), prof["best_wpm"], prof["wins"], prof["races"])
    return HTMLResponse(_page_html("/profile/%d" % user_id, title, desc, extra))


@app.get("/manifest.webmanifest")
async def manifest():
    return JSONResponse(
        {
            "name": "CodeRace - type real code",
            "short_name": "CodeRace",
            "description": "A multiplayer typing game for real code.",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "orientation": "any",
            "background_color": "#0d0f14",
            "theme_color": "#0d0f14",
            "categories": ["games", "education", "developer"],
            "icons": [
                {"src": "/static/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {
                    "src": "/static/icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable",
                },
                {"src": "/static/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            ],
        },
        media_type="application/manifest+json",
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        # lobby URLs are ephemeral and per-game; keep them out of the index
        "Disallow: /api/",
        "Disallow: /race/",
        "Disallow: /?l=",
        "",
        f"Sitemap: {SITE_URL}/sitemap.xml",
        "",
    ]
    return PlainTextResponse("\n".join(lines))


@app.get("/sitemap.xml")
async def sitemap():
    """Every page, plus the profile of everyone who has raced."""
    today = time.strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    def url(loc, freq, prio):
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ])

    url(SITE_URL + "/", "daily", "1.0")
    for path in ("/lobbies", "/players", "/feed", "/rankings", "/awards"):
        url(SITE_URL + path, "hourly" if path in ("/feed", "/lobbies") else "daily", "0.8")
    if db.enabled():
        try:
            rows = await run_in_threadpool(
                db.query,
                "SELECT id FROM cr_users WHERE races > 0 ORDER BY rating DESC LIMIT 5000",
            )
        except Exception:
            rows = []
        for r in rows:
            url("%s/profile/%d" % (SITE_URL, int(r["id"])), "weekly", "0.5")
    lines.extend(["</urlset>", ""])
    return Response(content="\n".join(lines), media_type="application/xml")


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
