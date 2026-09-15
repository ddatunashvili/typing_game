# CodeRace

Typer.io-style typing game for **real code**, with syntax highlighting, multiplayer lobbies and live chat.
Backend: FastAPI + WebSockets. Frontend: vanilla JS + Prism.js.

## Run

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000

## Play

- Pick a language (15 available), a **level** and the **topics** you want, then
  **Practice solo** or **Create lobby**.
- Share the invite link (the code pill copies it) or the 5-char code — friends paste it into **Join**.
- Host presses **Start race**; a race also auto-starts when everyone is Ready.
- The upcoming snippet is on screen during the countdown, so you can read ahead.
- When a race ends the host gets **Race again** (straight into another race on a new snippet)
  and **Another snippet** (swap the snippet without starting).
- 5s countdown, then everyone types the same snippet. Chat lives in the left panel.
- Live WPM / accuracy / progress bars per player, results table with placements.

## Levels and topics

Every snippet is tagged with one level and one topic, so you can narrow what you get.

- **Levels:** `very-easy` ("Really easy"), `easy`, `medium`, `hard` — graded by typing load
  (symbol density, nesting, length). All 15 languages have snippets at every level.
- **20+ snippets per level per language** across all 15 languages - **1,253 in total**,
  96% of them with a demo transcript for the run panel. Every language has its own
  `packs/<language>.py` holding `(level, topic, code, output)` tuples, merged automatically
  and skipping anything already present.

| language | really easy | easy | medium | hard | total |
| --- | --- | --- | --- | --- | --- |
| Python | 20 | 20 | 20 | 20 | 80 |
| JavaScript | 22 | 23 | 20 | 22 | 87 |
| TypeScript | 20 | 20 | 23 | 22 | 85 |
| Go | 22 | 21 | 21 | 22 | 86 |
| Rust | 20 | 21 | 21 | 22 | 84 |
| Java | 20 | 20 | 21 | 21 | 82 |
| C | 20 | 21 | 21 | 21 | 83 |
| C++ | 20 | 21 | 20 | 21 | 82 |
| C# | 20 | 21 | 21 | 22 | 84 |
| PHP | 20 | 21 | 21 | 22 | 84 |
| Ruby | 20 | 21 | 21 | 21 | 83 |
| SQL | 20 | 21 | 21 | 21 | 83 |
| CSS | 20 | 21 | 20 | 22 | 83 |
| HTML | 20 | 21 | 22 | 22 | 85 |
| Bash | 20 | 20 | 20 | 22 | 82 |

Where a real parser was available the snippets were checked with it: all 80 Python compile
with `compile()`, all 80 JavaScript parse through `vm.compileFunction`, all 82 PHP pass
`php -l` and all 82 Bash pass `bash -n`.
- **Topics:** `algorithms`, `data-structures`, `strings`, `math`, `async`, `web`, `oop`,
  `functional`, `errors`, `data`, `ui`, `devops`.
- Picking nothing means *any*. Picking several is a union — `easy` + `hard` gives both.
- Snippets are dealt from a **shuffled deck**, not picked at random: every snippet in the pool
  comes up once before any repeats, and never twice in a row.
- Once a race has a level, later snippets **stay on that level**, so difficulty does not jump
  between rounds. Changing the language or the level/topic filters releases the lock.
- Chips show how many snippets each choice has for the current language, and topics the
  language has nothing for are hidden (SQL has no `async` snippets, for instance).
- If a combination matches nothing, the app says so and falls back to a random snippet from
  that language rather than leaving you with an empty screen.
- In a lobby the **filters** button opens the same picker; only the host can change it, and
  it locks while a race is running.

## Race time

A race is either **classic** (one snippet, ends when you finish it) or **timed**.

- Pick the length on the home screen: one snippet, 30s, 1 min, 2 min or 5 min.
- In timed mode every racer works through the same shuffled **playlist**, so it stays fair.
  Finish a snippet while the clock is still running and the next one appears immediately.
- Ranking is by **characters typed**, then accuracy — not by who finished first.
- The server owns the clock: it ends the race and ranks everyone, so a tampered or lagging
  client cannot keep typing past the buzzer.
