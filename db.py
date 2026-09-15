"""MySQL persistence: recognised players, their IPs, avatars and race history.

Everything here degrades gracefully: if no database is configured or the server
is unreachable, `enabled()` reports False and the game keeps working without
accounts instead of failing requests.
"""
import hashlib
import logging
import os
import queue
import secrets
import threading
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import unquote, urlparse

import rating

try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:  # driver missing: accounts stay off
    pymysql = None
    DictCursor = None

log = logging.getLogger("coderace.db")

AVATAR_MAX_BYTES = 512 * 1024
AVATAR_TYPES = {
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"\xff\xd8\xff": "image/jpeg",
    b"GIF87a": "image/gif",
    b"GIF89a": "image/gif",
}

POOL_SIZE = 4

_pool: "queue.Queue" = queue.Queue()
_config: Optional[Dict[str, Any]] = None
_ready = False
_lock = threading.Lock()


# ---------- configuration ----------
def _from_url(url: str) -> Optional[Dict[str, Any]]:
    """Parse mysql://user:pass@host:port/db, also tolerating a jdbc: prefix."""
    raw = url.strip()
    if raw.startswith("jdbc:"):
        raw = raw[len("jdbc:") :]
    if "://" not in raw:
        return None
    parsed = urlparse(raw)
    if not parsed.hostname or not parsed.path.strip("/"):
        return None
    return {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "database": parsed.path.strip("/").split("?")[0],
    }


def _read_config() -> Optional[Dict[str, Any]]:
    url = os.environ.get("DATABASE_URL", "").strip()
    cfg = _from_url(url) if url else None
    if cfg is None:
        host = os.environ.get("MYSQL_HOST", "").strip()
        database = os.environ.get("MYSQL_DATABASE", "").strip()
        if not host or not database:
            return None
        cfg = {
            "host": host,
            "port": int(os.environ.get("MYSQL_PORT", "3306") or 3306),
            "user": os.environ.get("MYSQL_USER", "").strip(),
            "password": os.environ.get("MYSQL_PASSWORD", ""),
            "database": database,
        }
    cfg.update(
        charset="utf8mb4",
        autocommit=True,
        connect_timeout=int(os.environ.get("MYSQL_CONNECT_TIMEOUT", "8") or 8),
        read_timeout=20,
        write_timeout=20,
        cursorclass=DictCursor,
    )
    return cfg


# ---------- connections ----------
def _connect():
    return pymysql.connect(**_config)


class _Borrowed:
    """Checked-out connection; pinged on entry, returned (or dropped) on exit."""

    def __init__(self):
        self.conn = None

    def __enter__(self):
        try:
            self.conn = _pool.get_nowait()
        except queue.Empty:
            self.conn = _connect()
        try:
            self.conn.ping(reconnect=True)
        except Exception:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = _connect()
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        if self.conn is None:
            return False
        if exc_type is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            return False
        try:
            _pool.put_nowait(self.conn)
        except queue.Full:
            try:
                self.conn.close()
            except Exception:
                pass
        return False


def _query(sql: str, args: Sequence[Any] = ()) -> List[dict]:
    with _Borrowed() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return list(cur.fetchall() or [])


def _one(sql: str, args: Sequence[Any] = ()) -> Optional[dict]:
    rows = _query(sql, args)
    return rows[0] if rows else None


def _exec(sql: str, args: Sequence[Any] = ()) -> int:
    with _Borrowed() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            return cur.lastrowid or cur.rowcount


