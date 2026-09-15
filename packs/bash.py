"""Bash snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Everything is tagged
`devops`; the level does the sorting, from a one-line echo up to traps,
process substitution and locking.
"""
LANGUAGE = "bash"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "hello world"
''', r'''$ ./hello.sh
hello world'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

name="ada"
echo "hello ${name}"
''', r'''$ ./greet.sh
hello ada'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

for i in 1 2 3; do
  echo "$i"
done
''', r'''$ ./count.sh
1
2
3'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

pwd
ls -la
''', r'''$ ./where.sh
/home/container
total 76
drwxr-xr-x 1 app app 0 Sep 16 09:14 .'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

mkdir -p build/logs
touch build/logs/app.log
''', r'''$ ./setup.sh
$ ls build/logs
app.log'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

cp config.example.yml config.yml
mv old.log archive/old.log
''', r'''$ ./move.sh
$ ls archive
old.log'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

if [[ -f .env ]]; then
  echo "found .env"
else
  echo "no .env"
fi
''', r'''$ ./check.sh
no .env'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

count=$(ls -1 | wc -l)
echo "${count} entries"
''', r'''$ ./count.sh
11 entries'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "$HOME"
echo "$USER"
''', r'''$ ./who.sh
/home/container
app'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

grep -n "error" app.log
''', r'''$ ./errors.sh
14:[12:01:02] error: connection reset'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

head -n 3 names.txt
tail -n 2 names.txt
''', r'''$ ./peek.sh
ada
grace
linus
grace
linus'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "started at $(date +%H:%M)"
''', r'''$ ./now.sh
started at 09:14'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

read -r -p "Name: " name
echo "hello ${name}"
''', r'''$ ./ask.sh
Name: ada
hello ada'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "first: $1"
echo "count: $#"
''', r'''$ ./args.sh a b
first: a
count: 2'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

total=$((2 + 3))
echo "$total"
''', r'''$ ./math.sh
5'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

files=(a.txt b.txt c.txt)
echo "${#files[@]} files"
echo "${files[0]}"
''', r'''$ ./list.sh
3 files
a.txt'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "to stdout"
echo "to stderr" >&2
''', r'''$ ./streams.sh 2>/dev/null
to stdout'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

cat names.txt | sort | uniq
''', r'''$ ./unique.sh
ada
grace
linus'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

chmod +x deploy.sh
./deploy.sh
''', r'''$ ./run.sh
deploying...'''),
    ("very-easy", "devops", r'''
#!/usr/bin/env bash

