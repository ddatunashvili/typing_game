"""Bot opponents: a fixed roster with ratings and generated avatars.

Each bot types at a target speed with a little jitter and the odd stumble, so a
race against one feels less metronomic than a straight timer.
"""
import hashlib
import pathlib
from typing import Dict, List, Optional

import rating

# wpm = target typing speed, acc = the accuracy it reports,
# stumble = chance per tick of a short hesitation.
BOTS: List[dict] = [
    {
        "slug": "rubber-duck",
        "name": "Rubber Duck",
        "rating": 750,
        "wpm": 18,
        "acc": 99.0,
        "stumble": 0.04,
        "blurb": "Listens to your problems. Types slowly.",
    },
    {
        "slug": "copy-paste-carl",
        "name": "Copy-Paste Carl",
        "rating": 900,
        "wpm": 28,
        "acc": 91.0,
        "stumble": 0.10,
        "blurb": "Ships whatever the top answer said.",
    },
    {
        "slug": "off-by-one-olga",
        "name": "Off-By-One Olga",
        "rating": 1040,
        "wpm": 36,
        "acc": 93.0,
        "stumble": 0.08,
        "blurb": "Always one character short.",
    },
    {
        "slug": "semicolon-sam",
        "name": "Semicolon Sam",
        "rating": 1150,
        "wpm": 44,
        "acc": 95.0,
        "stumble": 0.06,
        "blurb": "Never forgets one. Ever.",
    },
    {
        "slug": "tabs-mcspaces",
        "name": "Tabs McSpaces",
        "rating": 1260,
        "wpm": 52,
        "acc": 94.0,
        "stumble": 0.07,
        "blurb": "Starts a war in every code review.",
    },
    {
        "slug": "null-pointer-pete",
        "name": "Null Pointer Pete",
        "rating": 1370,
        "wpm": 60,
        "acc": 96.0,
        "stumble": 0.05,
        "blurb": "Dereferences first, checks later.",
    },
    {
        "slug": "merge-conflict-marge",
        "name": "Merge Conflict Marge",
        "rating": 1480,
        "wpm": 68,
        "acc": 95.5,
        "stumble": 0.06,
        "blurb": "Rebases on Friday afternoon.",
    },
    {
        "slug": "yaml-yolanda",
        "name": "YAML Yolanda",
        "rating": 1590,
        "wpm": 76,
        "acc": 97.0,
        "stumble": 0.04,
        "blurb": "Indentation is a personality trait.",
    },
    {
        "slug": "regex-randy",
        "name": "Regex Randy",
        "rating": 1700,
        "wpm": 85,
        "acc": 97.5,
        "stumble": 0.03,
        "blurb": "Solved it with one unreadable line.",
    },
    {
        "slug": "infinite-loop-ian",
        "name": "Infinite Loop Ian",
        "rating": 1820,
        "wpm": 95,
        "acc": 98.0,
        "stumble": 0.03,
        "blurb": "while (true) { keep typing }",
    },
    {
        "slug": "race-condition-rita",
        "name": "Race Condition Rita",
        "rating": 1950,
        "wpm": 108,
        "acc": 98.2,
        "stumble": 0.02,
        "blurb": "Finishes before she starts. Sometimes.",
    },
    {
        "slug": "segfault-sally",
        "name": "Segfault Sally",
        "rating": 2080,
        "wpm": 122,
        "acc": 98.6,
        "stumble": 0.02,
        "blurb": "Core dumped, race won.",
    },
    {
        "slug": "kernel-panic-kim",
        "name": "Kernel Panic Kim",
        "rating": 2250,
        "wpm": 138,
        "acc": 99.0,
        "stumble": 0.01,
        "blurb": "Types in ring 0.",
    },
]

