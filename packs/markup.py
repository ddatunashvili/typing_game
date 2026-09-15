"""HTML snippet pack: 20 per level.

Entries are (level, topic, code, expected_output). Everything is tagged `ui`;
the level does the sorting, from a heading up to a full accessible component.
"""
LANGUAGE = "markup"

SNIPPETS = [
    # ---------------------------------------------------------------- very easy
    ("very-easy", "ui", r'''
<h1>Hello</h1>
<p>Type this line.</p>
''', r'''Rendered:
  Hello
  Type this line.'''),
    ("very-easy", "ui", r'''
<a href="/lobby">Create lobby</a>
''', r'''Rendered: Create lobby (links to /lobby)'''),
    ("very-easy", "ui", r'''
<button type="button">Ready</button>
''', r'''Rendered: [ Ready ]'''),
    ("very-easy", "ui", r'''
<img src="/static/og.png" alt="A keyboard lit from the side" />
''', r'''Rendered: the image, with alt text for screen readers'''),
    ("very-easy", "ui", r'''
<ul>
  <li>Python</li>
  <li>Rust</li>
</ul>
''', r'''Rendered:
  - Python
  - Rust'''),
    ("very-easy", "ui", r'''
<input id="name" type="text" placeholder="Your handle" />
''', r'''Rendered: a text box showing "Your handle"'''),
    ("very-easy", "ui", r'''
<br />
<hr />
''', r'''Rendered: a line break, then a horizontal rule'''),
    ("very-easy", "ui", r'''
<strong>98 wpm</strong> at <em>99%</em>
''', r'''Rendered: **98 wpm** at *99%*'''),
    ("very-easy", "ui", r'''
<div class="card">
  <p>Ready to race?</p>
</div>
''', r'''Rendered: a card containing one paragraph'''),
    ("very-easy", "ui", r'''
<span class="badge">racing</span>
''', r'''Rendered: racing'''),
    ("very-easy", "ui", r'''
<label for="lang">Language</label>
<select id="lang">
  <option>Python</option>
</select>
''', r'''Rendered: Language [ Python v ]'''),
    ("very-easy", "ui", r'''
<pre><code>def add(a, b):
    return a + b
</code></pre>
''', r'''Rendered: the code, monospaced, whitespace preserved'''),
    ("very-easy", "ui", r'''
<!-- the invite code goes here -->
<p id="code">-----</p>
''', r'''Rendered: -----   (the comment is not shown)'''),
    ("very-easy", "ui", r'''
<h2>Rankings</h2>
<h3>Bots</h3>
''', r'''Rendered: two headings, the second one smaller'''),
    ("very-easy", "ui", r'''
<input type="checkbox" id="timed" checked />
<label for="timed">Timed race</label>
''', r'''Rendered: a ticked checkbox labelled "Timed race"'''),
    ("very-easy", "ui", r'''
<textarea id="bio" rows="3"></textarea>
''', r'''Rendered: a three-line text area'''),
    ("very-easy", "ui", r'''
<p>Beat <b>Rubber Duck</b> &amp; win 24 points</p>
''', r'''Rendered: Beat **Rubber Duck** & win 24 points'''),
    ("very-easy", "ui", r'''
<video src="/demo.mp4" controls muted></video>
''', r'''Rendered: a muted video with playback controls'''),
    ("very-easy", "ui", r'''
<progress value="70" max="100"></progress>
''', r'''Rendered: a bar filled to 70%'''),
    ("very-easy", "ui", r'''
<time datetime="2026-09-16">16 Sep 2026</time>
''', r'''Rendered: 16 Sep 2026  (machine-readable date)'''),

    # --------------------------------------------------------------------- easy
    ("easy", "ui", r'''
<section class="hero">
  <h1 class="title">Race your friends</h1>
  <p class="subtitle">Type real code, not lorem ipsum.</p>
  <a class="btn" href="/lobby">Create lobby</a>
</section>
''', r'''Rendered:
  Race your friends
  Type real code, not lorem ipsum.
  [ Create lobby ]'''),
    ("easy", "ui", r'''
<nav class="topnav">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/lobby">Lobbies</a></li>
    <li><a href="/stats">Stats</a></li>
  </ul>
</nav>
''', r'''Rendered:
  Home | Lobbies | Stats'''),
    ("easy", "ui", r'''
<form class="signup" method="post" action="/api/signup">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required autocomplete="email" />

  <label for="name">Display name</label>
  <input id="name" name="name" maxlength="18" required />

  <button type="submit">Create account</button>
</form>
''', r'''Rendered: a two-field form that will not submit while empty'''),
    ("easy", "ui", r'''
<table class="results">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Player</th>
      <th scope="col">WPM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>ada</td>
      <td>118</td>
    </tr>
  </tbody>
</table>
''', r'''Rendered:
  #  Player  WPM
  1  ada     118'''),
    ("easy", "ui", r'''
<header>
  <a class="brand" href="/">CodeRace</a>
</header>
<main>
  <h1>Rankings</h1>
</main>
<footer>
  <p>&copy; 2026</p>
</footer>
''', r'''Rendered: a landmark structure screen readers can navigate'''),
    ("easy", "ui", r'''
<details>
  <summary>Difficulty</summary>
  <p>Four levels, from really easy to hard.</p>
</details>
''', r'''Rendered: a collapsed "Difficulty" toggle'''),
    ("easy", "ui", r'''
<fieldset>
  <legend>Levels</legend>
  <label><input type="checkbox" name="level" value="easy" checked /> Easy</label>
  <label><input type="checkbox" name="level" value="hard" /> Hard</label>
</fieldset>
''', r'''Rendered: a grouped pair of checkboxes titled "Levels"'''),
    ("easy", "ui", r'''
<dl>
  <dt>WPM</dt>
  <dd>Words per minute, five characters to a word.</dd>
  <dt>Elo</dt>
  <dd>A rating that moves with every race.</dd>
</dl>
''', r'''Rendered: two terms, each with its definition'''),
    ("easy", "ui", r'''
<blockquote cite="https://example.com/review">
  <p>I typed a whole quicksort without looking down.</p>
  <footer>&mdash; <cite>a happy racer</cite></footer>
</blockquote>
''', r'''Rendered: an indented quotation with its attribution'''),
    ("easy", "ui", r'''
<picture>
  <source srcset="/img/hero.avif" type="image/avif" />
  <source srcset="/img/hero.webp" type="image/webp" />
  <img src="/img/hero.png" alt="A keyboard lit from the side" loading="lazy" />
</picture>
''', r'''Rendered: the smallest format the browser understands'''),
    ("easy", "ui", r'''
<label for="search">Search snippets</label>
<input id="search" type="search" list="languages" />
<datalist id="languages">
  <option value="python"></option>
  <option value="rust"></option>
</datalist>
''', r'''Rendered: a search box that suggests python and rust'''),
    ("easy", "ui", r'''
<button type="button" aria-pressed="false" class="toggle">
  Timed mode
</button>
''', r'''Rendered: a toggle button whose state is announced'''),
    ("easy", "ui", r'''
<a href="/report.pdf" download="race-report.pdf">
  Download the report
</a>
''', r'''Rendered: a link that saves the file as race-report.pdf'''),
    ("easy", "ui", r'''
<ol start="3">
  <li>Regex Randy</li>
  <li>YAML Yolanda</li>
</ol>
''', r'''Rendered:
  3. Regex Randy
  4. YAML Yolanda'''),
    ("easy", "ui", r'''
<input
  id="wpm"
  name="wpm"
  type="number"
  min="0"
  max="400"
  step="1"
  inputmode="numeric"
/>
''', r'''Rendered: a numeric field that rejects anything above 400'''),
    ("easy", "ui", r'''
<iframe
  src="/embed/leaderboard"
  title="Leaderboard"
  loading="lazy"
  sandbox="allow-scripts"
></iframe>
''', r'''Rendered: a sandboxed embed, loaded when it scrolls near'''),
    ("easy", "ui", r'''
<p>
  Press <kbd>Enter</kbd> to skip the indent.
  Output: <samp>hello world</samp>
</p>
''', r'''Rendered: Press [Enter] to skip the indent. Output: hello world'''),
    ("easy", "ui", r'''
<figure>
  <img src="/img/chart.png" alt="WPM over the last 30 days" />
  <figcaption>Your speed over the last month.</figcaption>
</figure>
''', r'''Rendered: the chart with a caption tied to it'''),
    ("easy", "ui", r'''
<template id="racer-row">
  <div class="racer">
    <span class="nm"></span>
    <span class="wpm"></span>
  </div>
</template>
''', r'''Nothing renders: the template is cloned by script'''),
    ("easy", "ui", r'''
<noscript>
  <p>CodeRace needs JavaScript to run a race.</p>
</noscript>
''', r'''Rendered only when scripting is switched off'''),

    # ------------------------------------------------------------------- medium
    ("medium", "ui", r'''
<article class="post" itemscope itemtype="https://schema.org/BlogPosting">
  <header>
    <h2 itemprop="headline">Typing faster in code</h2>
    <time itemprop="datePublished" datetime="2026-09-15">15 Sep 2026</time>
  </header>
  <p itemprop="articleBody">Symbols are the slow part, not the words.</p>
</article>
''', r'''Rendered: the article, plus structured data for crawlers'''),
    ("medium", "ui", r'''
<dialog id="settings" aria-labelledby="settings-title">
  <h2 id="settings-title">Settings</h2>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="save">Save</button>
  </form>
</dialog>
''', r'''Rendered: a modal whose buttons close it with a return value'''),
    ("medium", "ui", r'''
<div class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab-ranks" aria-selected="true" aria-controls="panel-ranks">
    Rankings
  </button>
  <button role="tab" id="tab-bots" aria-selected="false" aria-controls="panel-bots">
    Bots
  </button>
</div>

<div role="tabpanel" id="panel-ranks" aria-labelledby="tab-ranks">…</div>
<div role="tabpanel" id="panel-bots" aria-labelledby="tab-bots" hidden>…</div>
''', r'''Rendered: two tabs, with the inactive panel hidden'''),
    ("medium", "ui", r'''
<img
  src="/img/hero-800.jpg"
  srcset="/img/hero-400.jpg 400w, /img/hero-800.jpg 800w, /img/hero-1600.jpg 1600w"
  sizes="(max-width: 640px) 100vw, 800px"
  alt="A dark editor with a race in progress"
/>
''', r'''Rendered: the browser picks a file to match the layout width'''),
    ("medium", "ui", r'''
<form action="/api/avatar" method="post" enctype="multipart/form-data">
  <label for="file">Profile image</label>
  <input
    id="file"
    name="file"
    type="file"
    accept="image/png,image/jpeg,image/webp"
    required
  />
  <button type="submit">Upload</button>
</form>
''', r'''Rendered: an upload form limited to three image types'''),
    ("medium", "ui", r'''
<div class="racer" role="group" aria-label="Rubber Duck, 18 words per minute">
  <span class="nm">Rubber Duck</span>
  <div
    class="bar"
    role="progressbar"
    aria-valuenow="42"
    aria-valuemin="0"
    aria-valuemax="100"
  >
    <i style="width: 42%"></i>
  </div>
</div>
''', r'''Rendered: a progress bar that announces 42%'''),
    ("medium", "ui", r'''
<p aria-live="polite" id="status">Waiting for the host…</p>
<p aria-live="assertive" id="alert" role="alert"></p>
''', r'''Status changes are announced; alerts interrupt'''),
    ("medium", "ui", r'''
<button popovertarget="bot-picker">Add a bot</button>

<div id="bot-picker" popover>
  <h3>Choose an opponent</h3>
  <button popovertarget="bot-picker" popovertargetaction="hide">Close</button>
</div>
''', r'''Rendered: a popover that opens and closes without script'''),
    ("medium", "ui", r'''
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CodeRace — type real code</title>
  <link rel="canonical" href="https://coderace.example.com/" />
  <meta name="description" content="A multiplayer typing game for real code." />
</head>
''', r'''No visible output: the page title and canonical URL are set'''),
    ("medium", "ui", r'''
<meta property="og:type" content="website" />
<meta property="og:title" content="CodeRace — type real code" />
<meta property="og:image" content="https://coderace.example.com/static/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
''', r'''Pasting the link now unfurls with a 1200x630 card'''),
    ("medium", "ui", r'''
<select id="language" name="language">
  <optgroup label="Curly braces">
    <option value="javascript">JavaScript</option>
    <option value="rust">Rust</option>
  </optgroup>
  <optgroup label="Indentation">
    <option value="python" selected>Python</option>
  </optgroup>
</select>
''', r'''Rendered: a grouped dropdown with Python preselected'''),
    ("medium", "ui", r'''
<table>
  <caption>Races this week</caption>
  <colgroup>
    <col span="1" style="width: 40px" />
    <col span="2" />
  </colgroup>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>ada</td>
      <td>118</td>
    </tr>
  </tbody>
</table>
''', r'''Rendered: a captioned table with a fixed first column'''),
    ("medium", "ui", r'''
<video controls poster="/img/poster.jpg" preload="metadata" playsinline>
  <source src="/demo.webm" type="video/webm" />
  <source src="/demo.mp4" type="video/mp4" />
  <track kind="captions" src="/demo.en.vtt" srclang="en" label="English" default />
  Your browser cannot play this video.
</video>
''', r'''Rendered: a captioned video with a fallback message'''),
    ("medium", "ui", r'''
<a class="skip" href="#main">Skip to content</a>

<nav>…</nav>

<main id="main" tabindex="-1">
  <h1>Rankings</h1>
</main>
''', r'''Tab once and the first stop is "Skip to content"'''),
    ("medium", "ui", r'''
<form>
  <label for="handle">Handle</label>
  <input
    id="handle"
    name="handle"
    pattern="[A-Za-z0-9_.]{2,18}"
    aria-describedby="handle-help"
    required
  />
  <small id="handle-help">2-18 letters, numbers, dots or underscores.</small>
</form>
''', r'''Rendered: the hint is read out with the field'''),
    ("medium", "ui", r'''
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "CodeRace",
    "applicationCategory": "GameApplication",
    "isAccessibleForFree": true
  }
</script>
''', r'''Nothing renders: search engines read the JSON-LD'''),
    ("medium", "ui", r'''
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin />
<link rel="preload" href="/static/app.js" as="script" />
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml" />
<link rel="manifest" href="/manifest.webmanifest" />
''', r'''No visible output: the browser warms up the connection early'''),
    ("medium", "ui", r'''
<ul class="racers">
  <li class="racer" data-id="1" data-wpm="118" data-bot="false">
    <span class="nm">ada</span>
  </li>
  <li class="racer" data-id="2" data-wpm="18" data-bot="true">
    <span class="nm">Rubber Duck</span>
  </li>
</ul>
''', r'''Rendered: two rows whose data- attributes script can read'''),
    ("medium", "ui", r'''
<output id="result" for="wpm acc" aria-live="polite">
  98 wpm at 99%
</output>
''', r'''Rendered: 98 wpm at 99%, announced when it changes'''),
    ("medium", "ui", r'''
<form method="get" action="/search">
  <input type="hidden" name="page" value="1" />
  <label for="q">Search</label>
  <input id="q" name="q" type="search" enterkeyhint="search" />
  <button type="submit">Go</button>
</form>
''', r'''Submitting goes to /search?page=1&q=…'''),

    # --------------------------------------------------------------------- hard
    ("hard", "ui", r'''
<div class="combo">
  <label id="lang-label" for="lang-input">Language</label>
  <input
    id="lang-input"
    role="combobox"
    aria-expanded="false"
    aria-controls="lang-list"
    aria-activedescendant=""
    aria-autocomplete="list"
    autocomplete="off"
  />
  <ul id="lang-list" role="listbox" aria-labelledby="lang-label" hidden>
    <li role="option" id="lang-python" aria-selected="false">Python</li>
    <li role="option" id="lang-rust" aria-selected="false">Rust</li>
  </ul>
</div>
''', r'''Rendered: an accessible autocomplete, states wired for script'''),
    ("hard", "ui", r'''
<table role="grid" aria-rowcount="214">
  <thead>
    <tr>
      <th scope="col" aria-sort="descending">
        <button>Rating</button>
      </th>
      <th scope="col" aria-sort="none"><button>Name</button></th>
    </tr>
  </thead>
  <tbody>
    <tr aria-rowindex="1">
      <td>1504</td>
      <td>ada</td>
    </tr>
  </tbody>
</table>
''', r'''Rendered: a sortable grid that reports 214 total rows'''),
    ("hard", "ui", r'''
<nav aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="/"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name" aria-current="page">Rankings</span>
      <meta itemprop="position" content="2" />
    </li>
  </ol>
</nav>
''', r'''Rendered: Home / Rankings, with breadcrumb structured data'''),
    ("hard", "ui", r'''
<form novalidate>
  <div class="field">
    <label for="email">Email</label>
    <input
      id="email"
      name="email"
      type="email"
      required
      aria-invalid="true"
      aria-errormessage="email-error"
    />
    <p id="email-error" role="alert">That address is missing an @.</p>
  </div>
</form>
''', r'''Rendered: the error is tied to the field and announced'''),
    ("hard", "ui", r'''
<dialog id="confirm" aria-labelledby="confirm-title" aria-describedby="confirm-body">
  <h2 id="confirm-title">Delete this profile?</h2>
  <p id="confirm-body">
    Your rating, races and avatar go with it. This cannot be undone.
  </p>
  <form method="dialog">
    <button value="cancel" autofocus>Keep it</button>
    <button value="delete" class="danger">Delete</button>
  </form>
</dialog>
''', r'''Rendered: a modal that opens with focus on the safe choice'''),
    ("hard", "ui", r'''
<figure class="chart">
  <svg viewBox="0 0 200 80" role="img" aria-labelledby="chart-title chart-desc">
    <title id="chart-title">WPM over seven days</title>
    <desc id="chart-desc">Rising from 84 to 104 words per minute.</desc>
    <polyline
      fill="none"
      stroke="#6fe3a1"
      stroke-width="2"
      points="0,60 33,52 66,55 99,40 132,36 165,28 198,20"
    />
  </svg>
  <figcaption>Steady gains, with one flat day.</figcaption>
</figure>
''', r'''Rendered: an inline chart that describes itself to a reader'''),
    ("hard", "ui", r'''
<div class="tree" role="tree" aria-label="Snippet library">
  <div role="treeitem" aria-expanded="true" aria-level="1" tabindex="0">
    Python
    <div role="group">
      <div role="treeitem" aria-level="2" tabindex="-1">Really easy</div>
      <div role="treeitem" aria-level="2" tabindex="-1">Hard</div>
    </div>
  </div>
</div>
''', r'''Rendered: a tree with one expanded branch and roving focus'''),
    ("hard", "ui", r'''
<form action="/api/register" method="post">
  <input type="hidden" name="csrf" value="{{ csrf_token }}" />
  <label for="pw">Password</label>
  <input
    id="pw"
    name="password"
    type="password"
    autocomplete="new-password"
    minlength="12"
    required
  />
  <button type="submit">Create account</button>
</form>
''', r'''Rendered: a form with a CSRF token and a 12-character minimum'''),
    ("hard", "ui", r'''
<input
  id="avatar"
  type="file"
  accept="image/*"
  capture="user"
  class="drop-input"
  aria-describedby="avatar-help"
/>
<div id="drop" role="button" tabindex="0" aria-controls="avatar">
  <b>Drop an image here</b>
  <span id="avatar-help">png, jpeg, gif or webp, up to 512 KB</span>
</div>
''', r'''Rendered: a drop zone reachable by keyboard as well as mouse'''),
    ("hard", "ui", r'''
<slot name="header"></slot>

<template shadowrootmode="open">
  <style>
    :host {
      display: block;
      border: 1px solid #262b38;
    }
  </style>
  <slot></slot>
</template>
''', r'''Rendered: declarative shadow DOM, styles scoped to the host'''),
    ("hard", "ui", r'''
<x-counter value="7"></x-counter>

<script type="module">
  class Counter extends HTMLElement {
    static observedAttributes = ["value"];

    connectedCallback() {
      this.attachShadow({ mode: "open" });
      this.render();
    }

    attributeChangedCallback() {
      if (this.shadowRoot) this.render();
    }

    render() {
      this.shadowRoot.innerHTML = `<b>${this.getAttribute("value") ?? 0}</b>`;
    }
  }

  customElements.define("x-counter", Counter);
</script>
''', r'''Rendered: 7  (and it re-renders when the attribute changes)'''),
    ("hard", "ui", r'''
<div
  class="carousel"
  role="region"
  aria-roledescription="carousel"
  aria-label="Featured bots"
>
  <div class="slides" aria-live="off">
    <div role="group" aria-roledescription="slide" aria-label="1 of 3">…</div>
  </div>
  <button aria-label="Previous bot">&#8592;</button>
  <button aria-label="Next bot">&#8594;</button>
</div>
''', r'''Rendered: a carousel that announces which slide is showing'''),
    ("hard", "ui", r'''
<table>
  <tbody>
    <tr>
      <th scope="rowgroup" rowspan="2">Python</th>
      <th scope="row">Really easy</th>
      <td>20</td>
    </tr>
    <tr>
      <th scope="row">Hard</th>
      <td>20</td>
    </tr>
  </tbody>
</table>
''', r'''Rendered: a spanned row header shared by two rows'''),
    ("hard", "ui", r'''
<ul class="pagination" role="navigation" aria-label="Pagination">
  <li>
    <a href="?page=1" rel="prev" aria-label="Previous page">&#8592;</a>
  </li>
  <li><a href="?page=2" aria-current="page">2</a></li>
  <li>
    <a href="?page=3" rel="next" aria-label="Next page">&#8594;</a>
  </li>
</ul>
''', r'''Rendered: pager with the current page marked for readers'''),
    ("hard", "ui", r'''
<form id="filters" method="get">
  <fieldset>
    <legend>Level</legend>
    <label><input type="radio" name="level" value="very-easy" /> Really easy</label>
    <label><input type="radio" name="level" value="hard" /> Hard</label>
  </fieldset>
</form>

<button type="submit" form="filters">Apply</button>
<button type="reset" form="filters">Clear</button>
''', r'''Rendered: buttons outside the form still drive it'''),
    ("hard", "ui", r'''
<head>
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="theme-color" content="#0d0f14" media="(prefers-color-scheme: dark)" />
</head>
''', r'''No visible output: inline scripts and third-party images are blocked'''),
    ("hard", "ui", r'''
<audio id="tick" preload="auto">
  <source src="/sfx/tick.ogg" type="audio/ogg" />
  <source src="/sfx/tick.mp3" type="audio/mpeg" />
</audio>

<button
  type="button"
  aria-pressed="false"
  onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed') === 'false')"
>
  Key sounds
</button>
''', r'''Rendered: a sound toggle whose pressed state is announced'''),
    ("hard", "ui", r'''
<div class="code-box">
  <pre
    id="codeArea"
    class="code-area"
    role="textbox"
    aria-readonly="true"
    aria-label="Snippet to type"
    tabindex="0"
  ></pre>
  <div id="ghosts" class="ghosts" aria-hidden="true"></div>
</div>
''', r'''Rendered: the snippet is readable by a screen reader;
opponent carets are hidden from it'''),
    ("hard", "ui", r'''
<form method="post" action="/api/race">
  <label for="lang">Language</label>
  <select id="lang" name="language" required>
    <option value="">Choose…</option>
    <option value="python">Python</option>
  </select>

  <label for="seconds">Race length</label>
  <input id="seconds" name="seconds" type="range" min="0" max="300" step="30"
         list="ticks" />
  <datalist id="ticks">
    <option value="0" label="One snippet"></option>
    <option value="60" label="1 min"></option>
    <option value="300" label="5 min"></option>
  </datalist>
</form>
''', r'''Rendered: a slider with labelled stops at 0, 60 and 300'''),
    ("hard", "ui", r'''
<svg width="0" height="0" aria-hidden="true" style="position: absolute">
  <symbol id="icon-star" viewBox="0 0 24 24">
    <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z" />
  </symbol>
</svg>

<button type="button">
  <svg class="icon" width="16" height="16" aria-hidden="true">
    <use href="#icon-star" />
  </svg>
  Favourite
</button>
''', r'''Rendered: [★ Favourite] - one sprite reused by every button'''),
]
