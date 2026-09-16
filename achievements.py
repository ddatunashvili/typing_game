"""Achievements: what a player has earned, and how rare it is.

Two halves that deliberately stay apart:

* The catalogue below is pure data plus a predicate. It knows nothing about the
  database, so a new achievement is one entry and no migration.
* `award` writes the ones a player has just qualified for into `cr_awards`, and
  `board` reads them back with the share of players holding each. Earning is
  recorded rather than recomputed on read, so an achievement keeps the date it
  was earned even if the rule behind it later changes - and the rarity figure
  is one grouped query instead of one query per achievement.

Nothing here raises when the database is off; the callers already check.
"""
import logging
from typing import Any, Dict, List, Optional

import db
import rating

log = logging.getLogger("coderace.achievements")

# Tiers only drive the colour of the badge.
BRONZE, SILVER, GOLD, LEGEND = "bronze", "silver", "gold", "legend"


class Achievement:
    __slots__ = ("slug", "name", "blurb", "icon", "tier", "test", "goal")

    def __init__(self, slug, name, blurb, icon, tier, test, goal=None):
        self.slug = slug
        self.name = name
        self.blurb = blurb
        self.icon = icon
        self.tier = tier
        self.test = test          # (stats) -> bool
        self.goal = goal          # (stats) -> (have, want), for a progress bar

    def public(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "blurb": self.blurb,
            "icon": self.icon,
            "tier": self.tier,
        }


def _n(stats: Dict[str, Any], key: str) -> float:
    try:
        return float(stats.get(key) or 0)
    except (TypeError, ValueError):
        return 0.0


def _count(key: str, want: float):
    """A plain 'reach N of something' achievement, with its progress bar."""
    return (
        lambda s: _n(s, key) >= want,
        lambda s: (min(_n(s, key), want), want),
    )


def _milestones(prefix, name, blurb, icon, key, steps, tiers):
    """One achievement per step of a climbing target."""
    out = []
    for want, tier in zip(steps, tiers):
        test, goal = _count(key, want)
        # "1 races" reads like a bug, so the first step of a climbing target
        # gets its own wording.
        label = name % want
        if want == 1:
            label = "First " + name.split(" ", 1)[1].rstrip("s")
        out.append(
            Achievement(
                "%s-%d" % (prefix, want),
                label,
                blurb % want,
                icon,
                tier,
                test,
                goal,
            )
        )
    return out


CATALOGUE: List[Achievement] = []

CATALOGUE += _milestones(
    "races", "%d races", "Finish %d races.", "\U0001f3c1", "races",
    (1, 10, 50, 250, 1000), (BRONZE, BRONZE, SILVER, GOLD, LEGEND),
)
CATALOGUE += _milestones(
    "wins", "%d wins", "Win %d races.", "\U0001f3c6", "wins",
    (1, 10, 50, 250), (BRONZE, SILVER, GOLD, LEGEND),
)
CATALOGUE += _milestones(
    "wpm", "%d wpm", "Finish a race at %d wpm or better.", "⚡", "best_wpm",
    (40, 60, 80, 100, 130), (BRONZE, BRONZE, SILVER, GOLD, LEGEND),
)
CATALOGUE += _milestones(
    "stars", "%d stars", "Collect %d stars.", "⭐", "stars",
    (10, 100, 500), (BRONZE, SILVER, GOLD),
)

