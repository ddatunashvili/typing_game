"""Generate the SEO and icon assets into static/.

Renders an HTML card with the real page styling through headless Chromium, then
packs the favicon with Pillow. Re-run after changing the branding:

    python tools/make_assets.py

Requires playwright (`pip install playwright && playwright install chromium`)
and Pillow. Both are dev-only; the server never needs them.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
STATIC = BASE / "static"

BG = "#0d0f14"
PANEL = "#14171f"
LINE = "#262b38"
TEXT = "#e6e9f0"
MUTED = "#8a93a6"
DIM = "#454c5e"
ACCENT = "#6fe3a1"
ACCENT2 = "#62b6ff"
MONO = "Consolas, 'Cascadia Code', 'DejaVu Sans Mono', monospace"
SANS = "'Segoe UI', Inter, system-ui, sans-serif"

# The social card: a mock race so the embed shows what the site actually is.
OG_HTML = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ box-sizing: border-box; margin: 0; }}
  body {{
    width: 1200px; height: 630px; background: {BG}; color: {TEXT};
    font-family: {SANS}; padding: 64px 68px; position: relative; overflow: hidden;
  }}
  .glow {{
    position: absolute; width: 760px; height: 760px; right: -240px; top: -300px;
    background: radial-gradient(circle, rgba(111,227,161,.16), transparent 62%);
  }}
  .glow2 {{
    position: absolute; width: 620px; height: 620px; left: -220px; bottom: -280px;
    background: radial-gradient(circle, rgba(98,182,255,.13), transparent 62%);
  }}
  .brand {{ display: flex; align-items: center; gap: 14px; font-size: 27px; font-weight: 700;
            letter-spacing: .6px; position: relative; }}
  .dot {{ width: 15px; height: 15px; border-radius: 50%; background: {ACCENT};
          box-shadow: 0 0 22px {ACCENT}; }}
  h1 {{ font-size: 68px; line-height: 1.04; margin: 34px 0 16px; letter-spacing: -1.4px;
        position: relative; }}
  h1 em {{ font-style: normal; color: {ACCENT}; }}
  p.sub {{ font-size: 26px; color: {MUTED}; position: relative; }}
  .code {{
    position: relative; margin-top: 38px; background: #101219; border: 1px solid {LINE};
    border-radius: 16px; padding: 24px 28px; font-family: {MONO}; font-size: 22px;
    line-height: 1.6; width: 660px;
  }}
  .code .kw {{ color: #c79bff; }}
  .code .fn {{ color: {ACCENT2}; }}
  .code .str {{ color: {ACCENT}; }}
  .code .todo {{ color: {DIM}; }}
  .caret {{ display: inline-block; width: 2px; height: 22px; background: {ACCENT2};
            vertical-align: -3px; margin: 0 1px; }}
  .side {{ position: absolute; right: 68px; bottom: 132px; width: 372px; }}
  .racer {{ display: flex; align-items: center; gap: 12px; background: {PANEL};
            border: 1px solid {LINE}; border-radius: 12px; padding: 12px 15px;
            margin-bottom: 11px; font-size: 18px; }}
  .racer.me {{ border-color: #2d6446; }}
  .av {{ width: 30px; height: 30px; border-radius: 50%; background: #1a1e28;
         border: 1px solid {LINE}; display: flex; align-items: center;
         justify-content: center; font-size: 14px; font-weight: 700; color: {MUTED}; }}
  .nm {{ flex: 1; font-weight: 600; }}
  .wpm {{ font-family: {MONO}; color: {ACCENT}; font-size: 16px; }}
  .bar {{ height: 7px; background: #0b0d12; border: 1px solid {LINE};
          border-radius: 999px; overflow: hidden; margin-top: 9px; }}
  .bar i {{ display: block; height: 100%; background: linear-gradient(90deg, {ACCENT2}, {ACCENT}); }}
  .foot {{ position: absolute; left: 68px; bottom: 56px; display: flex; gap: 10px; }}
  .chip {{ font-size: 17px; color: {MUTED}; border: 1px solid {LINE}; background: #1a1e28;
           border-radius: 999px; padding: 7px 15px; }}
  .chip.on {{ color: {ACCENT}; border-color: #2d6446; background: #1c3b2b; }}
</style></head><body>
  <div class="glow"></div><div class="glow2"></div>
  <div class="brand"><span class="dot"></span>CodeRace</div>
  <h1>Type real <em>code</em>.<br/>Race your friends.</h1>
  <p class="sub">15 languages &middot; 4 levels &middot; live multiplayer</p>

  <div class="code">
    <span class="kw">def</span> <span class="fn">binary_search</span>(items, target):<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;low, high = <span class="str">0</span>, len(items) - <span class="str">1</span><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">while</span> low &lt;= high:<span class="caret"></span><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="todo">mid = (low + high) // 2</span>
  </div>

  <div class="side">
    <div class="racer me">
      <span class="av">D</span><span class="nm">you</span><span class="wpm">98 wpm</span>
      <div class="bar" style="position:absolute"></div>
    </div>
    <div class="racer"><span class="av">R</span><span class="nm">Regex Randy</span><span class="wpm">85 wpm</span></div>
    <div class="racer"><span class="av">S</span><span class="nm">Segfault Sally</span><span class="wpm">122 wpm</span></div>
  </div>

  <div class="foot">
    <span class="chip on">Really easy</span>
    <span class="chip">Algorithms</span>
    <span class="chip">1 min</span>
    <span class="chip on">Multiplayer</span>
  </div>
</body></html>"""

