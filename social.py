"""The social layer: player-submitted snippets, profiles, a race feed,
reactions, comments, reports and challenges.

Everything here is read/write against MySQL through `db`, and every function is
safe to call when no database is configured - the callers check `db.enabled()`
first, and the listing helpers return empty results rather than raising.

Moderation is deliberately simple and mechanical: there is no admin account, so
content hides itself once `AUTO_HIDE_AT` distinct players report it, and both
comments and submissions are rate limited per account.
"""
from typing import Any, Dict, List, Optional

import db
import rating

# ---------- limits ----------
SNIPPETS_PER_DAY = 20
COMMENTS_PER_HOUR = 30
AUTO_HIDE_AT = 3
MAX_BODY = 500
MAX_NOTE = 300

REPORT_REASONS = ("cheating", "spam", "abuse", "broken-snippet", "other")
REPORT_KINDS = ("post", "comment", "snippet", "user")


# ---------- custom topics ----------
def topic_slug(label: str) -> str:
    """A url-safe slug for a player-created topic."""
    out: List[str] = []
    for ch in (label or "").strip().lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")[:24]


def add_topic(label: str, created_by: Optional[int]) -> Optional[dict]:
    """Create a topic, or return the existing one. None means a bad label."""
    slug = topic_slug(label)
    if len(slug) < 2:
        return None
    clean = (label or "").strip()[:40]
    db.execute(
        "INSERT INTO cr_topics (slug, label, created_by) VALUES (%s, %s, %s) "
        "ON DUPLICATE KEY UPDATE label = label",
        (slug, clean, created_by),
    )
    return {"id": slug, "label": clean, "custom": True}


def custom_topics() -> List[dict]:
    if not db.enabled():
        return []
    rows = db.query("SELECT slug, label FROM cr_topics ORDER BY label")
    return [{"id": r["slug"], "label": r["label"], "custom": True} for r in rows]


# ---------- player-submitted snippets ----------
def snippets_today(user_id: int) -> int:
    row = db.one(
        "SELECT COUNT(*) AS n FROM cr_snippets "
        "WHERE author_id = %s AND created_at >= CURRENT_DATE",
        (user_id,),
    )
    return int((row or {}).get("n") or 0)


def submit_snippet(
    author_id: int,
    language: str,
    level: str,
    topic: str,
    code: str,
    output: str = "",
    public: bool = True,
) -> Optional[int]:
    """Store a player's snippet. None means an identical one already exists."""
    rowid = db.execute(
        "INSERT IGNORE INTO cr_snippets "
        "(language, level, topic, code, output, code_hash, source, author_id, status) "
        "VALUES (%s, %s, %s, %s, %s, %s, 'user', %s, %s)",
        (
            language[:20],
            level[:10],
            topic[:24],
            code,
            output or None,
            db.code_hash(language, code),
            author_id,
            "public" if public else "private",
        ),
    )
    return int(rowid) if rowid else None


def my_snippets(user_id: int, limit: int = 100) -> List[dict]:
    rows = db.query(
        "SELECT id, language, level, topic, code, output, status, active, reports, "
        "created_at FROM cr_snippets WHERE author_id = %s "
        "ORDER BY created_at DESC LIMIT %s",
        (user_id, max(1, min(200, limit))),
    )
    for row in rows:
        row["id"] = int(row["id"])
        row["active"] = bool(row.get("active"))
        row["reports"] = int(row.get("reports") or 0)
        row["created_at"] = str(row.get("created_at") or "")
    return rows


def set_snippet_status(snippet_id: int, author_id: int, public: bool) -> bool:
    return bool(
        db.execute(
            "UPDATE cr_snippets SET status = %s WHERE id = %s AND author_id = %s",
            ("public" if public else "private", snippet_id, author_id),
        )
    )


def delete_snippet(snippet_id: int, author_id: int) -> bool:
    return bool(
        db.execute(
            "DELETE FROM cr_snippets WHERE id = %s AND author_id = %s",
            (snippet_id, author_id),
        )
    )


