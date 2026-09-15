"""Import bot avatar artwork into static/bots/.

    python tools/import_bot_avatars.py typing_bot_avatars.zip

The archive (or folder) holds one image per bot, named after the bot with
underscores, e.g. `null_pointer_pete.png` for the `null-pointer-pete` slug.

Two files come out of each source image:

  static/bots/<slug>.webp        256x256, cropped to the character's face
  static/bots/<slug>-card.webp   512px wide, the full artwork

The artwork is a character card with the blurb printed across the top and a
rating badge across the bottom, so a plain centre crop would slice through the
text. The avatar crop therefore takes the middle band only, which is where the
face sits, while the card keeps the whole illustration.

Dev-only: the server never needs Pillow. Re-run it if the art changes.
"""
import io
import pathlib
import sys
import zipfile
from typing import Dict, Tuple

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "static" / "bots"

sys.path.insert(0, str(BASE))
import bots  # noqa: E402

# Fractions of the source height kept for the avatar crop: skips the blurb at
# the top and the rating badge at the bottom.
CROP_TOP = 0.17
CROP_BOTTOM = 0.80

AVATAR_PX = 256
CARD_PX = 512
EXTS = (".png", ".jpg", ".jpeg", ".webp")


def slug_for(filename: str) -> str:
    stem = pathlib.Path(filename).stem.strip().lower()
    return stem.replace("_", "-").replace(" ", "-")


def sources(path: pathlib.Path) -> Dict[str, bytes]:
    """Map slug -> image bytes, from a zip or a directory."""
    found: Dict[str, bytes] = {}
    if path.is_dir():
        for item in sorted(path.iterdir()):
            if item.suffix.lower() in EXTS:
                found[slug_for(item.name)] = item.read_bytes()
        return found

    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith("/") or pathlib.Path(name).suffix.lower() not in EXTS:
                continue
            found[slug_for(pathlib.Path(name).name)] = archive.read(name)
    return found


def face_crop(image, target: int):
    """Square crop of the middle band, where the character's face is."""
    from PIL import Image

    width, height = image.size
    top = int(height * CROP_TOP)
    bottom = int(height * CROP_BOTTOM)
    band = max(1, bottom - top)
    side = min(width, band)
    left = (width - side) // 2
    # keep the crop inside the band even when the image is very wide
    box = (left, top, left + side, top + side)
    return image.crop(box).resize((target, target), Image.LANCZOS)


def card(image, width: int):
    from PIL import Image

    scale = width / image.width
    size = (width, max(1, int(image.height * scale)))
    return image.resize(size, Image.LANCZOS)


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    source = pathlib.Path(argv[1])
    if not source.exists():
        print("no such file or folder:", source)
        return 1

    from PIL import Image

    found = sources(source)
    known = {bot["slug"] for bot in bots.BOTS}

    unknown = sorted(set(found) - known)
    missing = sorted(known - set(found))
    if unknown:
        print("ignoring files that match no bot:", ", ".join(unknown))
    if missing:
        print("no artwork supplied for:", ", ".join(missing))
        print("  (those bots keep their generated identicon)")

    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for slug in sorted(known & set(found)):
        image = Image.open(io.BytesIO(found[slug])).convert("RGB")
        avatar = face_crop(image, AVATAR_PX)
        avatar.save(OUT / f"{slug}.webp", "WEBP", quality=88, method=6)
        card(image, CARD_PX).save(OUT / f"{slug}-card.webp", "WEBP", quality=82, method=6)
        a = (OUT / f"{slug}.webp").stat().st_size
        c = (OUT / f"{slug}-card.webp").stat().st_size
        print(f"  {slug:<22} avatar {a // 1024:>3} KB   card {c // 1024:>3} KB")
        written += 1

    print(f"{written} bot image pair(s) written to {OUT.relative_to(BASE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