SCHEMA = (
    """
    CREATE TABLE IF NOT EXISTS cr_users (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        token CHAR(64) NOT NULL,
        name VARCHAR(18) NOT NULL,
        avatar_mime VARCHAR(40) NULL,
        avatar_data MEDIUMBLOB NULL,
        avatar_version INT UNSIGNED NOT NULL DEFAULT 0,
        races INT UNSIGNED NOT NULL DEFAULT 0,
        best_wpm DECIMAL(6,1) NOT NULL DEFAULT 0,
        best_acc DECIMAL(5,1) NOT NULL DEFAULT 0,
        rating INT NOT NULL DEFAULT 1200,
        wins INT UNSIGNED NOT NULL DEFAULT 0,
        stars INT UNSIGNED NOT NULL DEFAULT 0,
        last_ip VARCHAR(45) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_seen_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uniq_token (token)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS cr_tokens (
        token CHAR(64) NOT NULL,
        user_id INT UNSIGNED NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_seen_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (token),
        KEY idx_cr_tokens_user (user_id),
        CONSTRAINT fk_cr_token_user FOREIGN KEY (user_id)
            REFERENCES cr_users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS cr_user_ips (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        ip VARCHAR(45) NOT NULL,
        hits INT UNSIGNED NOT NULL DEFAULT 1,
        first_seen_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_seen_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uniq_user_ip (user_id, ip),
        CONSTRAINT fk_cr_ip_user FOREIGN KEY (user_id)
            REFERENCES cr_users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS cr_snippets (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        language VARCHAR(20) NOT NULL,
        level VARCHAR(10) NOT NULL,
        topic VARCHAR(24) NOT NULL,
        code MEDIUMTEXT NOT NULL,
        output MEDIUMTEXT NULL,
        code_hash CHAR(64) NOT NULL,
        active TINYINT(1) NOT NULL DEFAULT 1,
        source VARCHAR(16) NOT NULL DEFAULT 'seed',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uniq_cr_snippet_hash (code_hash),
        KEY idx_cr_snippet_pick (language, level, topic, active)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS cr_config (
        name VARCHAR(40) NOT NULL,
        value VARCHAR(255) NOT NULL,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (name)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS cr_races (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id INT UNSIGNED NOT NULL,
        language VARCHAR(20) NOT NULL,
        level VARCHAR(10) NOT NULL DEFAULT '',
        topic VARCHAR(24) NOT NULL DEFAULT '',
        wpm DECIMAL(6,1) NOT NULL,
        acc DECIMAL(5,1) NOT NULL,
        seconds DECIMAL(7,2) NOT NULL,
        place SMALLINT UNSIGNED NULL,
        stars TINYINT UNSIGNED NOT NULL DEFAULT 0,
        rating_delta SMALLINT NOT NULL DEFAULT 0,
        lobby VARCHAR(8) NULL,
        ip VARCHAR(45) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_cr_races_user (user_id),
        KEY idx_cr_races_wpm (wpm),
        CONSTRAINT fk_cr_race_user FOREIGN KEY (user_id)
            REFERENCES cr_users (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
)


# Columns added after the first release; MySQL has no "ADD COLUMN IF NOT EXISTS".
MIGRATIONS = (
    ("cr_snippets", "output", "ALTER TABLE cr_snippets ADD COLUMN output MEDIUMTEXT NULL"),
    ("cr_users", "rating", "ALTER TABLE cr_users ADD COLUMN rating INT NOT NULL DEFAULT 1200"),
    ("cr_users", "wins", "ALTER TABLE cr_users ADD COLUMN wins INT UNSIGNED NOT NULL DEFAULT 0"),
    ("cr_users", "stars", "ALTER TABLE cr_users ADD COLUMN stars INT UNSIGNED NOT NULL DEFAULT 0"),
    ("cr_races", "stars", "ALTER TABLE cr_races ADD COLUMN stars TINYINT UNSIGNED NOT NULL DEFAULT 0"),
    ("cr_races", "rating_delta", "ALTER TABLE cr_races ADD COLUMN rating_delta SMALLINT NOT NULL DEFAULT 0"),
)


def _column_exists(table: str, column: str) -> bool:
    row = _one(
        """
        SELECT COUNT(*) AS n FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = %s AND column_name = %s
        """,
        (table, column),
    )
    return bool((row or {}).get("n"))


def migrate() -> None:
    for table, column, statement in MIGRATIONS:
        try:
            if not _column_exists(table, column):
                _exec(statement)
                log.info("added %s.%s", table, column)
        except Exception as exc:
            log.warning("migration for %s.%s failed: %s", table, column, exc)


def setup() -> bool:
    """Connect and create tables. Safe to call once at startup."""
    global _config, _ready
    with _lock:
        if _ready:
            return True
        if pymysql is None:
            log.warning("pymysql not installed - accounts disabled")
            return False
        _config = _read_config()
        if _config is None:
            log.info("no database configured - accounts disabled")
            return False
        try:
            for statement in SCHEMA:
                _exec(statement)
            _ready = True  # migrate() needs queries to work
            migrate()
            _ready = False
        except Exception as exc:
            log.warning("database unavailable - accounts disabled (%s)", exc)
            _config = None
            return False
        _ready = True
        log.info("database ready on %s/%s", _config["host"], _config["database"])
        return True


def enabled() -> bool:
    return _ready


def close() -> None:
    global _ready
    _ready = False
    while True:
        try:
            conn = _pool.get_nowait()
        except queue.Empty:
            return
        try:
            conn.close()
        except Exception:
            pass


# ---------- tokens ----------
def new_token() -> str:
    return secrets.token_hex(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def clean_name(name: str) -> str:
    return (name or "").strip()[:18]


# Auto-generated handles for players who never picked a name.
NAME_FIRST = (
    "Swift", "Lazy", "Eager", "Bold", "Silent", "Turbo", "Async", "Nimble",
    "Quantum", "Nocturnal", "Caffeinated", "Recursive", "Idempotent", "Atomic",
    "Greedy", "Chaotic", "Stateless", "Immutable", "Blazing", "Feral",
)
NAME_SECOND = (
    "Lambda", "Pointer", "Closure", "Monad", "Daemon", "Cursor", "Pixel",
    "Kernel", "Regex", "Socket", "Buffer", "Thread", "Vector", "Token",
    "Compiler", "Linter", "Falcon", "Otter", "Badger", "Comet",
)


def name_taken(name: str, ignore_id: Optional[int] = None) -> bool:
    """True when someone else already uses this display name (case-insensitive)."""
    if not _ready:
        return False
    row = _one(
        """
        SELECT COUNT(*) AS n FROM cr_users
        WHERE LOWER(name) = LOWER(%s) AND (%s IS NULL OR id <> %s)
        """,
        (clean_name(name), ignore_id, ignore_id),
    )
    return bool((row or {}).get("n"))


def name_suggestions(name: str, ignore_id: Optional[int] = None, count: int = 4) -> List[str]:
    """Free variations on a taken name, in the order a person would try them."""
    base = clean_name(name) or "Player"
    stem = base[:16]
    # Mixed styles, not just base1/base2/base3 - the numbered ones are the
    # least interesting, so they go last.
    ideas: List[str] = [
        f"{stem}1",
        "_".join(base),                    # d_a_v_i_d
        base + "Dev",
        f"the{base.capitalize()}",
        base + "_",
        base.lower() + ".exe",
        base + "Codes",
        f"{stem}42",
        f"x{base}x",
        base + "Types",
        f"{stem}_dev",
        f"{stem}404",
    ]
    for n in list(range(2, 10)) + [7, 99, 101, 2026]:
        ideas.append(f"{stem}{n}")
    ideas.append(random_name())

    out: List[str] = []
    seen = set()
    for idea in ideas:
        candidate = clean_name(idea)
        key = candidate.lower()
        if not candidate or key in seen or len(candidate) < 2:
            continue
        seen.add(key)
        if name_taken(candidate, ignore_id):
            continue
        out.append(candidate)
        if len(out) >= count:
            break
    return out


def random_free_name(tries: int = 12) -> str:
    """A generated handle nobody is using yet."""
    for _ in range(tries):
        candidate = random_name()
        if not name_taken(candidate):
            return candidate
    return clean_name(random_name()[:14] + str(secrets.randbelow(900) + 100))


def random_name() -> str:
    """A readable handle like SwiftLambda42, short enough for the name column."""
    first = secrets.choice(NAME_FIRST)
    second = secrets.choice(NAME_SECOND)
    return clean_name(f"{first}{second}{secrets.randbelow(90) + 10}")


# ---------- profile ----------
def public_user(row: dict) -> dict:
    score = int(row.get("rating") or rating.START_RATING)
    return {
        "id": int(row["id"]),
        "name": row["name"],
        # avatar is a cache-busting version; 0 means no image uploaded
        "avatar": int(row.get("avatar_version") or 0) if row.get("avatar_mime") else 0,
        "races": int(row.get("races") or 0),
        "best_wpm": float(row.get("best_wpm") or 0),
        "best_acc": float(row.get("best_acc") or 0),
        "rating": score,
        "rank": rating.rank_for(score),
        "wins": int(row.get("wins") or 0),
        "stars": int(row.get("stars") or 0),
    }


PROFILE_COLUMNS = """
        id, name, avatar_mime, avatar_version, races, best_wpm, best_acc,
        rating, wins, stars
"""


def find_by_token(token: str) -> Optional[dict]:
    """The account for a cookie. Checks cr_tokens, then the original column."""
    if not _ready or not token:
        return None
    hashed = hash_token(token)
    row = _one(
        """
        SELECT u.id, u.name, u.avatar_mime, u.avatar_version, u.races,
               u.best_wpm, u.best_acc, u.rating, u.wins, u.stars
        FROM cr_tokens AS t
        JOIN cr_users AS u ON u.id = t.user_id
        WHERE t.token = %s
        """,
        (hashed,),
    )
    if row is not None:
        _exec(
            "UPDATE cr_tokens SET last_seen_at = CURRENT_TIMESTAMP WHERE token = %s",
            (hashed,),
        )
        return row
    return _one(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc,
               rating, wins, stars
        FROM cr_users WHERE token = %s
        """,
        (hashed,),
    )


