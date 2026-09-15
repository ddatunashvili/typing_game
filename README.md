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

- Pick a language (15 available), then **Practice solo** or **Create lobby**.
- Share the invite link (the code pill copies it) or the 5-char code — friends paste it into **Join**.
- Host presses **Start race**; a race also auto-starts when everyone is Ready.
- 5s countdown, then everyone types the same snippet. Chat lives in the left panel.
- Live WPM / accuracy / progress bars per player, results table with placements.

## Typing rules

- Wrong key marks the character red and blocks — press the right key or Backspace.
- Pressing Enter auto-skips the next line's indentation (like typer.io).
- Untyped code is dimmed; typed code lights up in full syntax color.

## Layout

| file | role |
| --- | --- |
| `main.py` | FastAPI app, lobby state machine, `/ws/{code}` websocket |
| `snippets.py` | snippet library per language |
| `static/app.js` | typing engine, per-char highlighting, lobby client |
| `static/style.css` | dark theme |
| `static/index.html` | markup + Prism component loading |

## API

- `GET /api/languages` — language list
- `GET /api/snippet?lang=python` — random snippet (solo mode)
- `GET /api/lobby/new?lang=python` — create lobby, returns code
- `WS /ws/{code}?name=&pid=&create=0|1&lang=` — lobby socket

Client → server: `chat`, `ready`, `start`, `again`, `lang`, `progress`, `finish`
Server → client: `hello`, `state`, `chat`, `countdown`, `go`, `prog`, `error`

## Add snippets

Append strings to the matching list in `snippets.py` — leading indentation is preserved,
trailing whitespace is stripped automatically.

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