def snippet_author(snippet_id: int) -> Optional[int]:
    row = db.one("SELECT author_id FROM cr_snippets WHERE id = %s", (snippet_id,))
    author = (row or {}).get("author_id")
    return int(author) if author else None


# ---------- posts ----------
POST_COLUMNS = (
    "p.id, p.user_id, p.kind, p.language, p.level, p.topic, p.wpm, p.acc, "
    "p.seconds, p.place, p.stars, p.rating_delta, p.opponents, p.body, "
    "p.likes, p.dislikes, p.comment_count, p.created_at, "
    "u.name AS author_name, u.avatar_mime, u.avatar_version, "
    "u.rating AS author_rating"
)


def public_post(row: dict, viewer_id: Optional[int] = None) -> dict:
    score = int(row.get("author_rating") or rating.START_RATING)
    return {
        "id": int(row["id"]),
        "user": {
            "id": int(row["user_id"]),
            "name": row.get("author_name") or "player",
            "avatar": int(row.get("avatar_version") or 0) if row.get("avatar_mime") else 0,
            "rating": score,
            "rank": rating.rank_for(score),
        },
        "kind": row.get("kind") or "race",
        "language": row.get("language"),
        "level": row.get("level"),
        "topic": row.get("topic"),
        "wpm": float(row.get("wpm") or 0),
        "acc": float(row.get("acc") or 0),
        "seconds": float(row.get("seconds") or 0),
        "place": row.get("place"),
        "stars": int(row.get("stars") or 0),
        "delta": int(row.get("rating_delta") or 0),
        "opponents": row.get("opponents") or "",
        "body": row.get("body") or "",
        "likes": int(row.get("likes") or 0),
        "dislikes": int(row.get("dislikes") or 0),
        "comments": int(row.get("comment_count") or 0),
        "mine": viewer_id is not None and int(row["user_id"]) == viewer_id,
        "my_reaction": int(row.get("my_reaction") or 0),
        "created_at": str(row.get("created_at") or ""),
    }


def add_post(
    user_id: int,
    language: str = "",
    level: str = "",
    topic: str = "",
    wpm: float = 0.0,
    acc: float = 0.0,
    seconds: float = 0.0,
    place: Optional[int] = None,
    stars: int = 0,
    rating_delta: int = 0,
    opponents: str = "",
    body: str = "",
    kind: str = "race",
) -> int:
    """Write a finished race (or a note) onto the player's profile."""
    return int(
        db.execute(
            "INSERT INTO cr_posts (user_id, kind, language, level, topic, wpm, acc, "
            "seconds, place, stars, rating_delta, opponents, body) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                user_id,
                kind[:16],
                (language or "")[:20],
                (level or "")[:10],
                (topic or "")[:24],
                round(float(wpm), 1),
                round(float(acc), 1),
                round(float(seconds), 2),
                place,
                max(0, min(3, int(stars))),
                int(rating_delta),
                (opponents or "")[:255],
                (body or "").strip()[:MAX_BODY],
            ),
        )
    )


def feed(
    limit: int = 30,
    before: Optional[int] = None,
    user_id: Optional[int] = None,
    viewer_id: Optional[int] = None,
) -> List[dict]:
    """Newest posts, globally or for a single player."""
    where = ["p.hidden = 0"]
    args: List[Any] = []

    reaction = "0 AS my_reaction"
    if viewer_id is not None:
        reaction = (
            "COALESCE((SELECT value FROM cr_reactions "
            "WHERE post_id = p.id AND user_id = %s), 0) AS my_reaction"
        )
        args.append(viewer_id)

    if user_id is not None:
        where.append("p.user_id = %s")
        args.append(user_id)
    if before:
        where.append("p.id < %s")
        args.append(before)

    args.append(max(1, min(100, limit)))
    sql = (
        "SELECT " + POST_COLUMNS + ", " + reaction + " FROM cr_posts AS p "
        "JOIN cr_users AS u ON u.id = p.user_id "
        "WHERE " + " AND ".join(where) + " ORDER BY p.id DESC LIMIT %s"
    )
    return [public_post(row, viewer_id) for row in db.query(sql, args)]