def add_token(user_id: int) -> str:
    """Issue another cookie for an existing account, keeping the old ones valid."""
    token = new_token()
    _exec(
        "INSERT INTO cr_tokens (token, user_id) VALUES (%s, %s)",
        (hash_token(token), user_id),
    )
    return token


def find_by_ip(ip: str) -> Optional[dict]:
    """The account most recently seen from this IP address.

    Used to re-attach a visitor who has lost their cookie. Note that everyone
    behind one NAT shares an address, so this cannot distinguish people in the
    same household or office.
    """
    if not _ready or not ip:
        return None
    return _one(
        """
        SELECT u.id, u.name, u.avatar_mime, u.avatar_version, u.races,
               u.best_wpm, u.best_acc, u.rating, u.wins, u.stars
        FROM cr_user_ips AS p
        JOIN cr_users AS u ON u.id = p.user_id
        WHERE p.ip = %s
        ORDER BY p.last_seen_at DESC
        LIMIT 1
        """,
        (ip[:45],),
    )


def register(name: str, ip: str) -> Tuple[str, dict]:
    """Create a player and return (raw cookie token, public profile)."""
    token = new_token()
    user_id = _exec(
        "INSERT INTO cr_users (token, name, last_ip) VALUES (%s, %s, %s)",
        (hash_token(token), clean_name(name) or "Guest", ip or None),
    )
    _exec(
        "INSERT INTO cr_tokens (token, user_id) VALUES (%s, %s)",
        (hash_token(token), user_id),
    )
    touch_ip(user_id, ip)
    row = _one(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc,
               rating, wins, stars
        FROM cr_users WHERE id = %s
        """,
        (user_id,),
    )
    return token, public_user(row or {"id": user_id, "name": name})


def rename(user_id: int, name: str) -> None:
    _exec("UPDATE cr_users SET name = %s WHERE id = %s", (clean_name(name) or "Guest", user_id))


def sniff_avatar(data: bytes) -> Optional[str]:
    """Detect the image type from magic bytes; None means unsupported."""
    for magic, mime in AVATAR_TYPES.items():
        if data.startswith(magic):
            return mime
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def set_avatar(user_id: int, data: bytes, mime: str) -> int:
    _exec(
        """
        UPDATE cr_users
        SET avatar_data = %s, avatar_mime = %s, avatar_version = avatar_version + 1
        WHERE id = %s
        """,
        (data, mime, user_id),
    )
    row = _one("SELECT avatar_version FROM cr_users WHERE id = %s", (user_id,))
    return int((row or {}).get("avatar_version") or 0)


def clear_avatar(user_id: int) -> None:
    _exec(
        """
        UPDATE cr_users
        SET avatar_data = NULL, avatar_mime = NULL, avatar_version = avatar_version + 1
        WHERE id = %s
        """,
        (user_id,),
    )


def get_avatar(user_id: int) -> Optional[Tuple[bytes, str]]:
    row = _one(
        "SELECT avatar_data, avatar_mime FROM cr_users WHERE id = %s",
        (user_id,),
    )
    if not row or not row.get("avatar_data") or not row.get("avatar_mime"):
        return None
    return bytes(row["avatar_data"]), str(row["avatar_mime"])


# ---------- activity ----------
def touch_ip(user_id: int, ip: str) -> None:
    if not ip:
        return
    _exec(
        """
        INSERT INTO cr_user_ips (user_id, ip) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE hits = hits + 1, last_seen_at = CURRENT_TIMESTAMP
        """,
        (user_id, ip[:45]),
    )


def seen(user_id: int, ip: str) -> None:
    _exec(
        "UPDATE cr_users SET last_seen_at = CURRENT_TIMESTAMP, last_ip = %s WHERE id = %s",
        ((ip or None) and ip[:45], user_id),
    )
    touch_ip(user_id, ip)


def record_race(
    user_id: int,
    language: str,
    level: str,
    topic: str,
    wpm: float,
    acc: float,
    seconds: float,
    place: Optional[int] = None,
    lobby: Optional[str] = None,
    ip: str = "",
    stars: int = 0,
    rating_delta: int = 0,
) -> None:
    _exec(
        """
        INSERT INTO cr_races
            (user_id, language, level, topic, wpm, acc, seconds, place, stars,
             rating_delta, lobby, ip)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            language[:20],
            (level or "")[:10],
            (topic or "")[:24],
            round(float(wpm), 1),
            round(float(acc), 1),
            round(float(seconds), 2),
            place,
            max(0, min(3, int(stars))),
            int(rating_delta),
            (lobby or None) and lobby[:8],
            (ip or None) and ip[:45],
        ),
    )
    _exec(
        """
        UPDATE cr_users
        SET races = races + 1,
            best_wpm = GREATEST(best_wpm, %s),
            best_acc = GREATEST(best_acc, %s),
            rating = GREATEST(%s, rating + %s),
            wins = wins + %s,
            stars = stars + %s
        WHERE id = %s
        """,
        (
            round(float(wpm), 1),
            round(float(acc), 1),
            rating.MIN_RATING,
            int(rating_delta),
            1 if place == 1 else 0,
            max(0, min(3, int(stars))),
            user_id,
        ),
    )