CATALOGUE += [
    Achievement(
        "flawless", "Flawless", "Finish a race at 100% accuracy.",
        "\U0001f48e", GOLD, lambda s: _n(s, "best_acc") >= 100,
    ),
    Achievement(
        "sharp", "Sharp", "Finish a race at 98% accuracy or better.",
        "\U0001f3af", SILVER, lambda s: _n(s, "best_acc") >= 98,
    ),
    Achievement(
        "perfect-run", "Perfect run", "Take three stars in a single race.",
        "✨", SILVER, lambda s: _n(s, "best_stars") >= 3,
    ),
    Achievement(
        "author", "Author", "Publish a snippet other people race on.",
        "✍️", SILVER, lambda s: _n(s, "snippets") >= 1,
    ),
    Achievement(
        "librarian", "Librarian", "Publish ten snippets.",
        "\U0001f4da", GOLD, lambda s: _n(s, "snippets") >= 10,
        lambda s: (min(_n(s, "snippets"), 10), 10),
    ),
    Achievement(
        "polyglot", "Polyglot", "Race in five different languages.",
        "\U0001f30d", SILVER, lambda s: _n(s, "languages") >= 5,
        lambda s: (min(_n(s, "languages"), 5), 5),
    ),
    Achievement(
        "hyperglot", "Hyperglot", "Race in ten different languages.",
        "\U0001f5fa️", GOLD, lambda s: _n(s, "languages") >= 10,
        lambda s: (min(_n(s, "languages"), 10), 10),
    ),
    Achievement(
        "hard-way", "The hard way", "Win a race on a hard snippet.",
        "\U0001f5e1️", GOLD, lambda s: bool(s.get("won_hard")),
    ),
    Achievement(
        "giant-killer", "Giant killer",
        "Beat someone rated 200 points above you.",
        "\U0001f3f9", GOLD, lambda s: bool(s.get("beat_better")),
    ),
    Achievement(
        "streak-3", "On a roll", "Win three races in a row.",
        "\U0001f525", SILVER, lambda s: _n(s, "streak") >= 3,
        lambda s: (min(_n(s, "streak"), 3), 3),
    ),
    Achievement(
        "streak-10", "Unstoppable", "Win ten races in a row.",
        "☄️", LEGEND, lambda s: _n(s, "streak") >= 10,
        lambda s: (min(_n(s, "streak"), 10), 10),
    ),
    Achievement(
        "night-owl", "Night owl", "Finish a race between 2am and 5am.",
        "\U0001f989", BRONZE, lambda s: bool(s.get("night_owl")),
    ),
    Achievement(
        "social", "Sociable", "Race against five different people.",
        "\U0001f91d", SILVER, lambda s: _n(s, "rivals") >= 5,
        lambda s: (min(_n(s, "rivals"), 5), 5),
    ),
]

# Rank achievements, one per band above the starting rating.
for _floor, _title in rating.RANKS:
    if _floor <= rating.START_RATING:
        continue
    _tier = LEGEND if _floor >= 2100 else GOLD if _floor >= 1650 else SILVER
    CATALOGUE.append(
        Achievement(
            "rank-%d" % _floor,
            _title,
            "Reach %d rating." % _floor,
            "\U0001f396️",
            _tier,
            (lambda floor: lambda s: _n(s, "rating") >= floor)(_floor),
            (lambda floor: lambda s: (min(_n(s, "rating"), floor), floor))(_floor),
        )
    )

BY_SLUG = {a.slug: a for a in CATALOGUE}


def stats_for(user_id: int) -> Dict[str, Any]:
    """Everything the predicates need, in as few round trips as it takes.

    Most of it is already on the user row. The rest is one pass over that
    player's race history, which is small and indexed by user.
    """
    row = db.one(
        "SELECT id, races, wins, best_wpm, best_acc, rating, stars FROM cr_users "
        "WHERE id = %s",
        (user_id,),
    )
    if row is None:
        return {}
    stats: Dict[str, Any] = {
        "races": int(row.get("races") or 0),
        "wins": int(row.get("wins") or 0),
        "best_wpm": float(row.get("best_wpm") or 0),
        "best_acc": float(row.get("best_acc") or 0),
        "rating": int(row.get("rating") or rating.START_RATING),
        "stars": int(row.get("stars") or 0),
    }

    extra = db.one(
        "SELECT COUNT(DISTINCT language) AS languages, "
        "COALESCE(MAX(stars), 0) AS best_stars, "
        "SUM(place = 1 AND level = 'hard') AS won_hard, "
        "SUM(HOUR(created_at) BETWEEN 2 AND 4) AS night_owl "
        "FROM cr_races WHERE user_id = %s",
        (user_id,),
    ) or {}
    stats["languages"] = int(extra.get("languages") or 0)
    stats["best_stars"] = int(extra.get("best_stars") or 0)
    stats["won_hard"] = bool(extra.get("won_hard") or 0)
    stats["night_owl"] = bool(extra.get("night_owl") or 0)

    counted = db.one(
        "SELECT COUNT(*) AS n FROM cr_snippets WHERE author_id = %s", (user_id,)
    ) or {}
    stats["snippets"] = int(counted.get("n") or 0)

    # Longest run of wins, walked over the most recent races only - a streak
    # further back than this is not something anybody is still chasing.
    places = [
        r["place"]
        for r in db.query(
            "SELECT place FROM cr_races WHERE user_id = %s ORDER BY id DESC LIMIT 200",
            (user_id,),
        )
    ]
    best = run = 0
    for place in places:
        if place == 1:
            run += 1
            best = max(best, run)
        else:
            run = 0
    stats["streak"] = best
    return stats