def get_post(post_id: int, viewer_id: Optional[int] = None) -> Optional[dict]:
    args: List[Any] = []
    reaction = "0 AS my_reaction"
    if viewer_id is not None:
        reaction = (
            "COALESCE((SELECT value FROM cr_reactions "
            "WHERE post_id = p.id AND user_id = %s), 0) AS my_reaction"
        )
        args.append(viewer_id)
    args.append(post_id)
    row = db.one(
        "SELECT " + POST_COLUMNS + ", " + reaction + " FROM cr_posts AS p "
        "JOIN cr_users AS u ON u.id = p.user_id WHERE p.id = %s AND p.hidden = 0",
        args,
    )
    return public_post(row, viewer_id) if row else None


def delete_post(post_id: int, user_id: int) -> bool:
    return bool(
        db.execute(
            "DELETE FROM cr_posts WHERE id = %s AND user_id = %s", (post_id, user_id)
        )
    )


# ---------- reactions ----------
def react(post_id: int, user_id: int, value: int) -> dict:
    """Set, flip or clear a like/dislike. Returns the fresh counts."""
    value = 1 if value > 0 else (-1 if value < 0 else 0)
    if value == 0:
        db.execute(
            "DELETE FROM cr_reactions WHERE post_id = %s AND user_id = %s",
            (post_id, user_id),
        )
    else:
        db.execute(
            "INSERT INTO cr_reactions (post_id, user_id, value) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE value = VALUES(value)",
            (post_id, user_id, value),
        )

    counts = db.one(
        "SELECT COALESCE(SUM(value = 1), 0) AS likes, "
        "COALESCE(SUM(value = -1), 0) AS dislikes "
        "FROM cr_reactions WHERE post_id = %s",
        (post_id,),
    ) or {}
    likes = int(counts.get("likes") or 0)
    dislikes = int(counts.get("dislikes") or 0)
    db.execute(
        "UPDATE cr_posts SET likes = %s, dislikes = %s WHERE id = %s",
        (likes, dislikes, post_id),
    )
    return {"likes": likes, "dislikes": dislikes, "my_reaction": value}


# ---------- comments ----------
def comments_last_hour(user_id: int) -> int:
    row = db.one(
        "SELECT COUNT(*) AS n FROM cr_comments "
        "WHERE user_id = %s AND created_at >= NOW() - INTERVAL 1 HOUR",
        (user_id,),
    )
    return int((row or {}).get("n") or 0)


def _recount_comments(post_id: int) -> None:
    db.execute(
        "UPDATE cr_posts SET comment_count = "
        "(SELECT COUNT(*) FROM cr_comments WHERE post_id = %s AND hidden = 0) "
        "WHERE id = %s",
        (post_id, post_id),
    )


def add_comment(post_id: int, user_id: int, body: str) -> Optional[int]:
    body = (body or "").strip()[:MAX_BODY]
    if not body:
        return None
    rowid = db.execute(
        "INSERT INTO cr_comments (post_id, user_id, body) VALUES (%s, %s, %s)",
        (post_id, user_id, body),
    )
    _recount_comments(post_id)
    return int(rowid)


def comments(post_id: int, limit: int = 50) -> List[dict]:
    rows = db.query(
        "SELECT c.id, c.user_id, c.body, c.created_at, "
        "u.name, u.avatar_mime, u.avatar_version, u.rating "
        "FROM cr_comments AS c JOIN cr_users AS u ON u.id = c.user_id "
        "WHERE c.post_id = %s AND c.hidden = 0 ORDER BY c.id ASC LIMIT %s",
        (post_id, max(1, min(200, limit))),
    )
    out = []
    for row in rows:
        score = int(row.get("rating") or rating.START_RATING)
        out.append(
            {
                "id": int(row["id"]),
                "body": row["body"],
                "created_at": str(row["created_at"]),
                "user": {
                    "id": int(row["user_id"]),
                    "name": row["name"],
                    "avatar": int(row.get("avatar_version") or 0)
                    if row.get("avatar_mime")
                    else 0,
                    "rating": score,
                    "rank": rating.rank_for(score),
                },
            }
        )
    return out