- The host can switch the length from the lobby's **filters** tray; it locks during a race.
- `playlist_size` (default 12) sets how many snippets a lobby playlist holds; solo timed runs
  request 40. The pool is reshuffled and repeated when it is smaller than that.

## Stars, ratings and ranks

Every finished run gets **0-3 stars**, scored on accuracy and the error rate so a long
sloppy run cannot coast on a round percentage:

| stars | condition | note |
| --- | --- | --- |
| 3 | accuracy >= 96% and <= 4% error rate | Clean run |
| 2 | accuracy >= 88% and <= 12% error rate | Solid, a few slips |
| 1 | accuracy >= 72% | Messy - lots of corrections |
| 0 | below that, or unfinished | Rough one |

**Winning the race is worth a star** on top (capped at 3), so out-typing everyone cannot
score below a tidier opponent who covered a third of the distance. In timed mode the error
rate is measured against the characters you actually covered, not one snippet's length.

**Bots get no stars at all.** They type at a fixed synthetic accuracy, so a star rating for
them would be meaningless and would flatter them against a real player; the results table
shows a dash instead.

When a race ends the winner (or loser) gets an outcome overlay: animated stars, who you beat
or who beat you, your WPM, accuracy, place and rating change.

Multiplayer races also move an **Elo rating** (start 1200, K-factor 24), scored pairwise
against everyone in the lobby and averaged, so a crowded lobby is not worth more than a
duel and beating someone stronger pays more. Bots and unregistered guests count as
opposition but carry no rating of their own. Solo runs earn stars but never move the rating.

Rank titles run from **Rubber Duck** through Script Kiddie, Intern, Junior/Mid/Senior Dev,
Tech Lead, Architect, Principal and 10x Engineer up to **Kernel Hacker** at 2300.

The **Rankings** page in the top bar lists rated players, the full bot ladder and the rank
tiers, and re-reads itself every 15 seconds (plus immediately after any race finishes).

## Simulated run

When a snippet is finished the run panel shows the output that snippet produces.

**Nothing is executed.** Running code typed by a stranger in 15 languages would be a
sandbox-escape risk and a large amount of infrastructure, so each snippet carries a stored
transcript (`cr_snippets.output`) written by hand, plus a short demo call where the snippet
only defines things. Because every racer types the same snippet the result is deterministic,
so the transcript is accurate for what it claims to be - and the panel says so in as many
words. 74 of the 117 seed snippets have one; the rest report that they compiled with no
output. Add more with SQL:

```sql
UPDATE cr_snippets SET output = '>>> square(7)
49' WHERE id = 12;
```

## Bots

Thirteen bot opponents from **Rubber Duck** (750, 18 wpm) to **Kernel Panic Kim**
(2250, 138 wpm), each with a rating and a target speed. They type at their target wpm with
jitter and occasional hesitations rather than at a flat rate.

Portraits come from `static/bots/`, imported with
`python tools/import_bot_avatars.py <zip-or-folder>` - filenames map to slugs
(`null_pointer_pete.png` to `null-pointer-pete`). The importer crops the middle band of the
artwork for the round avatar, because the source cards have the blurb and rating printed
across the top and bottom. Any bot without artwork falls back to a generated identicon
(a mirrored 5x5 grid, no external service).

Challenge one from the home screen, or add one mid-lobby with **+ bot**. Bots are always
ready, so hitting **Ready** starts the race.

## Opponent carets

While a race is running you see every other racer's caret in the code, in their own colour
with their name on it. A caret that is ahead of yours pulses, so a rush is obvious. Carets
only show for racers on the same snippet as you, which matters in timed mode where players
drift apart in the playlist.

## Bot trash talk

Every bot has its own set of five rough one-liners and fires them into the lobby chat at
random while it types - first jab a few seconds in, then every 6-13 seconds, never repeating
within a race. They aim at your code and the clock, not at you. Lines live in `ROASTS` in
`bots.py`.

## Profiles

Optional — the game is fully playable without them, and everything below turns itself off
when no database is configured.

