"""Bot opponents: a fixed roster with ratings and generated avatars.

Each bot types at a target speed with a little jitter and the odd stumble, so a
race against one feels less metronomic than a straight timer.
"""
import hashlib
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

BY_SLUG: Dict[str, dict] = {b["slug"]: b for b in BOTS}

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
