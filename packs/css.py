"""CSS snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Everything is tagged `ui`;
the level does the sorting, from a two-property rule up to container queries
and scroll-driven animation.
"""
LANGUAGE = "css"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "ui", r'''
body {
  margin: 0;
  color: #eee;
}
''', r'''No console output - styles applied.
body: margin 0, text #eee'''),
    ("very-easy", "ui", r'''
h1 {
  font-size: 32px;
  font-weight: 700;
}
''', r'''h1: 32px, bold'''),
    ("very-easy", "ui", r'''
a {
  color: #62b6ff;
  text-decoration: none;
}
''', r'''links: blue, no underline'''),
    ("very-easy", "ui", r'''
a:hover {
  text-decoration: underline;
}
''', r'''links gain an underline on hover'''),
    ("very-easy", "ui", r'''
.hidden {
  display: none;
}
''', r'''.hidden elements are removed from the layout'''),
    ("very-easy", "ui", r'''
.center {
  text-align: center;
}
''', r'''.center: text centred'''),
    ("very-easy", "ui", r'''
img {
  max-width: 100%;
  height: auto;
}
''', r'''images never overflow their container'''),
    ("very-easy", "ui", r'''
.card {
  padding: 16px;
  border-radius: 12px;
}
''', r'''.card: 16px padding, rounded corners'''),
    ("very-easy", "ui", r'''
.row {
  display: flex;
  gap: 12px;
}
''', r'''.row: children in a row, 12px apart'''),
    ("very-easy", "ui", r'''
.stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
''', r'''.stack: children in a column, 8px apart'''),
    ("very-easy", "ui", r'''
* {
  box-sizing: border-box;
}
''', r'''padding and borders now count inside every width'''),
    ("very-easy", "ui", r'''
.muted {
  color: #8a93a6;
  font-size: 12px;
}
''', r'''.muted: small grey text'''),
    ("very-easy", "ui", r'''
button {
  cursor: pointer;
  border: 0;
}
''', r'''buttons: pointer cursor, no border'''),
    ("very-easy", "ui", r'''
.badge {
  border-radius: 999px;
  padding: 4px 12px;
}
''', r'''.badge: pill shaped'''),
    ("very-easy", "ui", r'''
ul {
  list-style: none;
  padding-left: 0;
}
''', r'''lists lose their bullets and indent'''),
    ("very-easy", "ui", r'''
.full {
  width: 100%;
}
''', r'''.full spans its container'''),
    ("very-easy", "ui", r'''
code {
  font-family: monospace;
  font-size: 14px;
}
''', r'''inline code renders monospaced'''),
    ("very-easy", "ui", r'''
.shadow {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
}
''', r'''.shadow: a soft drop shadow'''),
    ("very-easy", "ui", r'''
.border {
  border: 1px solid #262b38;
}
''', r'''.border: a 1px dark outline'''),
    ("very-easy", "ui", r'''
html {
  scroll-behavior: smooth;
}
''', r'''anchor jumps now animate instead of snapping'''),

    # --------------------------------------------------------------------- easy
    ("easy", "ui", r'''
.btn {
  padding: 10px 18px;
  border: 0;
  border-radius: 8px;
  background: #4f8cff;
  color: #fff;
  cursor: pointer;
}

.btn:hover {
  background: #3f78e0;
}
''', r'''No console output - styles applied.
.btn: 10px 18px, radius 8px, background #4f8cff'''),
    ("easy", "ui", r'''
.center {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 12px;
}
''', r'''No console output - styles applied.
.center: flex, centred, min-height 100vh'''),
    ("easy", "ui", r'''
.card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 12px;
  background: #16181d;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
}

.card:hover {
  transform: translateY(-2px);
}
''', r'''.card lifts 2px on hover'''),
    ("easy", "ui", r'''
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
''', r'''columns wrap automatically at 240px each'''),
    ("easy", "ui", r'''
.sidebar {
  position: sticky;
  top: 16px;
  align-self: start;
}
''', r'''.sidebar follows the scroll, pinned 16px from the top'''),
    ("easy", "ui", r'''
.truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
''', r'''long text becomes: a very long sentence…'''),
    ("easy", "ui", r'''
.clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
''', r'''paragraphs cut off after three lines'''),
    ("easy", "ui", r'''
input:focus,
select:focus {
  outline: none;
  border-color: #3d6ea8;
  box-shadow: 0 0 0 2px rgba(61, 110, 168, 0.35);
}
''', r'''focused fields gain a blue ring'''),
    ("easy", "ui", r'''
.bar {
  height: 10px;
  border-radius: 999px;
  background: #0b0d12;
  overflow: hidden;
}

.bar > i {
  display: block;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, #62b6ff, #6fe3a1);
  transition: width 0.12s linear;
}
''', r'''a progress bar that animates as its width changes'''),
    ("easy", "ui", r'''
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}
''', r'''.avatar: a 32px circle, image cropped to fill'''),
    ("easy", "ui", r'''
.table {
  width: 100%;
  border-collapse: collapse;
}

.table td {
  padding: 6px 0;
  border-top: 1px solid #262b38;
}
''', r'''rows separated by single hairlines'''),
    ("easy", "ui", r'''
.overlay {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(6, 8, 12, 0.72);
}
''', r'''a full-screen dimmed layer with its child centred'''),
    ("easy", "ui", r'''
:root {
  --bg: #0d0f14;
  --text: #e6e9f0;
  --accent: #6fe3a1;
}

body {
  background: var(--bg);
  color: var(--text);
}
''', r'''theme colours now come from custom properties'''),
    ("easy", "ui", r'''
@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
''', r'''below 640px the grid collapses to one column'''),
    ("easy", "ui", r'''
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  font-size: 13px;
  border: 1px solid #262b38;
  border-radius: 8px;
}
''', r'''.chip: a small bordered tag'''),
    ("easy", "ui", r'''
.scroll {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #2a3040 transparent;
}
''', r'''a thin dark scrollbar instead of the default slab'''),
    ("easy", "ui", r'''
.stack > * + * {
  margin-top: 12px;
}
''', r'''every child after the first gets 12px of space above it'''),
    ("easy", "ui", r'''
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
''', r'''hidden on screen, still read by screen readers'''),
    ("easy", "ui", r'''
.hero {
  background: linear-gradient(135deg, #101219, #1a2430);
  padding: 64px 24px;
  text-align: center;
}
''', r'''.hero: a gradient banner with generous padding'''),
    ("easy", "ui", r'''
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
''', r'''motion is effectively switched off for those who ask'''),

    ("easy", "ui", r"""
.divider {
  height: 1px;
  margin: 16px 0;
  background: linear-gradient(90deg, transparent, #262b38, transparent);
}
""", r"""a hairline rule that fades out at both ends"""),
    ("easy", "ui", r"""
.pill-group {
  display: inline-flex;
  border: 1px solid #262b38;
  border-radius: 999px;
  overflow: hidden;
}

.pill-group button + button {
  border-left: 1px solid #262b38;
}
""", r"""segmented buttons joined into one pill"""),

    # ------------------------------------------------------------------- medium
    ("medium", "ui", r'''
:root {
  --bg: #0e1013;
  --fg: #e6e9ef;
  --accent: #4f8cff;
  --radius: 12px;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
}

.badge[data-state="racing"] {
  animation: pulse 1.2s ease-in-out infinite;
  background: color-mix(in srgb, var(--accent) 25%, transparent);
}
''', r'''the racing badge breathes, tinted 25% accent'''),
    ("medium", "ui", r'''
.form:has(input:invalid) .submit {
  opacity: 0.5;
  pointer-events: none;
}

.list > li:not(:last-child)::after {
  content: "";
  display: block;
  height: 1px;
  margin: 8px 0;
  background: linear-gradient(90deg, transparent, #2a2f3a, transparent);
}
''', r'''submit disables itself while any field is invalid'''),
    ("medium", "ui", r'''
.layout {
  display: grid;
  grid-template-areas:
    "head head"
    "side main"
    "foot foot";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.layout > header { grid-area: head; }
.layout > aside { grid-area: side; }
.layout > main { grid-area: main; }
.layout > footer { grid-area: foot; }
''', r'''a named-area app shell: header, sidebar, content, footer'''),
    ("medium", "ui", r'''
.tooltip {
  position: relative;
}

.tooltip::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  translate: -50% 0;
  padding: 4px 8px;
  border-radius: 6px;
  background: #11141b;
  font-size: 11px;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.15s ease;
}

.tooltip:hover::after {
  opacity: 1;
}
''', r'''hovering shows the data-tip text above the element'''),
    ("medium", "ui", r'''
.switch {
  --size: 22px;
  position: relative;
  width: calc(var(--size) * 2);
  height: var(--size);
  border-radius: 999px;
  background: #262b38;
  transition: background 0.2s ease;
}

.switch::after {
  content: "";
  position: absolute;
  inset: 2px auto 2px 2px;
  width: calc(var(--size) - 4px);
  border-radius: 50%;
  background: #fff;
  transition: translate 0.2s ease;
}

.switch[aria-checked="true"] {
  background: #2d6446;
}

.switch[aria-checked="true"]::after {
  translate: var(--size) 0;
}
''', r'''a toggle whose knob slides when aria-checked flips'''),
    ("medium", "ui", r'''
.masonry {
  columns: 3 240px;
  column-gap: 16px;
}

.masonry > * {
  break-inside: avoid;
  margin-bottom: 16px;
}
''', r'''cards flow into three balanced columns'''),
    ("medium", "ui", r'''
.skeleton {
  background: linear-gradient(
    90deg,
    #14171f 25%,
    #1d222c 37%,
    #14171f 63%
  );
  background-size: 400% 100%;
  animation: shimmer 1.4s ease infinite;
  border-radius: 8px;
}

@keyframes shimmer {
  from { background-position: 100% 0; }
  to { background-position: 0 0; }
}
''', r'''a loading placeholder with a sweeping highlight'''),
    ("medium", "ui", r'''
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid #262b38;
}

.tabs button {
  padding: 8px 14px;
  background: none;
  border: 0;
  border-bottom: 2px solid transparent;
  color: #8a93a6;
}

.tabs button[aria-selected="true"] {
  color: #6fe3a1;
  border-bottom-color: #6fe3a1;
}
''', r'''the selected tab is underlined in green'''),
    ("medium", "ui", r'''
.code-area .ch {
  color: #454c5e;
}

.code-area .ch.done {
  color: inherit;
}

.code-area .ch.cur {
  background: rgba(98, 182, 255, 0.18);
  border-radius: 2px;
}

.code-area .ch.bad {
  background: rgba(255, 95, 109, 0.3);
  color: #ffd7da;
}
''', r'''untyped code is dim, typed lights up, mistakes go red'''),
    ("medium", "ui", r'''
.caret {
  position: absolute;
  width: 2px;
  background: #62b6ff;
  animation: blink 1s steps(1) infinite;
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}
''', r'''a text caret that blinks once a second'''),
    ("medium", "ui", r'''
.grid-fill {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: clamp(8px, 2vw, 24px);
}
''', r'''columns and gutters both scale with the viewport'''),
    ("medium", "ui", r'''
h1 {
  font-size: clamp(24px, 4vw, 48px);
  line-height: 1.1;
  letter-spacing: -0.02em;
  text-wrap: balance;
}
''', r'''the heading scales fluidly and wraps into even lines'''),
    ("medium", "ui", r'''
.nav a {
  position: relative;
}

.nav a::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 100%;
  height: 2px;
  background: currentColor;
  scale: 0 1;
  transform-origin: left;
  transition: scale 0.2s ease;
}

.nav a:hover::before {
  scale: 1 1;
}
''', r'''an underline that wipes in from the left on hover'''),
    ("medium", "ui", r'''
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --bg: #ffffff;
    --text: #12151c;
    --line: #e3e6ee;
  }
}

:root[data-theme="light"] {
  --bg: #ffffff;
  --text: #12151c;
}
''', r'''light mode follows the system, and a manual override wins'''),
    ("medium", "ui", r'''
.dialog {
  border: 0;
  border-radius: 16px;
  padding: 0;
  max-width: 480px;
}

.dialog::backdrop {
  background: rgba(6, 8, 12, 0.72);
  backdrop-filter: blur(3px);
}
''', r'''the native dialog gets a blurred dim backdrop'''),
    ("medium", "ui", r'''
.aspect {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
  border-radius: var(--radius, 12px);
}
''', r'''the box keeps a 16:9 shape at any width'''),
    ("medium", "ui", r'''
.sticky-head thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #101219;
  box-shadow: inset 0 -1px 0 #262b38;
}
''', r'''table headers stay visible while the body scrolls'''),
    ("medium", "ui", r'''
.scroll-x {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  overscroll-behavior-x: contain;
}

.scroll-x > * {
  flex: 0 0 80%;
  scroll-snap-align: center;
}
''', r'''a carousel that snaps each card to the centre'''),
    ("medium", "ui", r'''
.btn:focus-visible {
  outline: 2px solid #6fe3a1;
  outline-offset: 2px;
}

.btn:focus:not(:focus-visible) {
  outline: none;
}
''', r'''keyboard focus shows a ring; mouse clicks do not'''),
    ("medium", "ui", r'''
.toast {
  position: fixed;
  inset-inline: 16px;
  bottom: 16px;
  margin-inline: auto;
  max-width: 420px;
  padding: 12px 16px;
  border-radius: 10px;
  background: #1c3b2b;
  animation: rise 0.25s cubic-bezier(0.2, 1.3, 0.5, 1) both;
}

@keyframes rise {
  from {
    translate: 0 12px;
    opacity: 0;
  }
}
''', r'''a toast that slides up from the bottom edge'''),

    # --------------------------------------------------------------------- hard
    ("hard", "ui", r'''
@container card (min-width: 420px) {
  .card__body {
    display: grid;
    grid-template-columns: 96px 1fr;
    gap: 16px;
  }
}

.card {
  container: card / inline-size;
}
''', r'''the card relays out by its own width, not the viewport'''),
    ("hard", "ui", r'''
@layer reset, base, components, utilities;

@layer base {
  body {
    margin: 0;
    font: 16px/1.5 system-ui, sans-serif;
  }
}

@layer components {
  .btn {
    padding: 10px 18px;
    border-radius: 8px;
  }
}
''', r'''cascade layers keep utilities winning over components'''),
    ("hard", "ui", r'''
.card {
  view-transition-name: card;
}

@view-transition {
  navigate: auto;
}

::view-transition-old(card),
::view-transition-new(card) {
  animation-duration: 0.3s;
  animation-timing-function: cubic-bezier(0.2, 0.9, 0.3, 1);
}
''', r'''the card morphs between pages instead of blinking'''),
    ("hard", "ui", r'''
.progress {
  animation: grow linear both;
  animation-timeline: scroll(root block);
}

@keyframes grow {
  from {
    scale: 0 1;
  }
  to {
    scale: 1 1;
  }
}
''', r'''a reading-progress bar driven by scroll position, no JS'''),
    ("hard", "ui", r'''
.reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 10% cover 40%;
}

@keyframes fade-up {
  from {
    opacity: 0;
    translate: 0 24px;
  }
}
''', r'''each element fades up as it enters the viewport'''),
    ("hard", "ui", r'''
:root {
  --brand: oklch(72% 0.15 155);
}

.btn {
  background: var(--brand);
  color: oklch(from var(--brand) calc(l - 0.55) c h);
  border: 1px solid oklch(from var(--brand) calc(l - 0.12) c h);
}

.btn:hover {
  background: oklch(from var(--brand) calc(l + 0.05) c h);
}
''', r'''one brand colour derives its own text, border and hover'''),
    ("hard", "ui", r'''
@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.spinner {
  background: conic-gradient(from var(--angle), #6fe3a1, transparent 60%);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    --angle: 360deg;
  }
}
''', r'''a registered custom property lets the gradient animate'''),
    ("hard", "ui", r'''
.grid {
  display: grid;
  grid-template-columns:
    [full-start] minmax(16px, 1fr)
    [content-start] minmax(0, 1200px)
    [content-end] minmax(16px, 1fr)
    [full-end];
}

.grid > * {
  grid-column: content;
}

.grid > .bleed {
  grid-column: full;
}
''', r'''content sits in a 1200px column; .bleed spans edge to edge'''),
    ("hard", "ui", r'''
.tree li:has(> ul) > .label::before {
  content: "\25BE";
  display: inline-block;
  width: 1em;
  transition: rotate 0.15s ease;
}

.tree li:has(> ul[hidden]) > .label::before {
  rotate: -90deg;
}
''', r'''only branches with children get a caret, and it rotates'''),
    ("hard", "ui", r'''
.field {
  position: relative;
}

.field label {
  position: absolute;
  left: 12px;
  top: 12px;
  transition: translate 0.15s ease, font-size 0.15s ease;
  pointer-events: none;
}

.field:focus-within label,
.field input:not(:placeholder-shown) + label {
  translate: 0 -18px;
  font-size: 11px;
  color: #6fe3a1;
}
''', r'''the label floats above the field once it has focus or text'''),
    ("hard", "ui", r'''
.sheet {
  position: fixed;
  inset: auto 0 0 0;
  max-height: 85dvh;
  padding-bottom: env(safe-area-inset-bottom);
  border-radius: 16px 16px 0 0;
  translate: 0 100%;
  transition: translate 0.25s ease, overlay 0.25s allow-discrete;
}

.sheet:popover-open {
  translate: 0 0;
}
''', r'''a bottom sheet that slides up and respects the home bar'''),
    ("hard", "ui", r'''
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  grid-template-rows: masonry;
  gap: 16px;
}

@supports not (grid-template-rows: masonry) {
  .masonry {
    columns: 220px;
    column-gap: 16px;
  }
}
''', r'''native masonry where supported, columns everywhere else'''),
    ("hard", "ui", r'''
.parallax {
  perspective: 1px;
  transform-style: preserve-3d;
  overflow-x: hidden;
  overflow-y: auto;
  height: 100dvh;
}

.parallax__back {
  transform: translateZ(-1px) scale(2);
  transform-origin: center top;
}
''', r'''the background drifts at half speed as the page scrolls'''),
    ("hard", "ui", r'''
.table-wrap {
  overflow: auto;
  background:
    linear-gradient(90deg, #0d0f14 30%, rgba(13, 15, 20, 0)),
    linear-gradient(90deg, rgba(13, 15, 20, 0), #0d0f14 70%) 100% 0,
    radial-gradient(farthest-side at 0 50%, rgba(0, 0, 0, 0.4), transparent),
    radial-gradient(farthest-side at 100% 50%, rgba(0, 0, 0, 0.4), transparent) 100% 0;
  background-repeat: no-repeat;
  background-size: 40px 100%, 40px 100%, 14px 100%, 14px 100%;
  background-attachment: local, local, scroll, scroll;
}
''', r'''shadows appear at whichever edge still has content to scroll'''),
    ("hard", "ui", r'''
@media print {
  @page {
    margin: 18mm;
  }

  nav,
  .no-print {
    display: none !important;
  }

  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 10pt;
  }
}
''', r'''printing hides the chrome and spells out link targets'''),
    ("hard", "ui", r'''
.marquee {
  display: flex;
  gap: 32px;
  width: max-content;
  animation: slide 18s linear infinite;
}

.marquee:hover {
  animation-play-state: paused;
}

@keyframes slide {
  to {
    translate: -50% 0;
  }
}
''', r'''a seamless ticker that pauses when you hover it'''),
    ("hard", "ui", r'''
.card {
  transition:
    translate 0.18s cubic-bezier(0.2, 0.9, 0.3, 1),
    box-shadow 0.18s ease,
    border-color 0.18s ease;
  will-change: translate;
}

@media (hover: hover) and (pointer: fine) {
  .card:hover {
    translate: 0 -3px;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45);
  }
}
''', r'''the lift only applies to devices with a real hover'''),
    ("hard", "ui", r'''
.tag {
  anchor-name: --tag;
}

.popover {
  position: absolute;
  position-anchor: --tag;
  position-area: block-end span-inline-end;
  position-try-fallbacks: flip-block, flip-inline;
  margin-block-start: 6px;
}
''', r'''the popover pins to its tag and flips when space runs out'''),
    ("hard", "ui", r'''
.editor {
  display: grid;
  grid-template-columns: auto 1fr;
  font: 15px/1.7 var(--mono, monospace);
  tab-size: 4;
}

.editor__gutter {
  counter-reset: line;
  text-align: right;
  padding-inline-end: 12px;
  color: #454c5e;
  user-select: none;
}

.editor__gutter > span::before {
  counter-increment: line;
  content: counter(line);
}
''', r'''line numbers generated by counters, not markup'''),
    ("hard", "ui", r'''
.chart {
  --max: 120;
  display: grid;
  grid-auto-flow: column;
  align-items: end;
  gap: 4px;
  block-size: 160px;
}

.chart > div {
  block-size: calc(attr(data-value type(<number>), 0) / var(--max) * 100%);
  background: linear-gradient(180deg, #6fe3a1, #2d6446);
  border-radius: 3px 3px 0 0;
}
''', r'''bar heights read straight from each data-value attribute'''),
]