- **No sign-up.** Your first visit mints a profile automatically: a generated handle like
  `QuantumRegex42`, a generated identicon and a rating of 1200. The top bar shows a
  **profile button**, not a register button.
- **Lost your cookie?** With `IP_AUTOLOGIN=1` (the default) a visitor with no cookie is
  re-attached to the account last seen from their IP instead of getting a fresh one, so a
  cleared cookie does not strand a rating. Cookies live in `cr_tokens`, so one account can
  hold several of them and a second device does not log the first one out.

  The trade-off is real: **everyone behind one router, office NAT, mobile carrier or VPN
  shares an IP**, so they land on the same profile and can rename it or add to its rating.
  Set `IP_AUTOLOGIN=0` to make the cookie the only identity.
- Open it to change your **name** or **avatar**. Names are unique: the dialog checks
  availability as you type and, if the name is taken, offers free variations
  (`Davit1`, `D_a_v_i_t`, `DavitDev`, `theDavit`, `Davit_`, `davit.exe`) as one-click chips.
- The avatar picker takes a **drag-and-dropped** file or a click, then opens a **cropper**
  with a circular guide, drag-to-reposition and a zoom slider. The square is rendered to a
  256x256 WebP in the browser before upload, so the 512 KB cap is never the thing that
  stops you.
- You are **recognised automatically** on your next visit: registering sets a long-lived
  `HttpOnly` cookie holding a random token, and only the SHA-256 of that token is stored.
- Avatars are kept in MySQL as BLOBs, not on disk — the panel replaces `/home/container`
  on every start, so uploaded files would not survive a restart.
- Recognised players race under their saved name, show their avatar in the racer list and
  chat, and have finished races recorded for the leaderboard.
- IP addresses are stored per player (last seen, plus a per-IP hit log). That is personal
  data — make sure that is what you want before deploying publicly.

## SEO and embeds

- Full meta set in `static/index.html`: title, description, canonical, robots
  (`max-image-preview:large`), theme-color, Open Graph (including `og:image:width/height`
  and alt text), Twitter `summary_large_image`, and a `WebApplication` JSON-LD block.
- `{{SITE_URL}}` in the markup is substituted at serve time from the `SITE_URL` env var,
  because social scrapers reject relative image URLs. Set it to your real origin.
- Generated assets in `static/`, rebuilt with `python tools/make_assets.py`:
  `og.png` (1200x630 social card), `icon-512.png`, `icon-192.png`,
  `apple-touch-icon.png` (180x180), `favicon.svg` and `favicon.ico`.
- `/manifest.webmanifest`, `/robots.txt` and `/sitemap.xml` are served by the app.
  Lobby URLs (`/?l=CODE`) are excluded from crawling - they are ephemeral.

## Layout

The page centres on a **1300px** column on a desktop and reflows down from there: the
level / topics / race-time panels sit in one row on a wide screen, drop to two columns
below 1100px and stack below 820px, where the lobby chat moves underneath the race instead
of beside it. Below 620px the racer rows put the progress bar on its own line and the action
buttons go full width. Scrollbars are restyled thin and dark, with a stable gutter so the
layout does not jump when one appears.

## Typing rules

- Wrong key marks the character red and blocks — press the right key or Backspace.
- Pressing Enter auto-skips the next line's indentation (like typer.io).
- Untyped code is dimmed; typed code lights up in full syntax color.

## Layout

| file | role |
| --- | --- |
| `main.py` | FastAPI app, lobby state machine, `/ws/{code}` websocket, REST API |
| `snippets.py` | seed snippet library, tagged by language / level / topic |
| `packs/` | per-language snippet packs; drop in a module and it is picked up |
| `library.py` | reads snippets and settings from MySQL, falls back to the seed file |
| `db.py` | MySQL: players, IP log, avatars, race history, snippets, settings |
| `static/app.js` | typing engine, per-char highlighting, filters, profile, lobby client |
| `static/style.css` | dark theme |
| `static/index.html` | markup + Prism component loading |
| `rating.py` | stars, Elo and rank titles |
| `bots.py` | bot roster and generated identicons |
| `outputs.py` | demo transcripts for the simulated run panel |
| `tools/make_assets.py` | regenerates the OG card and icons |
| `tools/import_bot_avatars.py` | imports bot artwork from a zip or folder |
| `deploy/nginx.conf` | reverse proxy with TLS, WebSocket upgrade and static caching |