def get_rating(user_id: int) -> int:
    row = _one("SELECT rating FROM cr_users WHERE id = %s", (user_id,))
    return int((row or {}).get("rating") or rating.START_RATING)


def leaderboard(limit: int = 10) -> List[dict]:
    rows = _query(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc,
               rating, wins, stars
        FROM cr_users
        WHERE races > 0
        ORDER BY rating DESC, best_wpm DESC
        LIMIT %s
        """,
        (max(1, min(50, limit)),),
    )
    return [public_user(row) for row in rows]


# ---------- snippet library ----------
def code_hash(language: str, code: str) -> str:
    """Identity of a snippet: the same code under two languages is two rows."""
    parts = (language.encode("utf-8"), code.encode("utf-8"))
    return hashlib.sha256(b"".join(parts)).hexdigest()


def seed_snippets(by_language: Dict[str, List[dict]]) -> int:
    """Insert any seed snippet the table does not have yet. Idempotent."""
    if not _ready:
        return 0
    rows = []
    for language, pool in by_language.items():
        for item in pool:
            rows.append(
                (
                    language[:20],
                    item["level"][:10],
                    item["topic"][:24],
                    item["code"],
                    item.get("output") or None,
                    code_hash(language, item["code"]),
                )
            )
    if not rows:
        return 0
    with _Borrowed() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO cr_snippets
                    (language, level, topic, code, output, code_hash, source)
                VALUES (%s, %s, %s, %s, %s, %s, 'seed')
                ON DUPLICATE KEY UPDATE
                    output = COALESCE(VALUES(output), output)
                """,
                rows,
            )
            return cur.rowcount or 0


