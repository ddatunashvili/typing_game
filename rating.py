"""Stars, Elo ratings and rank titles.

Stars score a single run the way a puzzle site does: how cleanly you typed it.
The rating is a normal Elo, updated from the finishing order of a race, so a win
against a stronger opponent is worth more.
"""
from typing import Dict, Iterable, List, Optional, Tuple

START_RATING = 1200
K_FACTOR = 24
MIN_RATING = 100

# Rating bands, low to high. The title shown next to a player's name.
RANKS: List[Tuple[int, str]] = [
    (0, "Rubber Duck"),
    (900, "Script Kiddie"),
    (1050, "Intern"),
    (1200, "Junior Dev"),
    (1350, "Mid Dev"),
    (1500, "Senior Dev"),
    (1650, "Tech Lead"),
    (1800, "Architect"),
    (1950, "Principal"),
    (2100, "10x Engineer"),
    (2300, "Kernel Hacker"),
]


def rank_for(rating: float) -> str:
    title = RANKS[0][1]
    for floor, name in RANKS:
        if rating >= floor:
            title = name
    return title


def rank_index(rating: float) -> int:
    idx = 0
    for i, (floor, _) in enumerate(RANKS):
        if rating >= floor:
            idx = i
    return idx


def ranks() -> List[dict]:
    return [{"floor": floor, "title": name} for floor, name in RANKS]


# ---------- stars ----------
def stars(
    accuracy: float,
    errors: int,
    length: int,
    completed: bool = True,
    won: bool = False,
) -> int:
    """0-3 stars for one run.

    Accuracy is the headline number and the error rate stops a long sloppy run
    from scoring well just because the percentage looks round. Winning the race
    is worth a star on top: out-typing everyone should not score below someone
    who was tidier over a third of the distance.
    """
    if not completed:
        return 0
    length = max(1, int(length))
    error_rate = max(0, int(errors)) / length

    if accuracy >= 96 and error_rate <= 0.04:
        earned = 3
    elif accuracy >= 88 and error_rate <= 0.12:
        earned = 2
    elif accuracy >= 72:
        earned = 1
    else:
        earned = 0

    if won and earned:
        earned = min(3, earned + 1)
    return earned


STAR_NOTES = {
    3: "Clean run",
    2: "Solid, a few slips",
    1: "Messy - lots of corrections",
    0: "Rough one",
}

# Bots type at a fixed synthetic accuracy, so a star rating for them would be
# meaningless and would flatter them against a real player.
BOT_STARS = -1


def star_note(count: int) -> str:
    return STAR_NOTES.get(count, "")


# ---------- elo ----------
def expected_score(rating: float, opponent: float) -> float:
    return 1.0 / (1.0 + 10 ** ((opponent - rating) / 400.0))


def score_against(my_place: Optional[int], their_place: Optional[int]) -> float:
    """1 for a win, 0.5 for a tie, 0 for a loss. Unfinished counts as last."""
    mine = my_place if my_place else 10_000
    theirs = their_place if their_place else 10_000
    if mine == theirs:
        return 0.5
    return 1.0 if mine < theirs else 0.0


def elo_delta(
    rating: float,
    place: Optional[int],
    opponents: Iterable[Tuple[float, Optional[int]]],
    k: int = K_FACTOR,
) -> int:
    """Rating change from one race, scored pairwise against every opponent."""
    pairs = list(opponents)
    if not pairs:
        return 0
    total = 0.0
    for opp_rating, opp_place in pairs:
        actual = score_against(place, opp_place)
        total += k * (actual - expected_score(rating, opp_rating))
    # average so a crowded lobby is not worth more than a duel
    return int(round(total / len(pairs)))


def apply_delta(rating: float, delta: int) -> int:
    return max(MIN_RATING, int(round(rating + delta)))


def race_deltas(entries: List[dict]) -> Dict[str, int]:
    """Rating change per entry.

    Each entry needs `key`, `rating` and `place`. Entries flagged `provisional`
    (bots) are used as opposition but get no change of their own.
    """
    out: Dict[str, int] = {}
    for entry in entries:
        if entry.get("provisional"):
            continue
        opponents = [
            (float(other["rating"]), other.get("place"))
            for other in entries
            if other is not entry
        ]
        out[entry["key"]] = elo_delta(
            float(entry["rating"]), entry.get("place"), opponents
        )
    return out