def delete_comment(comment_id: int, user_id: int) -> bool:
    row = db.one(
        "SELECT post_id FROM cr_comments WHERE id = %s AND user_id = %s",
        (comment_id, user_id),
    )
    if row is None:
        return False
    db.execute("DELETE FROM cr_comments WHERE id = %s", (comment_id,))
    _recount_comments(int(row["post_id"]))
    return True


# ---------- reports ----------
def add_report(
    kind: str,
    target_id: int,
    reporter_id: int,
    reason: str,
    note: str = "",
    ip: str = "",
) -> dict:
    """File a report. Three distinct reporters hide the target automatically."""
    if kind not in REPORT_KINDS:
        kind = "post"
    if reason not in REPORT_REASONS:
        reason = "other"

    db.execute(
        "INSERT IGNORE INTO cr_reports "
        "(kind, target_id, reporter_id, reason, note, ip) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            kind,
            target_id,
            reporter_id,
            reason,
            (note or "").strip()[:MAX_NOTE] or None,
            (ip or None) and ip[:45],
        ),
    )
    row = db.one(
        "SELECT COUNT(*) AS n FROM cr_reports WHERE kind = %s AND target_id = %s",
        (kind, target_id),
    )
    total = int((row or {}).get("n") or 0)

    hidden = False
    if total >= AUTO_HIDE_AT:
        if kind == "post":
            db.execute("UPDATE cr_posts SET hidden = 1 WHERE id = %s", (target_id,))
            hidden = True
        elif kind == "comment":
            db.execute("UPDATE cr_comments SET hidden = 1 WHERE id = %s", (target_id,))
            hidden = True
        elif kind == "snippet":
            db.execute("UPDATE cr_snippets SET active = 0 WHERE id = %s", (target_id,))
            hidden = True
    if kind == "snippet":
        db.execute(
            "UPDATE cr_snippets SET reports = %s WHERE id = %s", (total, target_id)
        )
    return {"reports": total, "hidden": hidden, "threshold": AUTO_HIDE_AT}


# ---------- profiles and presence ----------
def _idle_seconds(row: dict) -> int:
    """Seconds since the player was last seen. 0 is valid, so no `or`."""
    value = row.get("idle")
    return 10 ** 9 if value is None else int(value)


def profile(user_id: int) -> Optional[dict]:
    row = db.one(
        "SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc, "
        "rating, wins, stars, created_at, last_seen_at, "
        "TIMESTAMPDIFF(SECOND, last_seen_at, NOW()) AS idle "
        "FROM cr_users WHERE id = %s",
        (user_id,),
    )
    if row is None:
        return None

    out = db.public_user(row)
    idle = _idle_seconds(row)
    out["joined"] = str(row.get("created_at") or "")
    out["idle"] = idle
    out["online"] = idle <= 300

    extra = db.one(
        "SELECT COUNT(*) AS races, COALESCE(AVG(wpm), 0) AS avg_wpm, "
        "COALESCE(AVG(acc), 0) AS avg_acc FROM cr_races WHERE user_id = %s",
        (user_id,),
    ) or {}
    out["avg_wpm"] = round(float(extra.get("avg_wpm") or 0), 1)
    out["avg_acc"] = round(float(extra.get("avg_acc") or 0), 1)

    counted = db.one(
        "SELECT COUNT(*) AS n FROM cr_snippets WHERE author_id = %s", (user_id,)
    ) or {}
    out["snippets"] = int(counted.get("n") or 0)

    out["by_language"] = [
        {
            "language": r["language"],
            "races": int(r["races"]),
            "best": float(r["best"] or 0),
        }
        for r in db.query(
            "SELECT language, COUNT(*) AS races, ROUND(MAX(wpm), 1) AS best "
            "FROM cr_races WHERE user_id = %s GROUP BY language "
            "ORDER BY races DESC LIMIT 8",
            (user_id,),
        )
    ]
    return out