def load_snippets() -> Dict[str, List[dict]]:
    """The whole active library, grouped by language."""
    out: Dict[str, List[dict]] = {}
    for row in _query(
        """
        SELECT id, language, level, topic, code, output
        FROM cr_snippets
        WHERE active = 1
        ORDER BY language, level, id
        """
    ):
        out.setdefault(row["language"], []).append(
            {
                "id": int(row["id"]),
                "level": row["level"],
                "topic": row["topic"],
                "code": row["code"],
                "output": row.get("output") or "",
            }
        )
    return out


def add_snippet(language: str, level: str, topic: str, code: str) -> bool:
    """Add one snippet. False means an identical one already exists."""
    changed = _exec(
        """
        INSERT IGNORE INTO cr_snippets
            (language, level, topic, code, code_hash, source)
        VALUES (%s, %s, %s, %s, %s, 'api')
        """,
        (language[:20], level[:10], topic[:24], code, code_hash(language, code)),
    )
    return bool(changed)


def set_snippet_active(snippet_id: int, active: bool) -> None:
    _exec(
        "UPDATE cr_snippets SET active = %s WHERE id = %s",
        (1 if active else 0, snippet_id),
    )


def snippet_count() -> int:
    row = _one("SELECT COUNT(*) AS n FROM cr_snippets WHERE active = 1")
    return int((row or {}).get("n") or 0)


# ---------- settings ----------
def seed_config(defaults: Dict[str, str]) -> int:
    """Write the env-derived defaults once, so the table is editable afterwards."""
    if not _ready or not defaults:
        return 0
    rows = [(name, str(value)) for name, value in defaults.items()]
    with _Borrowed() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT IGNORE INTO cr_config (name, value) VALUES (%s, %s)",
                rows,
            )
            return cur.rowcount or 0


def load_config() -> Dict[str, str]:
    return {row["name"]: row["value"] for row in _query("SELECT name, value FROM cr_config")}


def set_config(name: str, value: str) -> None:
    _exec(
        """
        INSERT INTO cr_config (name, value) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE value = VALUES(value)
        """,
        (name[:40], str(value)[:255]),
    )
