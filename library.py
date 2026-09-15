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
) -> List[dict]:
    """Snippets matching the filters, falling back to the whole language."""
    library = all_snippets()
    pool = library.get(language) or library.get("python") or SNIPPETS["python"]
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
) -> dict:
    """A random snippet dict: {code, level, topic}."""
    pool = pool_for(language, levels_filter, topics_filter)
    options = [s for s in pool if s["code"] != avoid] or pool
    return random.choice(options)


def playlist(
    language: str,
    size: int,
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
) -> List[dict]:
    """An ordered run of snippets for a timed race.

    Every racer works through the same list, so the mode stays fair. The pool is
    shuffled and repeated when it is smaller than the requested length.
    """
    pool = pool_for(language, levels_filter, topics_filter)
    size = max(1, min(60, size))
    out: List[dict] = []
    while len(out) < size:
        batch = pool[:]
        random.shuffle(batch)
        out.extend(batch)
    return out[:size]


def count_matching(
    language: str,
    levels_filter: Optional[Iterable[str]] = None,
    topics_filter: Optional[Iterable[str]] = None,
) -> int:
    """How many snippets actually match - 0 means the filters fell back."""
    library = all_snippets()
    pool = library.get(language) or []
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
