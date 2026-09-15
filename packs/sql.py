"""SQL snippet pack: 20 per level, PostgreSQL-flavoured.

Entries are (level, topic, code, expected_output). Everything is tagged `data`
because that is what SQL is; the level does the sorting.
"""
LANGUAGE = "sql"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "data", r'''
SELECT id, name
FROM users;
''', r''' id | name
----+-------
  1 | ada
  2 | grace
(2 rows)'''),
    ("very-easy", "data", r'''
SELECT COUNT(*)
FROM orders
WHERE paid = true;
''', r''' count
-------
    42
(1 row)'''),
    ("very-easy", "data", r'''
SELECT *
FROM races
LIMIT 10;
''', r'''(10 rows)'''),
    ("very-easy", "data", r'''
SELECT name
FROM users
WHERE active = true;
''', r''' name
-------
 ada
 grace
(2 rows)'''),
    ("very-easy", "data", r'''
SELECT name, wpm
FROM races
ORDER BY wpm DESC;
''', r''' name  | wpm
-------+-----
 ada   | 118
 grace | 104
(2 rows)'''),
    ("very-easy", "data", r'''
INSERT INTO tags (name, slug)
VALUES ('Databases', 'databases');
''', r'''INSERT 0 1'''),
    ("very-easy", "data", r'''
UPDATE users
SET last_seen_at = NOW()
WHERE id = 42;
''', r'''UPDATE 1'''),
    ("very-easy", "data", r'''
DELETE FROM sessions
WHERE expires_at < NOW();
''', r'''DELETE 17'''),
    ("very-easy", "data", r'''
SELECT DISTINCT language
FROM races;
''', r''' language
----------
 python
 rust
(2 rows)'''),
    ("very-easy", "data", r'''
SELECT MAX(wpm) AS best
FROM races;
''', r''' best
------
  118
(1 row)'''),
    ("very-easy", "data", r'''
SELECT AVG(wpm) AS mean_wpm
FROM races;
''', r''' mean_wpm
----------
     94.5
(1 row)'''),
    ("very-easy", "data", r'''
SELECT name
FROM users
WHERE name LIKE 'a%';
''', r''' name
------
 ada
(1 row)'''),
    ("very-easy", "data", r'''
SELECT id, name
FROM users
WHERE id IN (1, 2, 3);
''', r'''(3 rows)'''),
    ("very-easy", "data", r'''
SELECT COUNT(*) AS total, language
FROM races
GROUP BY language;
''', r''' total | language
-------+----------
    31 | python
    12 | rust
(2 rows)'''),
    ("very-easy", "data", r'''
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
''', r'''CREATE TABLE'''),
    ("very-easy", "data", r'''
ALTER TABLE users
ADD COLUMN rating INTEGER NOT NULL DEFAULT 1200;
''', r'''ALTER TABLE'''),
    ("very-easy", "data", r'''
SELECT name
FROM users
WHERE email IS NULL;
''', r''' name
-------
 linus
(1 row)'''),
    ("very-easy", "data", r'''
SELECT id
FROM races
WHERE wpm BETWEEN 90 AND 110;
''', r'''(8 rows)'''),
    ("very-easy", "data", r'''
SELECT name, rating
FROM users
ORDER BY rating DESC
LIMIT 3;
''', r''' name  | rating
-------+--------
 ada   |   1480
 grace |   1390
(3 rows)'''),
    ("very-easy", "data", r'''
SELECT NOW() AS server_time;
''', r'''      server_time
------------------------
 2026-09-16 09:14:22+00
(1 row)'''),

    # --------------------------------------------------------------------- easy
    ("easy", "data", r'''
SELECT id, name, email
FROM users
WHERE active = true
ORDER BY name
LIMIT 50;
''', r''' id | name  | email
----+-------+-------------------
  1 | ada   | ada@example.com
  2 | grace | grace@example.com
(2 rows)'''),
    ("easy", "data", r'''
SELECT u.name, r.wpm
FROM races AS r
JOIN users AS u ON u.id = r.user_id
ORDER BY r.wpm DESC
LIMIT 5;
''', r''' name  | wpm
-------+-----
 ada   | 118
 grace | 104
(5 rows)'''),
    ("easy", "data", r'''
SELECT language, COUNT(*) AS races, ROUND(AVG(wpm), 1) AS avg_wpm
FROM races
GROUP BY language
ORDER BY avg_wpm DESC;
''', r''' language | races | avg_wpm
----------+-------+---------
 python   |    31 |    96.4
 rust     |    12 |    91.8
(2 rows)'''),
    ("easy", "data", r'''
SELECT u.name
FROM users AS u
LEFT JOIN races AS r ON r.user_id = u.id
WHERE r.id IS NULL;
''', r''' name
-------
 linus
(1 row)'''),
    ("easy", "data", r'''
SELECT name, rating
FROM users
WHERE rating > (SELECT AVG(rating) FROM users);
''', r''' name | rating
------+--------
 ada  |   1480
(1 row)'''),
    ("easy", "data", r'''
INSERT INTO races (user_id, language, wpm, acc)
VALUES (1, 'python', 98.5, 97.2)
RETURNING id, created_at;
''', r''' id  |          created_at
-----+------------------------------
 104 | 2026-09-16 09:20:11.512+00
(1 row)'''),
    ("easy", "data", r'''
UPDATE users
SET rating = rating + 24
WHERE id = 1
RETURNING name, rating;
''', r''' name | rating
------+--------
 ada  |   1504
(1 row)'''),
    ("easy", "data", r'''
SELECT COALESCE(nickname, name, 'anonymous') AS display
FROM users
WHERE id = 3;
''', r'''  display
-----------
 anonymous
(1 row)'''),
    ("easy", "data", r'''
SELECT language,
       COUNT(*) FILTER (WHERE wpm > 100) AS fast,
       COUNT(*) AS total
FROM races
GROUP BY language;
''', r''' language | fast | total
----------+------+-------
 python   |    9 |    31
(1 row)'''),
    ("easy", "data", r'''
SELECT DATE_TRUNC('day', created_at) AS day, COUNT(*)
FROM races
GROUP BY day
ORDER BY day DESC
LIMIT 7;
''', r'''          day          | count
-----------------------+-------
 2026-09-16 00:00:00+00|    14
(7 rows)'''),
    ("easy", "data", r'''
CREATE TABLE races (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    wpm NUMERIC(6, 1) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
''', r'''CREATE TABLE'''),
    ("easy", "data", r'''
CREATE INDEX idx_races_user_created
ON races (user_id, created_at DESC);
''', r'''CREATE INDEX'''),
    ("easy", "data", r'''
SELECT name
FROM users
WHERE LOWER(name) = LOWER('Ada');
''', r''' name
------
 ada
(1 row)'''),
    ("easy", "data", r'''
SELECT id, name
FROM users
ORDER BY created_at DESC
OFFSET 20 LIMIT 10;
''', r'''(10 rows)'''),
    ("easy", "data", r'''
SELECT language, MAX(wpm) AS best
FROM races
GROUP BY language
HAVING MAX(wpm) > 100;
''', r''' language | best
----------+------
 python   |  118
(1 row)'''),
    ("easy", "data", r'''
SELECT u.name, COUNT(r.id) AS races
FROM users AS u
LEFT JOIN races AS r ON r.user_id = u.id
GROUP BY u.id, u.name
ORDER BY races DESC;
''', r''' name  | races
-------+-------
 ada   |    31
 linus |     0
(2 rows)'''),
    ("easy", "data", r'''
SELECT CASE
           WHEN rating >= 1500 THEN 'senior'
           WHEN rating >= 1200 THEN 'mid'
           ELSE 'junior'
       END AS band,
       COUNT(*)
FROM users
GROUP BY band;
''', r'''  band  | count
--------+-------
 mid    |    12
 junior |     5
(2 rows)'''),
    ("easy", "data", r'''
SELECT name
FROM users
WHERE created_at >= NOW() - INTERVAL '7 days';
''', r''' name
-------
 grace
(1 row)'''),
    ("easy", "data", r'''
SELECT STRING_AGG(name, ', ' ORDER BY name) AS everyone
FROM users;
''', r'''      everyone
---------------------
 ada, grace, linus
(1 row)'''),
    ("easy", "data", r'''
BEGIN;

UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

COMMIT;
''', r'''BEGIN
UPDATE 1
UPDATE 1
COMMIT'''),

    # ------------------------------------------------------------------- medium
    ("medium", "data", r'''
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 3
ORDER BY order_count DESC
LIMIT 20;
''', r''' id | name  | order_count
----+-------+-------------
  2 | grace |           7
  1 | ada   |           4
(2 rows)'''),
    ("medium", "data", r'''
WITH monthly AS (
    SELECT DATE_TRUNC('month', created_at) AS month,
           SUM(total) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY 1
)
SELECT month, revenue
FROM monthly
WHERE revenue > 10000
ORDER BY month;
''', r'''   month    | revenue
------------+----------
 2024-03-01 | 18240.00
 2024-04-01 | 21980.50
(2 rows)'''),
    ("medium", "data", r'''
WITH ranked AS (
    SELECT user_id,
           wpm,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY wpm DESC) AS rn
    FROM races
)
SELECT user_id, wpm
FROM ranked
WHERE rn = 1;
''', r''' user_id | wpm
---------+-----
       1 | 118
       2 | 104
(2 rows)'''),
    ("medium", "data", r'''
INSERT INTO daily_stats (day, plays, avg_wpm)
SELECT DATE_TRUNC('day', finished_at), COUNT(*), AVG(wpm)
FROM races
GROUP BY 1
ON CONFLICT (day) DO UPDATE
SET plays = EXCLUDED.plays,
    avg_wpm = EXCLUDED.avg_wpm;
''', r'''INSERT 0 31'''),
    ("medium", "data", r'''
SELECT language,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY wpm) AS median_wpm
FROM races
GROUP BY language
ORDER BY median_wpm DESC;
''', r''' language | median_wpm
----------+------------
 python   |       96.0
 rust     |       91.5
(2 rows)'''),
    ("medium", "data", r'''
SELECT u.name,
       r.wpm,
       r.wpm - LAG(r.wpm) OVER (PARTITION BY r.user_id ORDER BY r.created_at) AS delta
FROM races AS r
JOIN users AS u ON u.id = r.user_id
ORDER BY u.name, r.created_at;
''', r''' name | wpm | delta
------+-----+-------
 ada  |  94 |
 ada  | 101 |     7
(2 rows)'''),
    ("medium", "data", r'''
SELECT language, level, COUNT(*) AS snippets
FROM snippets
GROUP BY GROUPING SETS ((language, level), (language), ())
ORDER BY language NULLS LAST, level NULLS LAST;
''', r''' language | level  | snippets
----------+--------+----------
 python   | easy   |       20
 python   |        |       80
          |        |     1200
(3 rows)'''),
    ("medium", "data", r'''
SELECT r.language, COUNT(*) AS races
FROM races AS r
WHERE EXISTS (
    SELECT 1
    FROM users AS u
    WHERE u.id = r.user_id AND u.rating > 1400
)
GROUP BY r.language;
''', r''' language | races
----------+-------
 python   |    12
(1 row)'''),
    ("medium", "data", r'''
UPDATE users AS u
SET rating = u.rating + s.delta
FROM (
    SELECT user_id, SUM(rating_delta) AS delta
    FROM races
    WHERE created_at >= NOW() - INTERVAL '1 day'
    GROUP BY user_id
) AS s
WHERE u.id = s.user_id;
''', r'''UPDATE 14'''),
    ("medium", "data", r'''
SELECT name, rating
FROM users
WHERE rating = (SELECT MAX(rating) FROM users)
FOR UPDATE SKIP LOCKED;
''', r''' name | rating
------+--------
 ada  |   1504
(1 row)'''),
    ("medium", "data", r'''
CREATE VIEW leaderboard AS
SELECT u.id,
       u.name,
       MAX(r.wpm) AS best_wpm,
       COUNT(r.id) AS races
FROM users AS u
JOIN races AS r ON r.user_id = u.id
GROUP BY u.id, u.name;
''', r'''CREATE VIEW'''),
    ("medium", "data", r'''
SELECT day, plays,
       AVG(plays) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
           AS rolling_7
FROM daily_stats
ORDER BY day DESC
LIMIT 14;
''', r'''    day     | plays | rolling_7
------------+-------+-----------
 2026-09-16 |    14 |      11.4
(14 rows)'''),
    ("medium", "data", r'''
SELECT id, payload ->> 'language' AS language
FROM events
WHERE payload @> '{"type": "race_finished"}'::jsonb
ORDER BY id DESC
LIMIT 5;
''', r''' id | language
----+----------
 91 | python
(5 rows)'''),
    ("medium", "data", r'''
SELECT name
FROM users
WHERE to_tsvector('english', bio) @@ to_tsquery('english', 'rust & typing');
''', r''' name
-------
 grace
(1 row)'''),
    ("medium", "data", r'''
DELETE FROM races AS r
USING users AS u
WHERE r.user_id = u.id
  AND u.active = false
  AND r.created_at < NOW() - INTERVAL '1 year';
''', r'''DELETE 312'''),
    ("medium", "data", r'''
SELECT COUNT(*) AS total,
       COUNT(DISTINCT user_id) AS players,
       SUM(wpm) / NULLIF(COUNT(*), 0) AS mean_wpm
FROM races
WHERE created_at >= CURRENT_DATE;
''', r''' total | players | mean_wpm
-------+---------+----------
    14 |       6 |     95.2
(1 row)'''),
    ("medium", "data", r'''
CREATE TABLE races_2026 PARTITION OF races
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
''', r'''CREATE TABLE'''),
    ("medium", "data", r'''
SELECT u.name, r.language, r.wpm
FROM users AS u
CROSS JOIN LATERAL (
    SELECT language, wpm
    FROM races
    WHERE user_id = u.id
    ORDER BY wpm DESC
    LIMIT 1
) AS r;
''', r''' name  | language | wpm
-------+----------+-----
 ada   | python   | 118
 grace | rust     | 104
(2 rows)'''),
    ("medium", "data", r'''
SELECT generate_series(1, 5) AS n,
       generate_series(1, 5) * generate_series(1, 5) AS square;
''', r''' n | square
---+--------
 1 |      1
 2 |      4
(5 rows)'''),
    ("medium", "data", r'''
EXPLAIN ANALYZE
SELECT user_id, MAX(wpm)
FROM races
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY user_id;
''', r'''HashAggregate  (cost=214.50..216.50 rows=200 width=12)
  ->  Index Scan using idx_races_created_at on races
Planning Time: 0.214 ms
Execution Time: 3.881 ms'''),

    # --------------------------------------------------------------------- hard
    ("hard", "data", r'''
SELECT
    user_id,
    total,
    RANK() OVER (PARTITION BY user_id ORDER BY total DESC) AS rank_in_user,
    SUM(total) OVER (PARTITION BY user_id) AS lifetime_value,
    LAG(created_at) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_at
FROM orders
WHERE created_at >= NOW() - INTERVAL '12 months';
''', r''' user_id | total | rank_in_user | lifetime_value | prev_order_at
---------+-------+--------------+----------------+---------------
       1 | 90.00 |            1 |         210.00 |
(3 rows)'''),
    ("hard", "data", r'''
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.parent_id, c.name, t.depth + 1
    FROM categories AS c
    JOIN tree AS t ON t.id = c.parent_id
)
SELECT REPEAT('  ', depth - 1) || name AS label, depth
FROM tree
ORDER BY depth, name;
''', r'''    label    | depth
-------------+-------
 languages   |     1
   python    |     2
(2 rows)'''),
    ("hard", "data", r'''
WITH RECURSIVE dates AS (
    SELECT DATE_TRUNC('day', NOW() - INTERVAL '29 days') AS day
    UNION ALL
    SELECT day + INTERVAL '1 day' FROM dates WHERE day < DATE_TRUNC('day', NOW())
)
SELECT d.day, COALESCE(COUNT(r.id), 0) AS races
FROM dates AS d
LEFT JOIN races AS r ON DATE_TRUNC('day', r.created_at) = d.day
GROUP BY d.day
ORDER BY d.day;
''', r'''    day     | races
------------+-------
 2026-08-18 |     0
 2026-08-19 |     3
(30 rows)'''),
    ("hard", "data", r'''
SELECT
    language,
    COUNT(*) AS races,
    ROUND(AVG(wpm), 1) AS avg_wpm,
    ROUND(STDDEV_SAMP(wpm), 1) AS spread,
    PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY wpm) AS p90
FROM races
GROUP BY language
HAVING COUNT(*) >= 10
ORDER BY avg_wpm DESC;
''', r''' language | races | avg_wpm | spread | p90
----------+-------+---------+--------+-----
 python   |    31 |    96.4 |   12.8 | 114
(1 row)'''),
    ("hard", "data", r'''
CREATE MATERIALIZED VIEW leaderboard_cache AS
SELECT u.id,
       u.name,
       MAX(r.wpm) AS best_wpm,
       COUNT(r.id) AS races,
       MAX(r.created_at) AS last_race
FROM users AS u
JOIN races AS r ON r.user_id = u.id
GROUP BY u.id, u.name
WITH DATA;

CREATE UNIQUE INDEX ON leaderboard_cache (id);
''', r'''SELECT 214
CREATE INDEX'''),
    ("hard", "data", r'''
CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_touch
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION touch_updated_at();
''', r'''CREATE FUNCTION
CREATE TRIGGER'''),
    ("hard", "data", r'''
CREATE OR REPLACE FUNCTION rating_after(
    current INTEGER,
    opponent INTEGER,
    score NUMERIC
) RETURNS INTEGER AS $$
DECLARE
    expected NUMERIC;
BEGIN
    expected := 1.0 / (1.0 + POWER(10, (opponent - current) / 400.0));
    RETURN GREATEST(100, ROUND(current + 24 * (score - expected)));
END;
$$ LANGUAGE plpgsql IMMUTABLE;
''', r'''CREATE FUNCTION
SELECT rating_after(1200, 2250, 1) => 1224'''),
    ("hard", "data", r'''
SELECT
    u.name,
    COUNT(*) AS races,
    SUM(CASE WHEN r.place = 1 THEN 1 ELSE 0 END) AS wins,
    ROUND(
        100.0 * SUM(CASE WHEN r.place = 1 THEN 1 ELSE 0 END) / COUNT(*),
        1
    ) AS win_rate
FROM races AS r
JOIN users AS u ON u.id = r.user_id
GROUP BY u.id, u.name
HAVING COUNT(*) >= 5
ORDER BY win_rate DESC, races DESC;
''', r''' name  | races | wins | win_rate
-------+-------+------+----------
 ada   |    31 |   19 |     61.3
(1 row)'''),
    ("hard", "data", r'''
WITH gaps AS (
    SELECT user_id,
           created_at,
           created_at - LAG(created_at) OVER (
               PARTITION BY user_id ORDER BY created_at
           ) AS gap
    FROM races
)
SELECT user_id, COUNT(*) AS sessions
FROM gaps
WHERE gap IS NULL OR gap > INTERVAL '30 minutes'
GROUP BY user_id
ORDER BY sessions DESC;
''', r''' user_id | sessions
---------+----------
       1 |        9
(1 row)'''),
    ("hard", "data", r'''
SELECT
    DATE_TRUNC('week', created_at) AS week,
    COUNT(DISTINCT user_id) AS players,
    COUNT(DISTINCT user_id) FILTER (
        WHERE created_at >= DATE_TRUNC('week', created_at) + INTERVAL '3 days'
    ) AS late_week_players
FROM races
GROUP BY week
ORDER BY week DESC
LIMIT 8;
''', r'''   week     | players | late_week_players
------------+---------+-------------------
 2026-09-14 |      41 |                18
(8 rows)'''),
    ("hard", "data", r'''
INSERT INTO snippets (language, level, topic, code, code_hash)
SELECT language, level, topic, code, SHA256(code::bytea)
FROM staging_snippets
ON CONFLICT (code_hash) DO UPDATE
SET level = EXCLUDED.level,
    topic = EXCLUDED.topic
WHERE snippets.level <> EXCLUDED.level
   OR snippets.topic <> EXCLUDED.topic;
''', r'''INSERT 0 1200'''),
    ("hard", "data", r'''
SELECT
    r.language,
    JSONB_AGG(
        JSONB_BUILD_OBJECT('name', u.name, 'wpm', r.wpm)
        ORDER BY r.wpm DESC
    ) FILTER (WHERE r.wpm IS NOT NULL) AS top_players
FROM races AS r
JOIN users AS u ON u.id = r.user_id
GROUP BY r.language;
''', r''' language |              top_players
----------+----------------------------------------
 python   | [{"name": "ada", "wpm": 118}, ...]
(1 row)'''),
    ("hard", "data", r'''
CREATE TABLE races (
    id BIGSERIAL,
    user_id INTEGER NOT NULL,
    wpm NUMERIC(6, 1) NOT NULL CHECK (wpm >= 0 AND wpm <= 400),
    acc NUMERIC(5, 1) NOT NULL CHECK (acc BETWEEN 0 AND 100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);
''', r'''CREATE TABLE'''),
    ("hard", "data", r'''
SELECT
    a.name AS player,
    b.name AS opponent,
    COUNT(*) AS meetings
FROM races AS ra
JOIN races AS rb
  ON rb.lobby = ra.lobby AND rb.user_id <> ra.user_id
JOIN users AS a ON a.id = ra.user_id
JOIN users AS b ON b.id = rb.user_id
GROUP BY a.name, b.name
HAVING COUNT(*) > 2
ORDER BY meetings DESC;
''', r''' player | opponent | meetings
--------+----------+----------
 ada    | grace    |        7
(1 row)'''),
    ("hard", "data", r'''
WITH ranked AS (
    SELECT id,
           user_id,
           wpm,
           NTILE(4) OVER (ORDER BY wpm) AS quartile
    FROM races
)
SELECT quartile,
       MIN(wpm) AS floor_wpm,
       MAX(wpm) AS ceil_wpm,
       COUNT(*) AS races
FROM ranked
GROUP BY quartile
ORDER BY quartile;
''', r''' quartile | floor_wpm | ceil_wpm | races
----------+-----------+----------+-------
        1 |      31.0 |     78.0 |    54
(4 rows)'''),
    ("hard", "data", r'''
SELECT setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
       setweight(to_tsvector('english', coalesce(bio, '')), 'B') AS document,
       ts_rank(
           setweight(to_tsvector('english', coalesce(name, '')), 'A'),
           to_tsquery('english', 'rust')
       ) AS rank
FROM users
ORDER BY rank DESC
LIMIT 5;
''', r'''(5 rows)'''),
    ("hard", "data", r'''
CREATE OR REPLACE PROCEDURE archive_old_races(cutoff INTERVAL)
LANGUAGE plpgsql AS $$
DECLARE
    moved INTEGER;
BEGIN
    WITH gone AS (
        DELETE FROM races
        WHERE created_at < NOW() - cutoff
        RETURNING *
    )
    INSERT INTO races_archive SELECT * FROM gone;

    GET DIAGNOSTICS moved = ROW_COUNT;
    RAISE NOTICE 'archived % rows', moved;
END;
$$;
''', r'''CREATE PROCEDURE
CALL archive_old_races('1 year');
NOTICE:  archived 312 rows'''),
    ("hard", "data", r'''
SELECT
    u.id,
    u.name,
    u.rating,
    RANK() OVER (ORDER BY u.rating DESC) AS position,
    u.rating - LEAD(u.rating) OVER (ORDER BY u.rating DESC) AS lead_over_next
FROM users AS u
WHERE u.races > 0
ORDER BY position
LIMIT 25;
''', r''' id | name  | rating | position | lead_over_next
----+-------+--------+----------+----------------
  1 | ada   |   1504 |        1 |            114
  2 | grace |   1390 |        2 |             90
(25 rows)'''),
    ("hard", "data", r'''
BEGIN ISOLATION LEVEL SERIALIZABLE;

SELECT balance INTO STRICT current_balance
FROM accounts
WHERE id = 1
FOR UPDATE;

UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

COMMIT;
''', r'''BEGIN
UPDATE 1
UPDATE 1
COMMIT'''),
    ("hard", "data", r'''
SELECT
    language,
    level,
    COUNT(*) AS have,
    GREATEST(0, 20 - COUNT(*)) AS still_needed
FROM snippets
WHERE active
GROUP BY language, level
ORDER BY still_needed DESC, language, level;
''', r''' language | level     | have | still_needed
----------+-----------+------+--------------
 bash     | medium    |    2 |           18
 python   | easy      |   20 |            0
(60 rows)'''),
]