# Square mark used for the icons.
ICON_HTML = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ box-sizing: border-box; margin: 0; }}
  body {{ width: 512px; height: 512px; background: {BG}; display: flex;
          align-items: center; justify-content: center; }}
  .mark {{ width: 512px; height: 512px; background:
            radial-gradient(circle at 30% 22%, #17202b, {BG} 70%);
          display: flex; align-items: center; justify-content: center;
          position: relative; }}
  .glyph {{ font-family: {MONO}; font-size: 250px; font-weight: 700; color: {ACCENT};
            text-shadow: 0 0 60px rgba(111,227,161,.45); letter-spacing: -12px; }}
  .caret {{ width: 26px; height: 190px; background: {ACCENT2}; margin-left: 16px;
            box-shadow: 0 0 40px rgba(98,182,255,.5); border-radius: 3px; }}
</style></head><body>
  <div class="mark"><span class="glyph">&gt;_</span><span class="caret"></span></div>
</body></html>"""

FAVICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="{BG}"/>
  <text x="7" y="44" font-family="monospace" font-size="34" font-weight="700"
        fill="{ACCENT}">&gt;_</text>
  <rect x="47" y="17" width="5" height="30" rx="1.5" fill="{ACCENT2}"/>
</svg>
"""


def render(html: str, path: pathlib.Path, width: int, height: int) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=1)
        page.set_content(html, wait_until="load")
        page.wait_for_timeout(250)
        page.screenshot(path=str(path), clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()
    print("wrote", path.relative_to(BASE), f"({width}x{height})")


def main() -> int:
    STATIC.mkdir(parents=True, exist_ok=True)

    (STATIC / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    print("wrote static/favicon.svg")

    render(OG_HTML, STATIC / "og.png", 1200, 630)
    render(ICON_HTML, STATIC / "icon-512.png", 512, 512)

    from PIL import Image

    master = Image.open(STATIC / "icon-512.png").convert("RGBA")
    for size in (192, 180):
        name = "apple-touch-icon.png" if size == 180 else f"icon-{size}.png"
        master.resize((size, size), Image.LANCZOS).save(STATIC / name)
        print(f"wrote static/{name} ({size}x{size})")

    master.resize((64, 64), Image.LANCZOS).save(
        STATIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("wrote static/favicon.ico")
    return 0


if __name__ == "__main__":
    sys.exit(main())
