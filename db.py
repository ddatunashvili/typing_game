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
        last_ip VARCHAR(45) NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_seen_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE KEY uniq_token (token)
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


# ---------- profile ----------
def public_user(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "name": row["name"],
        # avatar is a cache-busting version; 0 means no image uploaded
        "avatar": int(row.get("avatar_version") or 0) if row.get("avatar_mime") else 0,
        "races": int(row.get("races") or 0),
        "best_wpm": float(row.get("best_wpm") or 0),
        "best_acc": float(row.get("best_acc") or 0),
    }


def find_by_token(token: str) -> Optional[dict]:
    if not _ready or not token:
        return None
    return _one(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc
        FROM cr_users WHERE token = %s
        """,
        (hash_token(token),),
    )


def register(name: str, ip: str) -> Tuple[str, dict]:
    """Create a player and return (raw cookie token, public profile)."""
    token = new_token()
    user_id = _exec(
        "INSERT INTO cr_users (token, name, last_ip) VALUES (%s, %s, %s)",
        (hash_token(token), clean_name(name) or "Guest", ip or None),
    )
    touch_ip(user_id, ip)
    row = _one(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc
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
) -> None:
    _exec(
        """
        INSERT INTO cr_races
            (user_id, language, level, topic, wpm, acc, seconds, place, lobby, ip)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            (lobby or None) and lobby[:8],
            (ip or None) and ip[:45],
        ),
    )
    _exec(
        """
        UPDATE cr_users
        SET races = races + 1,
            best_wpm = GREATEST(best_wpm, %s),
            best_acc = GREATEST(best_acc, %s)
        WHERE id = %s
        """,
        (round(float(wpm), 1), round(float(acc), 1), user_id),
    )


def leaderboard(limit: int = 10) -> List[dict]:
    rows = _query(
        """
        SELECT id, name, avatar_mime, avatar_version, races, best_wpm, best_acc
        FROM cr_users
        WHERE races > 0
        ORDER BY best_wpm DESC, best_acc DESC
        LIMIT %s
        """,
        (max(1, min(50, limit)),),
    )
    return [public_user(row) for row in rows]