## API

Catalog and snippets:

- `GET /api/meta` — languages, levels, topics and per-language counts (incl. level×topic)
- `GET /api/languages` — language list
- `GET /api/snippet?lang=python&levels=easy,hard&topics=math&level=easy` — one snippet + its
  tags; `level` pins an exact level
- `GET /api/playlist?lang=python&size=12&levels=&topics=` — an ordered run, for timed solo
- `GET /api/config` — effective settings and where the library is being read from
- `GET /api/lobby/new?lang=python&levels=&topics=&duration=60` — create lobby, returns code
- `GET /api/lobby/{code}` — lobby snapshot
- `GET /healthz` — liveness, lobby count, database state

Accounts (all no-ops when no database is configured):

- `GET /api/me` — the recognised player for this cookie, or `null`
- `POST /api/register` `{name}` — create a player, sets the recognition cookie
- `POST /api/profile` `{name}` — rename
- `POST /api/avatar` (multipart `file`) — upload a profile image
- `DELETE /api/avatar` — remove it
- `GET /api/avatar/{user_id}` — serve it
- `GET /api/leaderboard?limit=10` — top players by rating
- `GET /api/rankings?limit=50` — the rankings board, the viewer's own row, bots and tiers
- `GET /api/bots` — the bot roster with ratings
- `GET /api/bot-avatar/{slug}` — bot portrait (imported artwork, else a generated identicon)
- `GET /api/bot-card/{slug}` — the full bot character-card illustration
- `GET /api/name-check?name=x` — is this display name free, plus suggestions if not
- `POST /api/race` — record a solo result (lobby races are recorded server-side)

Websocket `WS /ws/{code}?name=&pid=&create=0|1&lang=&levels=&topics=&duration=`

Client → server: `chat`, `ready`, `start`, `restart`, `again`, `lang`, `filters`,
`duration`, `bot`, `unbot`, `progress`, `finish` — `again` swaps the snippet, `restart`
starts another race, `bot`/`unbot` seat and remove a bot (host only)
Server → client: `hello`, `state`, `chat`, `countdown`, `go`, `prog`, `time_up`, `error`

## Where the snippets live

The snippets and the tunable settings are stored in MySQL, in `cr_snippets` and `cr_config`.

- `snippets.py` is the **seed**. On every start it is pushed into `cr_snippets` with
  `INSERT IGNORE` keyed by a content hash, so restarts never duplicate rows and hand-edits
  are never overwritten.
- The running server re-reads both tables every `LIBRARY_REFRESH_SECONDS` (default 60), so
  SQL edits take effect without a restart or a redeploy.
- With no database configured the seed file is used directly; `GET /api/config` reports which
  source is live.

Add or retire a snippet without touching the code:

```sql
INSERT INTO cr_snippets (language, level, topic, code, code_hash)
VALUES ('python', 'very-easy', 'math', 'x = 1 + 1', SHA2(CONCAT('python', CHAR(31), 'x = 1 + 1'), 256));

UPDATE cr_snippets SET active = 0 WHERE id = 42;   -- retire one
```

Change a setting the same way (`countdown_seconds`, `chat_history`, `race_seconds`,
`playlist_size`):

```sql
UPDATE cr_config SET value = '60' WHERE name = 'race_seconds';
```

`cr_config` is seeded from the matching environment variable on first start, so `.env` still
sets the initial values; afterwards the table wins.

## Add snippets to the seed

Append a `snip(level, topic, code)` entry to the matching list in `snippets.py`:

```python
snip("medium", "algorithms", r'''
def bubble(items):
    for i in range(len(items)):
        for j in range(len(items) - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items
'''),
```

Use a raw string (`r'''`) so escapes like `
` stay literal. Leading indentation is
preserved, trailing whitespace is stripped, and an unknown level or topic raises at import
time rather than failing quietly.

