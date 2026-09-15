"""Fill the committed nginx templates in with real values.

    python tools/make_nginx.py

Reads the placeholder vhosts in `deploy/`, substitutes the domains and backend
address, and writes the result to `deploy/local/` - which is gitignored, so the
container's address never lands in a public repository.

Values come from .env (also gitignored) or the environment:

    NGINX_PRIMARY=race.example.com
    NGINX_SECOND=typing.example.com
    NGINX_BACKEND=10.0.0.5:8000

or straight from the command line:

    python tools/make_nginx.py --backend 10.0.0.5:8000 \
        --primary race.example.com --second typing.example.com
"""
import argparse
import os
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
DEPLOY = BASE / "deploy"
OUT = DEPLOY / "local"

# What the committed templates use as placeholders.
PLACEHOLDER_PRIMARY = "coderace.example.com"
PLACEHOLDER_SECOND = "typing.example.com"
PLACEHOLDER_BACKEND = "CONTAINER_IP:CONTAINER_PORT"

# Nothing real is hardcoded here: the deployment's own values live in .env.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE / ".env")
except ImportError:  # dotenv is optional; plain env vars still work
    pass

PRIMARY = os.environ.get("NGINX_PRIMARY", "").strip() or PLACEHOLDER_PRIMARY
SECOND = os.environ.get("NGINX_SECOND", "").strip() or PLACEHOLDER_SECOND
BACKEND = os.environ.get("NGINX_BACKEND", "").strip() or PLACEHOLDER_BACKEND

TEMPLATES = (
    ("nginx-coderace.conf", "{primary}.conf"),
    ("nginx-typing.conf", "{second}.conf"),
    ("nginx-typing-redirect.conf", "{second}-redirect.conf"),
)


def render(template: str, primary: str, second: str, backend: str) -> str:
    text = (DEPLOY / template).read_text(encoding="utf-8")
    text = text.replace(PLACEHOLDER_PRIMARY, primary)
    text = text.replace(PLACEHOLDER_SECOND, second)
    text = text.replace(PLACEHOLDER_BACKEND, backend)
    header = (
        "# Generated from deploy/%s with the real domain and backend filled in.\n"
        "# This folder is gitignored - the backend address is not committed.\n"
        "# Regenerate with: python tools/make_nginx.py\n\n" % template
    )
    return header + text


def main(argv) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", default=PRIMARY, help="canonical domain")
    parser.add_argument("--second", default=SECOND, help="the other domain")
    parser.add_argument("--backend", default=BACKEND, help="host:port of the app")
    args = parser.parse_args(argv[1:])

    missing = [t for t, _ in TEMPLATES if not (DEPLOY / t).is_file()]
    if missing:
        print("missing template(s):", ", ".join(missing))
        return 1

    if args.backend == PLACEHOLDER_BACKEND:
        print("No backend address set.")
        print("Put NGINX_BACKEND=host:port in .env, or pass --backend host:port.")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    for template, pattern in TEMPLATES:
        name = pattern.format(primary=args.primary, second=args.second)
        (OUT / name).write_text(
            render(template, args.primary, args.second, args.backend),
            encoding="utf-8",
        )
        print("wrote", (OUT / name).as_posix().replace(BASE.as_posix() + "/", ""))

    print()
    print("Paste %s.conf into the %s vhost," % (args.primary, args.primary))
    print("and %s.conf into the %s vhost." % (args.second, args.second))
    print("Then: nginx -t && systemctl reload nginx")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