echo "done" > result.txt
cat result.txt
''', r'''$ ./write.sh
done'''),

    # --------------------------------------------------------------------- easy
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

for file in ./logs/*.log; do
  echo "== $file"
  tail -n 5 "$file"
done
''', r'''$ ./tail-logs.sh
== ./logs/app.log
[12:01:44] request finished in 31ms
== ./logs/error.log
[12:01:02] connection reset'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"

if ! command -v psql >/dev/null 2>&1; then
  echo "psql not installed" >&2
  exit 1
fi
''', r'''$ ./check.sh
./check.sh: line 4: DATABASE_URL: DATABASE_URL is required'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

greet() {
  local name="${1:-world}"
  echo "hello ${name}"
}

greet
greet "ada"
''', r'''$ ./greet.sh
hello world
hello ada'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

while IFS= read -r line; do
  echo "line: $line"
done < names.txt
''', r'''$ ./each.sh
line: ada
line: grace
line: linus'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  start) echo "starting" ;;
  stop) echo "stopping" ;;
  *)
    echo "usage: $0 {start|stop}" >&2
    exit 64
    ;;
esac
''', r'''$ ./svc.sh
usage: ./svc.sh {start|stop}'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

count=$(grep -c "error" app.log || true)
if (( count > 0 )); then
  echo "${count} errors found"
fi
''', r'''$ ./errors.sh
3 errors found'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

find . -name "*.tmp" -type f -print -delete
''', r'''$ ./clean.sh
./build/a.tmp
./build/b.tmp'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

awk -F, '{ total += $2 } END { printf "%.1f\n", total / NR }' races.csv
''', r'''$ ./mean.sh
94.5'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

sed -i.bak 's/DEBUG=1/DEBUG=0/' .env
diff .env.bak .env || true
''', r'''$ ./prod.sh
< DEBUG=1
> DEBUG=0'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

if curl -fsS "http://127.0.0.1:${PORT:-8000}/healthz" >/dev/null; then
  echo "healthy"
else
  echo "unhealthy" >&2
  exit 1
fi
''', r'''$ ./ping.sh
healthy'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

branch=$(git rev-parse --abbrev-ref HEAD)
echo "on ${branch}"
git status --short
''', r'''$ ./status.sh
on master
 M main.py'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

tar -czf "backup-$(date +%F).tar.gz" data/
ls -lh backup-*.tar.gz
''', r'''$ ./backup.sh
-rw-r--r-- 1 app app 4.2M backup-2026-09-16.tar.gz'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

for host in web1 web2 web3; do
  echo "== ${host}"
  ssh "${host}" "uptime" || echo "  unreachable" >&2
done
''', r'''$ ./uptime.sh
== web1
 09:14:02 up 12 days,  load average: 0.14'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

target="${1:?usage: $0 <dir>}"
du -sh "${target}"/* | sort -hr | head -n 5
''', r'''$ ./biggest.sh /var/log
412M	/var/log/journal
 88M	/var/log/nginx'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${CI:-}" ]]; then
  echo "running locally"
else
  echo "running in CI"
fi
''', r'''$ ./where.sh
running locally'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
''', r'''$ ./bootstrap.sh
$ which python
/home/container/.venv/bin/python'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

printf "%-12s %s\n" "name" "wpm"
printf "%-12s %s\n" "ada" "118"
''', r'''$ ./table.sh
name         wpm
ada          118'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

files=$(git diff --name-only --cached)
if [[ -n "$files" ]]; then
  echo "$files" | xargs -r python -m py_compile
fi
''', r'''$ ./pre-commit.sh
(no output: every staged file compiled)'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

docker compose up -d
docker compose ps --format "table {{.Name}}\t{{.Status}}"
''', r'''$ ./up.sh
NAME        STATUS
app         Up 2 seconds
db          Up 2 seconds'''),
    ("easy", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

jq -r '.dependencies | keys[]' package.json
''', r'''$ ./deps.sh
react
react-dom'''),

    # ------------------------------------------------------------------- medium
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

deploy() {
  local env="$1"
  if [[ -z "$env" ]]; then
    echo "usage: deploy <env>" >&2
    return 1
  fi
  docker build -t app:"$env" .
  docker push registry.local/app:"$env"
}
''', r'''$ deploy staging
Successfully tagged app:staging
The push refers to repository [registry.local/app]'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

tar -czf "$workdir/backup.tar.gz" -C /var/lib/app data
find /backups -name '*.tar.gz' -mtime +14 -delete
mv "$workdir/backup.tar.gz" "/backups/app-$(date +%F).tar.gz"
''', r'''$ ./backup.sh
$ ls /backups
app-2026-09-16.tar.gz'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

usage() { echo "usage: $0 [-e env] [-t tag] [-v]" >&2; exit 64; }

env="staging"
tag="latest"
verbose=0

while getopts ":e:t:v" opt; do
  case "$opt" in
    e) env="$OPTARG" ;;
    t) tag="$OPTARG" ;;
    v) verbose=1 ;;
    \?) usage ;;
  esac
done
shift $(( OPTIND - 1 ))

(( verbose )) && set -x
echo "deploying ${tag} to ${env}"
''', r'''$ ./deploy.sh -e prod -t v1.4.2
deploying v1.4.2 to prod'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

port="${SERVER_PORT:-8000}"
retries=10

while (( retries > 0 )); do
  if curl -fsS "http://127.0.0.1:${port}/healthz" >/dev/null; then
    echo "healthy on ${port}"
    exit 0
  fi
  retries=$(( retries - 1 ))
  sleep 2
done

echo "service never became healthy" >&2
exit 1
''', r'''$ ./healthcheck.sh
healthy on 25616'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

log() {
  printf '[%s] %s\n' "$(date -u +%H:%M:%S)" "$*" >&2
}

die() {
  log "ERROR: $*"
  exit 1
}

log "starting"
[[ -f .env ]] || die ".env is missing"
''', r'''$ ./run.sh
[09:14:02] starting
[09:14:02] ERROR: .env is missing'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

declare -A limits=(
  [cpu]="2"
  [memory]="1Gi"
)

for key in "${!limits[@]}"; do
  echo "${key}=${limits[$key]}"
done
''', r'''$ ./limits.sh
cpu=2
memory=1Gi'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

while IFS='=' read -r key value; do
  [[ "$key" =~ ^#|^$ ]] && continue
  export "${key}=${value}"
done < .env

echo "port is ${SERVER_PORT}"
''', r'''$ ./load-env.sh
port is 25616'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

mapfile -t branches < <(git for-each-ref --format='%(refname:short)' refs/heads)

for branch in "${branches[@]}"; do
  merged=$(git branch --merged master --format='%(refname:short)' | grep -Fx "$branch" || true)
  [[ -n "$merged" && "$branch" != "master" ]] && git branch -d "$branch"
done
''', r'''$ ./prune.sh
Deleted branch feature/stars (was 4af930b).'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

if ! diff <(sort expected.txt) <(sort actual.txt) >/dev/null; then
  echo "output differs:" >&2
  diff <(sort expected.txt) <(sort actual.txt) >&2 || true
  exit 1
fi
echo "match"
''', r'''$ ./verify.sh
match'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

total=0
while read -r _ size _; do
  total=$(( total + size ))
done < <(ls -l --time-style=+ | tail -n +2)

echo "$(( total / 1024 )) KiB"
''', r'''$ ./size.sh
1284 KiB'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

retry() {
  local attempts="$1"; shift
  local n=0
  until "$@"; do
    n=$(( n + 1 ))
    (( n >= attempts )) && return 1
    sleep $(( 2 ** n ))
  done
}

retry 3 curl -fsS https://api.example.com/health
''', r'''$ ./retry.sh
(succeeds, or exits 1 after three tries)'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  local code=$?
  [[ -n "${container:-}" ]] && docker rm -f "$container" >/dev/null 2>&1
  exit "$code"
}
trap cleanup EXIT INT TERM

container=$(docker run -d postgres:16)
echo "started ${container:0:12}"
''', r'''$ ./with-db.sh
started 4f2a91c3b8de'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

version=$(grep -oP '(?<=^version = ")[^"]+' pyproject.toml)
next="${version%.*}.$(( ${version##*.} + 1 ))"
sed -i "s/^version = \"${version}\"/version = \"${next}\"/" pyproject.toml
echo "${version} -> ${next}"
''', r'''$ ./bump.sh
1.4.2 -> 1.4.3'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

find . -type f -name '*.py' -print0 \
  | xargs -0 -P "$(nproc)" -n 20 python -m py_compile
echo "compiled everything"
''', r'''$ ./compile-all.sh
compiled everything'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

logfile="/var/log/app.log"
if [[ $(stat -c%s "$logfile") -gt 10485760 ]]; then
  mv "$logfile" "${logfile}.$(date +%s)"
  : > "$logfile"
  echo "rotated"
fi
''', r'''$ ./rotate.sh
rotated'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

status=$(curl -s -o /dev/null -w '%{http_code}' "$1")
case "$status" in
  2??) echo "ok ($status)" ;;
  3??) echo "redirect ($status)" ;;
  4??) echo "client error ($status)"; exit 1 ;;
  *)   echo "server error ($status)"; exit 1 ;;
esac
''', r'''$ ./probe.sh https://coderace.example.com
ok (200)'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

jq -r '.rows[] | [.name, .rating] | @tsv' <<<"$(curl -fsS /api/rankings)" \
  | sort -k2 -nr \
  | head -n 5
''', r'''$ ./top.sh
ada	1504
grace	1390'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

self="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(cd "${self}/.." && pwd)"

cd "$root"
echo "repo root: $root"
''', r'''$ tools/where.sh
repo root: /home/container'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--dry-run" ]]; then
  run() { echo "would run: $*"; }
else
  run() { "$@"; }
fi

run rm -rf build/
run docker system prune -f
''', r'''$ ./clean.sh --dry-run
would run: rm -rf build/
would run: docker system prune -f'''),
    ("medium", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

sum_field() {
  local field="$1" file="$2"
  awk -F, -v f="$field" 'NR > 1 { total += $f } END { print total + 0 }' "$file"
}

echo "total wpm: $(sum_field 2 races.csv)"
''', r'''$ ./sum.sh
total wpm: 2931'''),

    ("medium", "devops", r"""
#!/usr/bin/env bash
set -euo pipefail

confirm() {
  local prompt="${1:-Are you sure?}"
  read -r -p "${prompt} [y/N] " reply
  [[ "${reply,,}" == y* ]]
}

if confirm "Drop the production database?"; then
  echo "dropping"
else
  echo "cancelled"
fi
""", r"""$ ./danger.sh
Drop the production database? [y/N] n
cancelled"""),
    ("medium", "devops", r"""
#!/usr/bin/env bash
set -euo pipefail

require() {
  local missing=()
  local tool
  for tool in "$@"; do
    command -v "$tool" >/dev/null 2>&1 || missing+=("$tool")
  done
  if (( ${#missing[@]} )); then
    printf 'missing tools: %s\n' "${missing[*]}" >&2
    exit 1
  fi
}

require git docker jq
echo "all tools present"
""", r"""$ ./preflight.sh
missing tools: jq"""),

    # --------------------------------------------------------------------- hard
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s inherit_errexit nullglob

on_error() {
  local code=$? line=$1
  printf 'failed at line %s with status %s\n' "$line" "$code" >&2
  exit "$code"
}
trap 'on_error $LINENO' ERR

main() {
  echo "doing work"
  false
}

main "$@"
''', r'''$ ./strict.sh
doing work
failed at line 15 with status 1'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

lock="/var/lock/$(basename "$0").lock"
exec 9>"$lock"
if ! flock -n 9; then
  echo "another run is already in progress" >&2
  exit 75
fi

echo "holding the lock for $$"
sleep 5
''', r'''$ ./nightly.sh & ./nightly.sh
holding the lock for 4821
another run is already in progress'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

run_parallel() {
  local -a pids=()
  local host
  for host in "$@"; do
    ssh "$host" "systemctl restart app" &
    pids+=("$!")
  done

  local failed=0 pid
  for pid in "${pids[@]}"; do
    wait "$pid" || failed=$(( failed + 1 ))
  done
  (( failed == 0 )) || { echo "${failed} host(s) failed" >&2; return 1; }
}

run_parallel web1 web2 web3
''', r'''$ ./restart-all.sh
1 host(s) failed'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

declare -A counts=()
while IFS= read -r line; do
  [[ "$line" =~ \"([A-Z]+)\ ([^\"]+)\" ]] || continue
  counts["${BASH_REMATCH[1]} ${BASH_REMATCH[2]%%\?*}"]+=x
done < access.log

for route in "${!counts[@]}"; do
  printf '%6d %s\n' "${#counts[$route]}" "$route"
done | sort -rn | head
''', r'''$ ./routes.sh
  1841 GET /
   402 GET /api/rankings'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

blue_green() {
  local next="$1" current
  current=$(docker ps --filter "label=role=live" --format '{{.Names}}' | head -n1)

  docker run -d --label role=candidate --name "$next" app:latest
  until curl -fsS "http://${next}:8000/healthz" >/dev/null; do sleep 1; done

  docker label "$next" role=live
  [[ -n "$current" ]] && docker rm -f "$current"
  echo "live is now ${next}"
}

blue_green "app-$(date +%s)"
''', r'''$ ./switch.sh
live is now app-1789456200'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE' >&2
usage: backup.sh [options] <target>

  -d, --dest DIR     where to write the archive (default: /backups)
  -k, --keep N       how many archives to keep (default: 14)
  -n, --dry-run      print what would happen
  -h, --help         this text
USAGE
  exit 64
}

dest=/backups keep=14 dry=0
while (( $# )); do
  case "$1" in
    -d|--dest) dest="$2"; shift 2 ;;
    -k|--keep) keep="$2"; shift 2 ;;
    -n|--dry-run) dry=1; shift ;;
    -h|--help) usage ;;
    --) shift; break ;;
    -*) echo "unknown option: $1" >&2; usage ;;
    *) break ;;
  esac
done
[[ $# -eq 1 ]] || usage
''', r'''$ ./backup.sh --help
usage: backup.sh [options] <target>
  -d, --dest DIR     where to write the archive (default: /backups)'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

with_timeout() {
  local seconds="$1"; shift
  "$@" &
  local pid=$!
  (
    sleep "$seconds"
    kill -TERM "$pid" 2>/dev/null && echo "timed out after ${seconds}s" >&2
  ) &
  local watcher=$!
  wait "$pid" 2>/dev/null
  local code=$?
  kill "$watcher" 2>/dev/null || true
  return "$code"
}

with_timeout 5 curl -fsS https://slow.example.com
''', r'''$ ./timeout.sh
timed out after 5s'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

migrate() {
  local dir="$1" applied
  applied=$(psql -Atqc "SELECT name FROM schema_migrations" 2>/dev/null || true)

  local file name
  for file in "$dir"/*.sql; do
    name=$(basename "$file")
    grep -Fxq "$name" <<<"$applied" && continue

    echo "applying ${name}"
    psql -1 -v ON_ERROR_STOP=1 -f "$file"
    psql -c "INSERT INTO schema_migrations (name) VALUES ('${name}')"
  done
}

migrate ./migrations
''', r'''$ ./migrate.sh
applying 003_add_ratings.sql'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

progress() {
  local total="$1" done="$2" width=40
  local filled=$(( done * width / total ))
  printf '\r[%-*s] %3d%%' "$width" "$(printf '#%.0s' $(seq 1 "$filled"))" \
    "$(( done * 100 / total ))"
}

for i in $(seq 1 20); do
  progress 20 "$i"
  sleep 0.05
done
printf '\n'
''', r'''$ ./progress.sh
[########################################] 100%'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

assert_eq() {
  local expected="$1" actual="$2" label="${3:-assertion}"
  if [[ "$expected" != "$actual" ]]; then
    printf 'FAIL %s\n  expected: %s\n  actual:   %s\n' "$label" "$expected" "$actual" >&2
    return 1
  fi
  printf 'ok   %s\n' "$label"
}

assert_eq "5" "$(echo $(( 2 + 3 )))" "arithmetic"
assert_eq "ada" "$(head -n1 names.txt)" "first name"
''', r'''$ ./test.sh
ok   arithmetic
ok   first name'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  printf '"%s"' "$s"
}

printf '{"level":%s,"message":%s}\n' \
  "$(json_escape "info")" "$(json_escape "deploy \"v1.4\" done")"
''', r'''$ ./log-json.sh
{"level":"info","message":"deploy \"v1.4\" done"}'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

watch_dir() {
  local dir="$1"; shift
  inotifywait -m -r -e close_write --format '%w%f' "$dir" \
  | while IFS= read -r changed; do
      case "$changed" in
        *.py|*.js|*.css) "$@" ;;
      esac
    done
}

watch_dir ./static pkill -HUP -f 'python main.py'
''', r'''$ ./watch.sh
(reloads the server whenever a source file is saved)'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

declare -r remote="${1:?usage: $0 user@host}"

rsync -az --delete \
  --exclude '.git/' \
  --exclude '__pycache__/' \
  --exclude '.env' \
  --filter=':- .gitignore' \
  ./ "${remote}:/srv/app/"

ssh "$remote" 'cd /srv/app && systemctl restart app && systemctl is-active app'
''', r'''$ ./push.sh app@web1
active'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

summarise() {
  awk -F, '
    NR == 1 { next }
    {
      count[$1]++
      total[$1] += $2
      if ($2 > best[$1]) best[$1] = $2
    }
    END {
      printf "%-10s %6s %8s %6s\n", "language", "races", "avg", "best"
      for (lang in count) {
        printf "%-10s %6d %8.1f %6d\n", lang, count[lang], total[lang] / count[lang], best[lang]
      }
    }
  ' "$1"
}

summarise races.csv
''', r'''$ ./report.sh
language    races      avg   best
python         31     96.4    118
rust           12     91.8    104'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

secret() {
  local name="$1" file="/run/secrets/${1}"
  if [[ -r "$file" ]]; then
    cat "$file"
  elif [[ -n "${!name:-}" ]]; then
    printf '%s' "${!name}"
  else
    echo "secret ${name} is not available" >&2
    return 1
  fi
}

DB_PASSWORD="$(secret MYSQL_PASSWORD)"
export DB_PASSWORD
''', r'''$ ./load-secrets.sh
(reads /run/secrets first, then falls back to the environment)'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

trap 'echo; echo "interrupted, cleaning up"; jobs -p | xargs -r kill; exit 130' INT

tail -F /var/log/app.log | grep --line-buffered ERROR &
tail -F /var/log/nginx/error.log &

wait
''', r'''$ ./watch-errors.sh
^C
interrupted, cleaning up'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

checksum_tree() {
  find "$1" -type f -not -path '*/.git/*' -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    | sha256sum \
    | cut -d' ' -f1
}

before=$(checksum_tree ./static)
npm run build >/dev/null
after=$(checksum_tree ./static)

[[ "$before" == "$after" ]] && echo "no change" || echo "assets changed"
''', r'''$ ./verify-build.sh
assets changed'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

exec 3< <(curl -fsSN "https://api.example.com/events")

while IFS= read -r -u 3 line; do
  [[ "$line" == data:* ]] || continue
  payload="${line#data: }"
  jq -r '"\(.type) \(.id)"' <<<"$payload"
done

exec 3<&-
''', r'''$ ./stream.sh
race_finished 1041
race_finished 1042'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

colour() {
  local code="$1"; shift
  if [[ -t 1 ]]; then
    printf '\033[%sm%s\033[0m\n' "$code" "$*"
  else
    printf '%s\n' "$*"
  fi
}

ok()   { colour '32' "  ok   $*"; }
warn() { colour '33' "  warn $*"; }
fail() { colour '31' "  fail $*"; }

ok "database reachable"
warn "no .env found, using defaults"
fail "port 25616 already bound"
''', r'''$ ./doctor.sh
  ok   database reachable
  warn no .env found, using defaults
  fail port 25616 already bound'''),
    ("hard", "devops", r'''
#!/usr/bin/env bash
set -euo pipefail

self_update() {
  local remote="https://example.com/install.sh"
  local tmp; tmp="$(mktemp)"
  trap 'rm -f "$tmp"' RETURN

  curl -fsS "$remote" -o "$tmp"
  if ! sha256sum -c <<<"$(cat install.sha256)  $tmp" >/dev/null 2>&1; then
    echo "checksum mismatch, refusing to install" >&2
    return 1
  fi
  install -m 0755 "$tmp" "$0"
  echo "updated $0"
}

self_update
''', r'''$ ./install.sh
checksum mismatch, refusing to install'''),
]