## LAN play

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Friends open `http://<your-lan-ip>:8000`. Lobbies live in memory, so a restart clears them.

## Deploy (game panel)

The panel fetches this repo into `/home/container` on every server start and installs
`requirements.txt`, then runs the entry file from the **Startup** tab.

- **Entry file:** `main.py` — running it directly starts uvicorn.
- **Port:** taken from the panel-injected `SERVER_PORT` (falls back to `PORT`, then `8000`).
  Never hardcode it, or nothing outside the container can reach the app.
- **Health check:** `GET /healthz`.
- **Updates:** the latest commit is fetched at server start, not on push — restart after
  pushing, or tick *"Restart the server when someone pushes to this branch"*.
- **Static/paths:** resolved from the file's own directory, so the working directory
  does not matter.

### `.env`

`.env` is gitignored and is **not** copied by the fetch. Upload it through the **Files**
tab and keep a local copy — `/home/container` is replaced on every start.

Copy `.env.example` to `.env` as the starting point. Leave `SERVER_PORT` unset in
production so the panel's injected value wins.

| var | default | role |
| --- | --- | --- |
| `SERVER_PORT` | injected | listen port (panel-supplied) |
| `HOST` | `0.0.0.0` | bind address |
| `APP_TITLE` | `Code Typing Race` | FastAPI title |
| `LOG_LEVEL` | `info` | uvicorn log level |
| `COUNTDOWN_SECONDS` | `5` | pre-race countdown |
| `CHAT_HISTORY` | `100` | chat messages kept per lobby |
| `WS_PING_INTERVAL` / `WS_PING_TIMEOUT` | `20` | websocket keepalive, raise if a proxy drops idle sockets |
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DATABASE` | unset | accounts, avatars and race history |
| `DATABASE_URL` | unset | alternative to the five `MYSQL_*` vars; a `jdbc:` prefix and percent-encoded passwords are accepted |
| `MYSQL_CONNECT_TIMEOUT` | `8` | seconds before giving up on the database |
| `LIBRARY_REFRESH_SECONDS` | `60` | how often the snippet library and settings are re-read |
| `SITE_URL` | `https://coderace.renode.space` | absolute origin for canonical and Open Graph tags |
| `IP_AUTOLOGIN` | `1` | re-attach a cookie-less visitor to the last account seen from their IP |
| `COUNTDOWN_SECONDS` / `CHAT_HISTORY` / `RACE_SECONDS` / `PLAYLIST_SIZE` | see above | seed values for `cr_config` on first start |

Leave the database vars unset to run with accounts disabled and the seed snippets in use.
Tables (`cr_users`, `cr_user_ips`, `cr_races`, `cr_snippets`, `cr_config`) are created
automatically on first start. If the database is
unreachable the app logs a warning and serves the game without accounts rather than failing.

### Cache busting

`index.html` is templated, and the `app.js` / `style.css` URLs get a `?v=<stamp>` taken from
their modification time. A browser or proxy that cached the old JavaScript therefore cannot
pair it with newer markup - which previously threw
`Cannot set properties of null (setting 'onclick')` on the first element that had been
removed, and killed the whole page. The event wiring is also bound through a guarded helper
now, so a single missing element warns instead of aborting the rest of the script.

### Reverse proxy

`deploy/nginx.conf` is a working config with placeholders for the domain and the
container's address. The parts that matter:

- `proxy_http_version 1.1` plus the `Upgrade` / `Connection` headers — without them
  `/ws/{code}` arrives as a plain GET, which a websocket route does not match, so the app
  answers **404** and multiplayer silently never connects. **Every** hostname the app serves
  needs this, not just the first one.
- The `map $http_upgrade $connection_upgrade` block belongs in `http{}`, not `server{}`.
- `X-Forwarded-Proto $scheme` — the app uses it to mark its cookie `Secure` on HTTPS.
- `X-Forwarded-For` — the source of the stored client IP.
- `proxy_read_timeout 3600s` — lobbies hold a socket open while idle.
- `client_max_body_size 2m` — headroom over the 512 KB avatar cap.