def award(user_id: int, extra: Optional[Dict[str, Any]] = None) -> List[dict]:
    """Record anything this player now qualifies for. Returns what was new."""
    if not db.enabled():
        return []
    try:
        stats = stats_for(user_id)
    except Exception as exc:
        log.warning("could not read achievement stats for %s: %s", user_id, exc)
        return []
    if not stats:
        return []
    if extra:
        stats.update(extra)

    held = {
        r["slug"]
        for r in db.query("SELECT slug FROM cr_awards WHERE user_id = %s", (user_id,))
    }
    fresh = []
    for item in CATALOGUE:
        if item.slug in held:
            continue
        try:
            if not item.test(stats):
                continue
        except Exception:
            continue
        try:
            # INSERT IGNORE: two races closing at once must not collide on the
            # unique key and lose the whole batch.
            db.execute(
                "INSERT IGNORE INTO cr_awards (user_id, slug) VALUES (%s, %s)",
                (user_id, item.slug),
            )
        except Exception as exc:
            log.warning("could not award %s to %s: %s", item.slug, user_id, exc)
            continue
        fresh.append(item.public())
    return fresh


def holders() -> Dict[str, int]:
    rows = db.query("SELECT slug, COUNT(*) AS n FROM cr_awards GROUP BY slug")
    return {r["slug"]: int(r["n"]) for r in rows}


def board(user_id: Optional[int] = None) -> dict:
    """The whole catalogue, marked with what this player holds and how rare it is.

    `share` is the percentage of players who have ever raced that hold it, so a
    player who signed up and never played does not drag every number down.
    """
    if not db.enabled():
        return {"achievements": [], "earned": 0, "total": len(CATALOGUE), "players": 0}

    counts = holders()
    total_players = int(
        (db.one("SELECT COUNT(*) AS n FROM cr_users WHERE races > 0") or {}).get("n") or 0
    )

    mine: Dict[str, str] = {}
    stats: Dict[str, Any] = {}
    if user_id:
        mine = {
            r["slug"]: str(r.get("earned_at") or "")
            for r in db.query(
                "SELECT slug, earned_at FROM cr_awards WHERE user_id = %s", (user_id,)
            )
        }
        try:
            stats = stats_for(user_id)
        except Exception:
            stats = {}

    out = []
    for item in CATALOGUE:
        row = item.public()
        held = int(counts.get(item.slug) or 0)
        row["holders"] = held
        row["share"] = round(100.0 * held / total_players, 1) if total_players else 0.0
        row["earned"] = item.slug in mine
        row["earned_at"] = mine.get(item.slug, "")
        row["have"] = row["want"] = 0
        if not row["earned"] and stats and item.goal:
            try:
                have, want = item.goal(stats)
                row["have"], row["want"] = round(float(have), 1), round(float(want), 1)
            except Exception:
                pass
        out.append(row)

    return {
        "achievements": out,
        "earned": sum(1 for r in out if r["earned"]),
        "total": len(out),
        "players": total_players,
    }


def for_user(user_id: int, limit: int = 0) -> List[dict]:
    """Just the earned ones, rarest first - the badges shown on a profile."""
    if not db.enabled() or not user_id:
        return []
    counts = holders()
    rows = db.query(
        "SELECT slug, earned_at FROM cr_awards WHERE user_id = %s", (user_id,)
    )
    out = []
    for r in rows:
        item = BY_SLUG.get(r["slug"])
        if item is None:
            continue  # an achievement that has since been retired
        shown = item.public()
        shown["earned_at"] = str(r.get("earned_at") or "")
        shown["holders"] = int(counts.get(item.slug) or 0)
        out.append(shown)
    out.sort(key=lambda r: r["holders"])
    return out[:limit] if limit else out