# Trash talk. Fired at random while a bot is typing - rough, but aimed at the
# code and the clock, never at the person.
ROASTS: Dict[str, List[str]] = {
    "rubber-duck": [
        "quack. that was your best line?",
        "i float. you sink.",
        "explain your bug to me. slowly. i have time.",
        "i am a bath toy and i am still in this race.",
        "take your time. i literally cannot drown.",
    ],
    "copy-paste-carl": [
        "did you write that or did you remember it?",
        "ctrl+c is a skill. yours is not.",
        "i shipped this exact function nine times today.",
        "no idea what this does. still faster than you.",
        "the top answer never asks questions.",
    ],
    "off-by-one-olga": [
        "you missed a character. i can tell from here.",
        "i am always one short and still ahead of you.",
        "arrays start at 0. your wpm starts lower.",
        "one more keystroke. you can manage one, surely.",
        "off by one. you are off by forty.",
    ],
    "semicolon-sam": [
        "you forgot one. you always forget one.",
        "i never miss a semicolon. you never hit a target.",
        "that was a syntax error waiting to happen.",
        "punctuation is not optional. neither is speed.",
        "i can hear you hunting for the bracket key.",
    ],
    "tabs-mcspaces": [
        "your indentation is a cry for help.",
        "four spaces. or a tab. pick a side and type faster.",
        "i have started wars over less than your formatting.",
        "the linter is going to have a field day with you.",
        "whitespace is free. your time is not.",
    ],
    "null-pointer-pete": [
        "i checked for null. i did not check for competition.",
        "your race is throwing. handle it.",
        "somewhere a reference is pointing at your wpm. it is null.",
        "dereference first. apologise later.",
        "segmentation fault: your typing.",
    ],
    "merge-conflict-marge": [
        "i would rebase your run but there is nothing worth keeping.",
        "this is going to be a painful merge for you.",
        "force push. it is the only way you are catching me.",
        "i rebase on friday. you cannot beat me on a tuesday.",
        "your branch is behind. by a lot.",
    ],
    "yaml-yolanda": [
        "two spaces. two. it is not complicated.",
        "your config is invalid and so is your pace.",
        "i indent in my sleep and still type faster.",
        "that keystroke was tabbed. i felt it.",
        "no, the colon goes there. keep up.",
    ],
    "regex-randy": [
        "i did that in one line. unreadable, but one line.",
        "/^too slow$/ matches your run.",
        "you type like you are escaping every character.",
        "greedy match. that is what i am doing to this race.",
        "i parsed HTML with a regex once. still faster than this.",
    ],
    "infinite-loop-ian": [
        "while (true) { beat you }",
        "no exit condition. no mercy.",
        "i do not stop. that is the whole problem.",
        "you will finish eventually. i will not.",
        "your loop is the one that needs breaking.",
    ],
    "race-condition-rita": [
        "i finished before you started. check the timestamps.",
        "no locks. no waiting. no chance.",
        "we both read the same snippet. only one of us wrote it.",
        "this race is not thread safe and neither are you.",
        "whoever commits first wins. that was me.",
    ],
    "segfault-sally": [
        "core dumped. race still won.",
        "i wrote past the end of the buffer and past you.",
        "your stack is deeper than your skill.",
        "free() called twice. your chances, once.",
        "i crash. i just crash faster than you type.",
    ],
    "kernel-panic-kim": [
        "i type in ring 0. you type in slow motion.",
        "your process has been scheduled. behind mine.",
        "i do not context switch. i just win.",
        "panic: no route to victory for you.",
        "uptime: 400 days. your lead: zero seconds.",
    ],
}

GENERIC_ROASTS = [
    "is that your typing speed or your loading screen?",
    "the snippet is right there. all of it.",
    "keep going. someone has to come second.",
]


def roasts(slug: str) -> List[str]:
    return ROASTS.get((slug or "").strip().lower()) or GENERIC_ROASTS


BY_SLUG: Dict[str, dict] = {b["slug"]: b for b in BOTS}

# Hand-drawn artwork, dropped in by tools/import_bot_avatars.py. Any bot without
# a file falls back to the generated identicon.
ART_DIR = pathlib.Path(__file__).resolve().parent / "static" / "bots"
ART_EXTS = (".webp", ".png", ".jpg", ".jpeg")
ART_TYPES = {
    ".webp": "image/webp",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def _find(stem: str) -> Optional[pathlib.Path]:
    for ext in ART_EXTS:
        candidate = ART_DIR / (stem + ext)
        if candidate.is_file():
            return candidate
    return None


def art(slug: str) -> Optional[pathlib.Path]:
    """The square avatar image for a bot, if one was imported."""
    return _find((slug or "").strip().lower())


def card_art(slug: str) -> Optional[pathlib.Path]:
    """The full character-card illustration, if one was imported."""
    return _find((slug or "").strip().lower() + "-card")


def media_type(path: pathlib.Path) -> str:
    return ART_TYPES.get(path.suffix.lower(), "application/octet-stream")

# Avatar palette: picked to stay legible on the dark theme.
PALETTE = [
    ("#6fe3a1", "#123021"),
    ("#62b6ff", "#101f33"),
    ("#ffc46b", "#332616"),
    ("#ff8fa3", "#331a20"),
    ("#c79bff", "#241933"),
    ("#7de0d8", "#0f2f2d"),
    ("#ffd166", "#332a12"),
    ("#9ae66e", "#1d3315"),
]


def public(bot: dict) -> dict:
    return {
        "slug": bot["slug"],
        "art": art(bot["slug"]) is not None,
        "card": card_art(bot["slug"]) is not None,
        "name": bot["name"],
        "rating": bot["rating"],
        "rank": rating.rank_for(bot["rating"]),
        "wpm": bot["wpm"],
        "blurb": bot["blurb"],
        "bot": True,
    }


def roster() -> List[dict]:
    return [public(b) for b in BOTS]


def get(slug: str) -> Optional[dict]:
    return BY_SLUG.get((slug or "").strip().lower())


def _bits(seed: str) -> bytes:
    return hashlib.sha256(seed.encode("utf-8")).digest()


def avatar_svg(seed: str) -> str:
    """A deterministic identicon, so a bot always looks the same.

    A 5x5 grid mirrored down the middle - the same trick GitHub used - drawn
    straight to SVG so nothing external has to be fetched.
    """
    data = _bits(seed)
    fg, bg = PALETTE[data[0] % len(PALETTE)]
    cells = []
    for col in range(3):
        for row in range(5):
            if data[2 + col * 5 + row] & 1:
                cells.append((col, row))
                if col < 2:  # mirror to the right-hand side
                    cells.append((4 - col, row))

    size, pad = 20, 0
    rects = "".join(
        f'<rect x="{pad + c * size}" y="{pad + r * size}" width="{size}" height="{size}"/>'
        for c, r in cells
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'width="100" height="100" shape-rendering="crispEdges">'
        f'<rect width="100" height="100" fill="{bg}"/>'
        f'<g fill="{fg}">{rects}</g>'
        "</svg>"
    )
