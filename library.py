"""Snippet library and settings, read from MySQL with the seed file as fallback.

`snippets.py` holds the seed data. On startup it is pushed into `cr_snippets`
(idempotently, keyed by a content hash) and everything afterwards reads from the
database, so snippets and settings can be edited with SQL without a redeploy.
With no database configured the seed data is used directly and the game still
works, just without live editing.
"""
import logging
import os
import random
import time
from typing import Dict, Iterable, List, Optional, Sequence

import db
from snippets import (
    LANGUAGES,
    LEVEL_IDS,
    LEVELS,
    SNIPPETS,
    TOPIC_IDS,
    TOPICS,
    clean_ids,
    languages,
    levels,
    parse_ids,
    topics,
)

log = logging.getLogger("coderace.library")

# How long a cached copy of the library/settings is trusted before a re-read.
# Edits made straight in SQL therefore show up within this many seconds.
try:
    REFRESH_SECONDS = max(1, int(os.environ.get("LIBRARY_REFRESH_SECONDS", "60") or 60))
except ValueError:
    REFRESH_SECONDS = 60

# Settings that live in cr_config, with the env-derived default written on seed.
SETTING_DEFAULTS = {
    "countdown_seconds": "5",
    "chat_history": "100",
    "race_seconds": "0",  # 0 = classic: the race ends when the snippet is done
    "playlist_size": "12",
}

_cache: Dict[str, object] = {"snippets": None, "config": {}, "at": 0.0}


def _env_default(name: str, fallback: str) -> str:
    """cr_config is seeded from the environment, so .env still sets the defaults."""
    return os.environ.get(name.upper(), "").strip() or fallback


def seed() -> None:
    """Push the seed snippets and default settings into the database."""
    if not db.enabled():
        return
    try:
        added = db.seed_snippets(SNIPPETS)
        defaults = {k: _env_default(k, v) for k, v in SETTING_DEFAULTS.items()}
        db.seed_config(defaults)
        log.info(
            "library seeded: %d new snippet(s), %d active in total",
            added,
            db.snippet_count(),
        )
    except Exception as exc:
        log.warning("could not seed the library: %s", exc)


def refresh(force: bool = False) -> None:
    """Re-read the library and settings if the cache is stale."""
    if not db.enabled():
        _cache["snippets"] = None
        return
    fresh_enough = (time.time() - float(_cache["at"] or 0)) < REFRESH_SECONDS
    if not force and _cache["snippets"] is not None and fresh_enough:
        return
    try:
        pool = db.load_snippets()
        if pool:
            _cache["snippets"] = pool
        _cache["config"] = db.load_config()
        _cache["at"] = time.time()
    except Exception as exc:
        log.warning("library refresh failed, using the last copy: %s", exc)


def all_snippets() -> Dict[str, List[dict]]:
    """The active library: database copy when available, seed file otherwise."""
    refresh()
    cached = _cache.get("snippets")
    if cached:
        return cached  # type: ignore[return-value]
    return SNIPPETS


# ---------- settings ----------
def setting(name: str, default: str = "") -> str:
    refresh()
    config = _cache.get("config") or {}
    value = config.get(name)  # type: ignore[union-attr]
    if value is None or value == "":
        return _env_default(name, default or SETTING_DEFAULTS.get(name, ""))
    return str(value)


def setting_int(name: str, default: int) -> int:
    try:
        return int(float(setting(name, str(default))))
    except (TypeError, ValueError):
        return default


def settings() -> Dict[str, str]:
    """Every known setting with its effective value."""
    return {name: setting(name, fallback) for name, fallback in SETTING_DEFAULTS.items()}


# ---------- picking ----------
def pool_for(
    language: str,
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
    level: Optional[str] = None,
) -> List[dict]:
    """Snippets matching the filters, falling back to the whole language.

    `level` pins one exact level, which is how a race keeps handing out
    snippets of the same difficulty.
    """
    library = all_snippets()
    pool = library.get(language) or library.get("python") or SNIPPETS["python"]
    if level:
        levels_filter = [level]
    wanted_levels = set(clean_ids(levels_filter, LEVEL_IDS))
    wanted_topics = set(clean_ids(topics_filter, TOPIC_IDS))
    matches = [
        s
        for s in pool
        if (not wanted_levels or s["level"] in wanted_levels)
        and (not wanted_topics or s["topic"] in wanted_topics)
    ]
    return matches or pool