def players(limit: int = 40, online_within: int = 300) -> List[dict]:
    """Recently active players, freshest first, for the find-players page."""
    rows = db.query(
        "SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc, "
        "rating, wins, stars, "
        "TIMESTAMPDIFF(SECOND, last_seen_at, NOW()) AS idle "
        "FROM cr_users ORDER BY last_seen_at DESC LIMIT %s",
        (max(1, min(100, limit)),),
    )
    out = []
    for row in rows:
        item = db.public_user(row)
        idle = _idle_seconds(row)
        item["idle"] = idle
        item["online"] = idle <= online_within
        out.append(item)
    return out


# ---------- challenges ----------
def add_challenge(
    from_id: int,
    to_id: int,
    lobby: str,
    language: str,
    levels: str,
    topics: str,
    duration: int,
) -> int:
    return int(
        db.execute(
            "INSERT INTO cr_challenges "
            "(from_id, to_id, lobby, language, levels, topics, duration) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                from_id,
                to_id,
                lobby[:8],
                (language or "python")[:20],
                (levels or "")[:64] or None,
                (topics or "")[:255] or None,
                int(duration),
            ),
        )
    )


def _shape_challenge(row: dict) -> dict:
    score = int(row.get("rating") or rating.START_RATING)
    return {
        "id": int(row["id"]),
        "lobby": row["lobby"],
        "language": row.get("language"),
        "levels": row.get("levels") or "",
        "topics": row.get("topics") or "",
        "duration": int(row.get("duration") or 0),
        "status": row.get("status") or "pending",
        "created_at": str(row.get("created_at") or ""),
        "other": {
            "id": int(row["other_id"]),
            "name": row["name"],
            "avatar": int(row.get("avatar_version") or 0) if row.get("avatar_mime") else 0,
            "rating": score,
            "rank": rating.rank_for(score),
        },
    }


def challenges_for(user_id: int) -> dict:
    """Live challenges in both directions. Stale invitations expire first."""
    db.execute(
        "UPDATE cr_challenges SET status = 'expired' "
        "WHERE status = 'pending' AND created_at < NOW() - INTERVAL 10 MINUTE"
    )
    incoming = db.query(
        "SELECT c.id, c.lobby, c.language, c.levels, c.topics, c.duration, "
        "c.status, c.created_at, u.id AS other_id, u.name, u.avatar_mime, "
        "u.avatar_version, u.rating FROM cr_challenges AS c "
        "JOIN cr_users AS u ON u.id = c.from_id "
        "WHERE c.to_id = %s AND c.status = 'pending' ORDER BY c.id DESC LIMIT 10",
        (user_id,),
    )
    outgoing = db.query(
        "SELECT c.id, c.lobby, c.language, c.levels, c.topics, c.duration, "
        "c.status, c.created_at, u.id AS other_id, u.name, u.avatar_mime, "
        "u.avatar_version, u.rating FROM cr_challenges AS c "
        "JOIN cr_users AS u ON u.id = c.to_id "
        "WHERE c.from_id = %s AND c.status IN ('pending', 'accepted') "
        "ORDER BY c.id DESC LIMIT 10",
        (user_id,),
    )
    return {
        "incoming": [_shape_challenge(r) for r in incoming],
        "outgoing": [_shape_challenge(r) for r in outgoing],
    }


def set_challenge_status(challenge_id: int, user_id: int, status: str) -> Optional[dict]:
    """Accept or decline an invitation addressed to this player."""
    row = db.one(
        "SELECT id, from_id, to_id, lobby FROM cr_challenges WHERE id = %s",
        (challenge_id,),
    )
    if row is None or int(row["to_id"]) != user_id:
        return None
    db.execute(
        "UPDATE cr_challenges SET status = %s WHERE id = %s",
        (status[:10], challenge_id),
    )
    return {"id": int(row["id"]), "lobby": row["lobby"], "status": status}


def pending_challenge_count(user_id: int) -> int:
    row = db.one(
        "SELECT COUNT(*) AS n FROM cr_challenges "
        "WHERE to_id = %s AND status = 'pending'",
        (user_id,),
    )
    return int((row or {}).get("n") or 0)
