"""Per-language snippet packs.

Each module in this package exposes:

    LANGUAGE = "python"
    SNIPPETS = [(level, topic, code, output), ...]

Plain tuples, deliberately: the packs must not import `snippets`, or the two
modules would import each other. `snippets.py` converts them with `snip()` and
skips anything whose code it already has, so a pack can safely restate a
snippet that started life inline.

Add a language by dropping in a new module - it is picked up automatically.
"""
import importlib
import pkgutil
from typing import Dict, List, Tuple

Entry = Tuple[str, str, str, str]


def load() -> Dict[str, List[Entry]]:
    """Every pack, keyed by language id."""
    out: Dict[str, List[Entry]] = {}
    for info in pkgutil.iter_modules(__path__):
        module = importlib.import_module("%s.%s" % (__name__, info.name))
        entries = getattr(module, "SNIPPETS", None)
        if not entries:
            continue
        language = getattr(module, "LANGUAGE", info.name)
        out.setdefault(language, []).extend(entries)
    return out