def pick_snippet(
    language: str,
    avoid: str = "",
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
    level: Optional[str] = None,
) -> dict:
    """A random snippet dict: {code, level, topic}."""
    pool = pool_for(language, levels_filter, topics_filter, level)
    options = [s for s in pool if s["code"] != avoid] or pool
    return random.choice(options)


class Bag:
    """Deals snippets without repeats: shuffle, deal one at a time, reshuffle.

    A plain random pick can show the same snippet twice in a row; this walks a
    shuffled deck instead, so every snippet in the pool comes up once before any
    of them repeats.
    """

    def __init__(self) -> None:
        self._queue: List[dict] = []
        self._key: Optional[tuple] = None
        self._last: Optional[str] = None

    def deal(
        self,
        language: str,
        levels_filter: Optional[Iterable[str]] = None,
        topics_filter: Optional[Iterable[str]] = None,
        level: Optional[str] = None,
    ) -> dict:
        key = (
            language,
            tuple(clean_ids(levels_filter, LEVEL_IDS)),
            tuple(clean_ids(topics_filter, TOPIC_IDS)),
            level or "",
        )
        if key != self._key or not self._queue:
            pool = pool_for(language, levels_filter, topics_filter, level)
            self._queue = pool[:]
            random.shuffle(self._queue)
            self._key = key
            # avoid dealing the same snippet twice across a reshuffle
            if len(self._queue) > 1 and self._queue[-1]["code"] == self._last:
                self._queue.insert(0, self._queue.pop())
        item = self._queue.pop()
        self._last = item["code"]
        return item


def playlist(
    language: str,
    size: int,
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
    level: Optional[str] = None,
    unique: bool = False,
) -> List[dict]:
    """An ordered run of snippets for a timed race.

    Every racer works through the same list, so the mode stays fair. Each pass is
    a fresh shuffle, and a pass never starts with the snippet the previous one
    ended on, so nothing repeats back to back.

    `unique=True` caps the run at one pass, i.e. no snippet twice at all.
    """
    pool = pool_for(language, levels_filter, topics_filter, level)
    if not pool:
        return []
    size = max(1, min(400, size))
    if unique:
        size = min(size, len(pool))

    out: List[dict] = []
    while len(out) < size:
        batch = pool[:]
        random.shuffle(batch)
        if out and len(batch) > 1 and batch[0]["code"] == out[-1]["code"]:
            batch.append(batch.pop(0))  # don't repeat across the seam
        out.extend(batch)
    return out[:size]


def count_matching(
    language: str,
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
    level: Optional[str] = None,
) -> int:
    """How many snippets actually match - 0 means the filters fell back."""
    library = all_snippets()
    pool = library.get(language) or []
    if level:
        levels_filter = [level]
    wanted_levels = set(clean_ids(levels_filter, LEVEL_IDS))
    wanted_topics = set(clean_ids(topics_filter, TOPIC_IDS))
    return sum(
        1
        for s in pool
        if (not wanted_levels or s["level"] in wanted_levels)
        and (not wanted_topics or s["topic"] in wanted_topics)
    )


def catalog() -> List[dict]:
    """Per-language counts by level, topic and level x topic, for the picker."""
    library = all_snippets()
    out = []
    for lid, label in LANGUAGES:
        pool = library.get(lid, [])
        by_level = {level: 0 for level in LEVEL_IDS}
        by_topic = {topic: 0 for topic in TOPIC_IDS}
        combos: Dict[str, int] = {}
        for s in pool:
            if s["level"] in by_level:
                by_level[s["level"]] += 1
            if s["topic"] in by_topic:
                by_topic[s["topic"]] += 1
            key = s["level"] + "|" + s["topic"]
            combos[key] = combos.get(key, 0) + 1
        out.append(
            {
                "id": lid,
                "label": label,
                "total": len(pool),
                "levels": by_level,
                "topics": {t: n for t, n in by_topic.items() if n},
                "combos": combos,
            }
        )
    return out


def source() -> str:
    return "database" if _cache.get("snippets") else "seed file"
