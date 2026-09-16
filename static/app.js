/* CodeRace client: typing engine, filters, profile and lobby websocket. */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);

  const el = {
    home: $("screen-home"),
    room: $("screen-room"),
    name: $("nameInput"),
    nameField: $("nameField"),
    brand: $("brand"),
    profileBtn: $("profileBtn"),
    profileAvatar: $("profileAvatar"),
    profileName: $("profileName"),
    profileRate: $("profileRate"),
    leave: $("leaveBtn"),
    langGrid: $("langGrid"),
    levelChips: $("levelChips"),
    topicChips: $("topicChips"),
    levelHint: $("levelHint"),
    topicHint: $("topicHint"),
    topicAll: $("topicAll"),
    topicNone: $("topicNone"),
    filterWarn: $("filterWarn"),
    durationChips: $("durationChips"),
    durationHint: $("durationHint"),
    roomDurationChips: $("roomDurationChips"),
    hudSnips: $("hudSnips"),
    hudSnipsBox: $("hudSnipsBox"),
    solo: $("soloBtn"),
    create: $("createBtn"),
    joinForm: $("joinForm"),
    joinCode: $("joinCode"),
    homeErr: $("homeErr"),
    lbPanel: $("lbPanel"),
    leaderboard: $("leaderboard"),
    chatLog: $("chatLog"),
    chatForm: $("chatForm"),
    chatInput: $("chatInput"),
    roomCode: $("roomCode"),
    codeText: $("codeText"),
    copyLink: $("copyLink"),
    langSelect: $("langSelect"),
    filterBtn: $("filterBtn"),
    roomFilters: $("roomFilters"),
    roomLevelChips: $("roomLevelChips"),
    roomTopicChips: $("roomTopicChips"),
    roomFilterNote: $("roomFilterNote"),
    snipMeta: $("snipMeta"),
    stateBadge: $("stateBadge"),
    ready: $("readyBtn"),
    start: $("startBtn"),
    again: $("againBtn"),
    newSnip: $("newSnipBtn"),
    racers: $("racers"),
    countdown: $("countdown"),
    countNum: $("countNum"),
    hudWpm: $("hudWpm"),
    hudAcc: $("hudAcc"),
    hudTime: $("hudTime"),
    hudLeft: $("hudLeft"),
    codeBox: $("codeBox"),
    codeArea: $("codeArea"),
    trap: $("trap"),
    hint: $("hint"),
    results: $("results"),
    modal: $("profileModal"),
    pfTitle: $("pfTitle"),
    pfName: $("pfName"),
    pfAvatar: $("pfAvatar"),
    pfPreview: $("pfPreview"),
    pfRemove: $("pfRemove"),
    pfErr: $("pfErr"),
    pfCancel: $("pfCancel"),
    pfSave: $("pfSave"),
    pfNameNote: $("pfNameNote"),
    pfIdeas: $("pfIdeas"),
    pfDrop: $("pfDrop"),
    pfCrop: $("pfCrop"),
    pfStage: $("pfStage"),
    pfCanvas: $("pfCanvas"),
    pfZoom: $("pfZoom"),
    cvDrop: $("cvDrop"),
    cvFile: $("cvFile"),
    cvCrop: $("cvCrop"),
    cvStage: $("cvStage"),
    cvCanvas: $("cvCanvas"),
    cvZoom: $("cvZoom"),
    cvRemove: $("cvRemove"),
    pfRecrop: $("pfRecrop"),
    ranksBtn: $("ranksBtn"),
    ranksBack: $("ranksBack"),
    ranks: $("screen-ranks"),
    ranksTable: $("ranksTable"),
    ranksLadder: $("ranksLadder"),
    ranksCount: $("ranksCount"),
    ranksEmpty: $("ranksEmpty"),
    botPanel: $("botPanel"),
    botList: $("botList"),
    addBotBtn: $("addBotBtn"),
    botModal: $("botModal"),
    botPickList: $("botPickList"),
    botCancel: $("botCancel"),
    runPanel: $("runPanel"),
    runOut: $("runOut"),
    runStars: $("runStars"),
    runTitle: $("runTitle"),
    ghosts: $("ghosts"),
    gutter: $("gutter"),
    lineGlow: $("lineGlow"),
    resign: $("resignBtn"),
    suggest: $("suggest"),
    winModal: $("winModal"),
    winStars: $("winStars"),
    winTitle: $("winTitle"),
    winSub: $("winSub"),
    winWpm: $("winWpm"),
    winAcc: $("winAcc"),
    winPlace: $("winPlace"),
    winDelta: $("winDelta"),
    winDeltaBox: $("winDeltaBox"),
    winNote: $("winNote"),
    winClose: $("winClose"),
    winAgain: $("winAgain"),
  };

  /* Colours for opponent carets - each racer keeps the same one. */
  const GHOST_COLORS = ["#62b6ff", "#ffc46b", "#ff8fa3", "#c79bff", "#7de0d8", "#9ae66e"];

  function ghostColor(id) {
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) % 997;
    return GHOST_COLORS[h % GHOST_COLORS.length];
  }

  const LANG_FALLBACK = { markup: "markup", html: "markup" };

  function readList(key) {
    try {
      const raw = JSON.parse(localStorage.getItem(key) || "[]");
      return Array.isArray(raw) ? raw.filter((v) => typeof v === "string") : [];
    } catch (err) {
      return [];
    }
  }

  /* ---------- countries ----------
     Only the ISO 3166-1 alpha-2 codes are held here. The browser turns a code
     into a name in the reader's own language through Intl.DisplayNames, and the
     flag is the two letters shifted into the regional-indicator block, so
     neither a name table nor a sprite sheet has to be shipped or kept current. */
  const COUNTRY_CODES = (
    "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI " +
    "BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN " +
    "CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK " +
    "FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM " +
    "HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN " +
    "KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK " +
    "ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP " +
    "NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW " +
    "SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF " +
    "TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI " +
    "VN VU WF WS YE YT ZA ZM ZW"
  ).split(" ");

  let COUNTRY_NAMES = null;
  try {
    COUNTRY_NAMES = new Intl.DisplayNames(undefined, { type: "region" });
  } catch (err) {
    COUNTRY_NAMES = null;  // very old browser: the code itself has to do
  }

  function countryName(code) {
    if (!code) return "";
    if (!COUNTRY_NAMES) return code;
    try {
      return COUNTRY_NAMES.of(code) || code;
    } catch (err) {
      return code;
    }
  }

  /** "GB" -> the flag emoji, by shifting each letter into regional indicators. */
  function countryFlag(code) {
    if (!code || code.length !== 2) return "";
    const base = 0x1f1e6 - 65;
    return String.fromCodePoint(
      base + code.charCodeAt(0),
      base + code.charCodeAt(1)
    );
  }

  const GENDER_LABELS = { male: "Male", female: "Female", other: "Other" };

  /**
   * A flag image for a country code.
   *
   * The emoji flag is one string and no network, but Windows has never shipped
   * a font that renders a regional-indicator pair, so there it comes out as two
   * letters in a box. These are real images, with the emoji put back if the
   * request fails - so an offline or blocked browser still shows something.
   */
  function flagNode(code, size) {
    const wrap = document.createElement("span");
    wrap.className = "flag";
    if (!code) return wrap;
    const low = code.toLowerCase();
    const h = size || 18;
    const w = Math.round((h * 4) / 3);
    const img = document.createElement("img");
    img.width = w;
    img.height = h;
    img.alt = "";
    img.loading = "lazy";
    img.decoding = "async";
    img.src = "https://flagcdn.com/" + w + "x" + h + "/" + low + ".png";
    img.srcset = "https://flagcdn.com/" + w * 2 + "x" + h * 2 + "/" + low + ".png 2x";
    img.onerror = () => {
      wrap.textContent = countryFlag(code) || code;
      wrap.classList.add("flag-text");
    };
    wrap.appendChild(img);
    return wrap;
  }

  /* ---------- searchable dropdown ----------
     Built rather than borrowed: it has to hold 250 rows with a flag on each,
     filter as you type, and keep working with the keyboard. The value lives in
     a hidden input, so everything that reads or writes the field carries on
     using it as if it were still a <select>. */
  function makeCombo(rootId, opts) {
    const root = el2(rootId);
    if (!root) return null;
    const hidden = root.querySelector('input[type="hidden"]');
    const toggle = root.querySelector(".combo-toggle");
    const face = root.querySelector(".combo-face");
    const pop = root.querySelector(".combo-pop");
    const search = root.querySelector(".combo-search");
    const list = root.querySelector(".combo-list");
    const empty = root.querySelector(".combo-empty");
    const rows = opts.items || [];
    const blank = opts.blank || "Rather not say";
    let shown = rows;
    let active = -1;

    function paintFace() {
      const row = rows.find((r) => r.value === hidden.value);
      face.innerHTML = "";
      if (row && row.value) {
        face.appendChild(flagNode(row.value, 14));
        const label = document.createElement("span");
        label.textContent = row.label;
        face.appendChild(label);
      } else {
        const label = document.createElement("span");
        label.className = "muted";
        label.textContent = blank;
        face.appendChild(label);
      }
    }

    function render(filter) {
      const q = (filter || "").trim().toLowerCase();
      shown = q
        ? rows.filter(
            (r) =>
              r.label.toLowerCase().includes(q) ||
              (r.value && r.value.toLowerCase() === q)
          )
        : rows;
      list.innerHTML = "";
      // Cap what is in the DOM at once: 250 rows each with an image is a lot
      // to lay out for a list nobody scrolls to the bottom of.
      for (const row of shown.slice(0, 80)) {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "combo-item" + (row.value === hidden.value ? " on" : "");
        item.dataset.value = row.value;
        item.setAttribute("role", "option");
        if (row.value) item.appendChild(flagNode(row.value, 14));
        const label = document.createElement("span");
        label.textContent = row.label;
        if (!row.value) label.className = "muted";
        item.appendChild(label);
        item.onclick = () => {
          hidden.value = row.value;
          paintFace();
          close();
        };
        list.appendChild(item);
      }
      empty.classList.toggle("hidden", shown.length > 0);
      active = -1;
    }

    function move(step) {
      const items = [...list.children];
      if (!items.length) return;
      if (active >= 0 && items[active]) items[active].classList.remove("cursor");
      active = (active + step + items.length) % items.length;
      items[active].classList.add("cursor");
      items[active].scrollIntoView({ block: "nearest" });
    }

    function open() {
      pop.classList.remove("hidden");
      toggle.setAttribute("aria-expanded", "true");
      search.value = "";
      render("");
      search.focus();
    }

    function close() {
      pop.classList.add("hidden");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.onclick = () => (pop.classList.contains("hidden") ? open() : close());
    search.oninput = () => render(search.value);
    search.onkeydown = (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        e.preventDefault();
        const pick = list.children[active >= 0 ? active : 0];
        if (pick) pick.click();
      } else if (e.key === "Escape") {
        e.preventDefault();
        close();
        toggle.focus();
      }
    };
    // Clicking anywhere else closes it, but a click inside must not.
    document.addEventListener("click", (e) => {
      if (!root.contains(e.target)) close();
    });

    paintFace();
    return {
      get: () => hidden.value,
      set: (value) => {
        hidden.value = value || "";
        paintFace();
      },
    };
  }

  let COUNTRY_COMBO = null;

  /* ---------- themes and display preferences ----------
     The browser is the source of truth: the choice is written to localStorage
     first (and applied to <html> straight away) so it survives a reload with
     no network, then mirrored onto the account so it follows the player to
     another machine. index.html applies the stored theme before first paint. */
  const THEMES = [
    { id: "dark", label: "Midnight", swatch: ["#0d0f14", "#6fe3a1", "#62b6ff"] },
    { id: "dracula", label: "Dracula", swatch: ["#1a1b26", "#50fa7b", "#ff79c6"] },
    { id: "nord", label: "Nord", swatch: ["#2e3440", "#a3be8c", "#88c0d0"] },
    { id: "light", label: "Daylight", swatch: ["#f5f6f8", "#10a35f", "#2a72d4"] },
    { id: "paper", label: "Paper", swatch: ["#f4efe4", "#1f7a4d", "#2f6bb0"] },
  ];
  const THEME_IDS = THEMES.map((t) => t.id);

  const DISPLAY = {
    theme: "dark",
    lineNumbers: true,
    indentGuides: true,
    caretScroll: true,
  };

  function loadDisplay() {
    try {
      const theme = localStorage.getItem("cr_theme");
      if (theme && THEME_IDS.indexOf(theme) >= 0) DISPLAY.theme = theme;
      const raw = JSON.parse(localStorage.getItem("cr_display") || "{}");
      for (const key of ["lineNumbers", "indentGuides", "caretScroll"]) {
        if (typeof raw[key] === "boolean") DISPLAY[key] = raw[key];
      }
    } catch (err) {
      /* a blocked or corrupt store just means the defaults */
    }
    applyDisplay();
  }

  function applyDisplay() {
    document.documentElement.setAttribute("data-theme", DISPLAY.theme);
    document.documentElement.classList.toggle("no-lines", !DISPLAY.lineNumbers);
    document.documentElement.classList.toggle("no-guides", !DISPLAY.indentGuides);
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      const bg = getComputedStyle(document.documentElement)
        .getPropertyValue("--bg")
        .trim();
      if (bg) meta.setAttribute("content", bg);
    }
    const scheme = document.querySelector('meta[name="color-scheme"]');
    if (scheme) {
      const light = DISPLAY.theme === "light" || DISPLAY.theme === "paper";
      scheme.setAttribute("content", light ? "light" : "dark");
    }
    // the gutter changes the code width, so anything measured from it is stale
    if (T.chars && T.chars.length) requestAnimationFrame(remeasure);
  }

  /** Persist locally at once, then mirror onto the account if there is one. */
  function saveDisplay() {
    try {
      localStorage.setItem("cr_theme", DISPLAY.theme);
      localStorage.setItem(
        "cr_display",
        JSON.stringify({
          lineNumbers: DISPLAY.lineNumbers,
          indentGuides: DISPLAY.indentGuides,
          caretScroll: DISPLAY.caretScroll,
        })
      );
    } catch (err) {
      /* private mode: the account copy below is the fallback */
    }
    applyDisplay();
    if (!S.me) return;
    fetch("/api/settings", {
      method: "POST",
      credentials: "same-origin",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        theme: DISPLAY.theme,
        lineNumbers: DISPLAY.lineNumbers,
        indentGuides: DISPLAY.indentGuides,
        caretScroll: DISPLAY.caretScroll,
      }),
    }).catch(() => {});
  }

  /** Settings that arrived with the account, for a browser that has none yet. */
  function adoptDisplay(settings) {
    if (!settings) return;
    let stored = null;
    try {
      stored = localStorage.getItem("cr_theme");
    } catch (err) {
      stored = null;
    }
    if (stored) return;  // this device has already chosen
    if (settings.theme && THEME_IDS.indexOf(settings.theme) >= 0) {
      DISPLAY.theme = settings.theme;
    }
    for (const key of ["lineNumbers", "indentGuides", "caretScroll"]) {
      if (typeof settings[key] === "boolean") DISPLAY[key] = settings[key];
    }
    applyDisplay();
  }

  const S = {
    meta: null,
    lang: localStorage.getItem("cr_lang") || "python",
    levels: readList("cr_levels"),
    topics: readList("cr_topics"),
    name: localStorage.getItem("cr_name") || "",
    pid: localStorage.getItem("cr_pid") || "",
    me: null,
    accounts: false,
    ws: null,
    room: null,
    solo: false,
    spectating: false,  // watching a lobby rather than racing in it
    lobbyKey: "",       // key for the private lobby being joined
    lobby: null,
    snipLevel: "",
    snipTopic: "",
    soloLevel: "",  // level the solo session is pinned to
    lastCode: "",   // last snippet played, so a new deck never repeats it
    bots: [],
    ranksTimer: 0,
    output: "",     // expected output of the current snippet
    runTimer: 0,
    duration: null, // null until /api/meta supplies the default
  };

  const DURATIONS = [
    { v: 0, label: "One snippet" },
    { v: 30, label: "30s" },
    { v: 60, label: "1 min" },
    { v: 120, label: "2 min" },
    { v: 300, label: "5 min" },
  ];

  /* Timed run: a playlist typed end to end until the clock stops. */
  const R = {
    timed: false,
    playlist: [],
    idx: 0,
    chars: 0,      // correct characters across every snippet so far
    typed: 0,      // correct keystrokes, for cumulative accuracy
    errors: 0,
    snips: 0,      // snippets completed
    endsAt: 0,     // performance.now() deadline
    startedAt: 0,
    over: false,
  };

  /* ---------- replay recorder ----------
     Every accepted key, miss and backspace, as [ms, pos, idx, flag] relative
     to the moment the race armed. A few KB per race. Sent with the result, so
     the run can be watched back from the feed. Nothing here touches the
     screen or the network mid-race: it is an array push. */
  const REC = { events: [], t0: 0, on: false };

  function recStart() {
    REC.events = [];
    REC.t0 = performance.now();
    REC.on = true;
  }

  function recEvent(flag) {
    if (!REC.on) return;
    if (REC.events.length >= 20000) return;  // the server caps it here too
    REC.events.push([Math.round(performance.now() - REC.t0), T.pos, R.idx, flag || 0]);
  }

  function recTake() {
    REC.on = false;
    return REC.events.length ? REC.events : null;
  }

  function recSnippets() {
    return R.playlist && R.playlist.length ? R.playlist.map((x) => x.code) : [T.code];
  }

  function initRun(timed, playlist) {
    R.timed = !!timed;
    R.playlist = playlist || [];
    R.idx = 0;
    R.chars = 0;
    R.typed = 0;
    R.errors = 0;
    R.snips = 0;
    R.endsAt = 0;
    R.startedAt = 0;
    R.over = false;
    el.hudSnipsBox.classList.toggle("hidden", !timed);
  }

  function runSeconds() {
    return R.startedAt ? (performance.now() - R.startedAt) / 1000 : 0;
  }

  function remaining() {
    if (!R.timed || !R.endsAt) return 0;
    return Math.max(0, (R.endsAt - performance.now()) / 1000);
  }

  /** Characters completed, including the snippet currently being typed. */
  function liveChars() {
    return R.chars + T.pos;
  }

  function runWpm() {
    const secs = runSeconds();
    if (secs < 0.5) return 0;
    return (liveChars() / 5) / (secs / 60);
  }

  function runAccuracy() {
    const good = R.typed + T.typed;
    const total = good + R.errors + T.errors;
    return total ? (good / total) * 100 : 100;
  }

  // ---------- typing engine ----------
  const T = {
    code: "",
    chars: [],
    lineOf: [],     // character index -> 0-based line number
    lineTops: [],   // line number -> offsetTop, measured once per snippet
    lineNodes: [],  // line number -> gutter <i>
    curSpan: null,  // the span currently wearing .cur
    curLine: -1,
    pos: 0,
    typed: 0,
    errors: 0,
    bad: false,
    startedAt: 0,
    running: false,
    raf: 0,
    lastSend: 0,
  };

  function grammarFor(lang) {
    const key = LANG_FALLBACK[lang] || lang;
    return Prism.languages[key] || Prism.languages.clike || Prism.languages.markup;
  }

  function wrapChars(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    const out = [];
    for (const node of nodes) {
      const frag = document.createDocumentFragment();
      const text = node.nodeValue;
      for (let i = 0; i < text.length; i++) {
        const span = document.createElement("span");
        span.className = text[i] === "\n" ? "ch nl" : "ch";
        span.textContent = text[i];
        frag.appendChild(span);
        out.push(span);
      }
      node.parentNode.replaceChild(frag, node);
    }
    return out;
  }

  /* Tab stop used for the indent guides. Matches `tab-size: 4` in the CSS. */
  const INDENT = 4;

  /**
   * Mark the leading whitespace so the CSS can draw a rule every four columns,
   * and remember which line each character is on. Doing both in one walk keeps
   * it to a single pass over the snippet.
   */
  function indexLines(code) {
    const lineOf = new Array(code.length);
    let line = 0;
    let col = 0;
    let leading = true;
    for (let i = 0; i < code.length; i++) {
      const ch = code[i];
      lineOf[i] = line;
      if (ch === "\n") {
        line++;
        col = 0;
        leading = true;
        continue;
      }
      if (leading && (ch === " " || ch === "\t")) {
        if (col % INDENT === 0) T.chars[i].classList.add("ig");
        col += ch === "\t" ? INDENT : 1;
      } else {
        leading = false;
        col += 1;
      }
    }
    T.lineOf = lineOf;
    return line + 1;
  }

  /** One <i> per source line. Same font metrics as the code, so it lines up. */
  function buildGutter(lines) {
    if (!el.gutter) return;
    const frag = document.createDocumentFragment();
    T.lineNodes = [];
    for (let n = 1; n <= lines; n++) {
      const item = document.createElement("i");
      item.textContent = n;
      frag.appendChild(item);
      T.lineNodes.push(item);
    }
    el.gutter.innerHTML = "";
    el.gutter.appendChild(frag);
    // widen the gutter for a long snippet so the digits never touch the code
    el.codeBox.style.setProperty("--ln-w", String(lines).length + 0.5 + "ch");
  }

  /**
   * offsetTop of the first character on each line, measured once. Reading it
   * per keystroke forced a layout on every key, which is what made the caret
   * lag behind on a long snippet.
   */
  function remeasure() {
    if (!T.chars.length) return;
    measureLines();
    T.curLine = -1;
    markLine();
  }

  function measureLines() {
    T.lineTops = [];
    let line = -1;
    for (let i = 0; i < T.chars.length; i++) {
      const at = T.lineOf[i];
      if (at !== line) {
        line = at;
        T.lineTops[at] = T.chars[i].offsetTop;
      }
    }
    if (!T.lineTops.length && T.chars.length) T.lineTops[0] = T.chars[0].offsetTop;
  }

  function renderCode(code, lang) {
    T.code = code;
    el.codeArea.innerHTML = Prism.highlight(code, grammarFor(lang), lang);
    T.chars = wrapChars(el.codeArea);
    if (T.chars.length !== code.length) {
      // highlighting desynced from source: fall back to plain text
      el.codeArea.textContent = code;
      T.chars = wrapChars(el.codeArea);
    }
    T.curSpan = null;
    T.curLine = -1;
    const lines = indexLines(code);
    buildGutter(lines);
    measureLines();
    resetRun();
  }

  function resetRun() {
    T.pos = 0;
    T.typed = 0;
    T.errors = 0;
    T.bad = false;
    T.startedAt = 0;
    T.running = false;
    cancelAnimationFrame(T.raf);
    for (const span of T.chars) span.classList.remove("done", "cur", "bad");
    T.curSpan = null;
    T.curLine = -1;
    el.codeBox.scrollTop = 0;
    if (el.suggest) el.suggest.classList.add("hidden");
    paintHud(0, 100, 0);
    el.hudLeft.textContent = T.code.length;
    markCursor();
  }

  /**
   * Move the caret. Only the two spans that change are touched - the old
   * version swept the whole snippet on every keystroke, so the caret fell
   * further behind the typing the longer the snippet was.
   */
  function markCursor() {
    if (T.curSpan) T.curSpan.classList.remove("cur");
    const span = T.chars[T.pos] || null;
    T.curSpan = span;
    if (span) span.classList.add("cur");
    markLine();
  }

  function lineHeight() {
    if (T.lineTops.length > 1) return T.lineTops[1] - T.lineTops[0];
    const probe = T.chars[0];
    return (probe && probe.offsetHeight) || 29;
  }

  /** Highlight the line being typed, in the gutter and behind the code. */
  function markLine() {
    const line = T.lineOf[Math.min(T.pos, T.lineOf.length - 1)] || 0;
    if (line === T.curLine) return;
    if (T.lineNodes[T.curLine]) T.lineNodes[T.curLine].classList.remove("on");
    T.curLine = line;
    if (T.lineNodes[line]) T.lineNodes[line].classList.add("on");
    if (el.lineGlow) {
      const top = T.lineTops[line];
      el.lineGlow.style.transform = "translateY(" + (top == null ? 0 : top) + "px)";
    }
  }

  /**
   * Keep the caret inside a comfortable band rather than only nudging it when
   * it leaves the box. With "keep the caret centred" on it rides a third of
   * the way down, so the next few lines are always already readable.
   */
  function scrollToCursor() {
    if (!T.chars.length) return;
    const box = el.codeBox;
    const line = T.lineOf[Math.min(T.pos, T.lineOf.length - 1)] || 0;
    const top = T.lineTops[line];
    if (top == null) return;
    const h = lineHeight();
    const view = box.clientHeight;
    if (box.scrollHeight <= view) return;  // nothing to scroll

    if (DISPLAY.caretScroll) {
      const want = top - view * 0.38;
      box.scrollTop = Math.max(0, Math.min(box.scrollHeight - view, want));
      return;
    }
    const pad = h * 2;
    if (top < box.scrollTop + pad) box.scrollTop = Math.max(0, top - pad);
    else if (top + h > box.scrollTop + view - pad)
      box.scrollTop = Math.min(box.scrollHeight - view, top + h - view + pad);
  }

  function armRace(endsAtMs) {
    T.running = true;
    R.over = false;
    if (!R.startedAt) {
      R.startedAt = performance.now();
      recStart();
    }
    if (endsAtMs != null) R.endsAt = endsAtMs;
    el.codeBox.classList.remove("locked");
    const strict = S.lobby && S.lobby.strict && !S.solo;
    const tips = S.lobby && S.lobby.suggest && !S.solo;
    el.hint.textContent = R.timed
      ? "type! — a new snippet appears while the clock runs"
      : tips
      ? "type! — Tab completes a keyword, and always clears indentation"
      : strict
      ? "type! — strict lobby: the indentation is yours to type (Tab for one level)"
      : "type! — Tab clears the indentation";
    focusTrap();
    loop();
  }

  function stopRace() {
    T.running = false;
    cancelAnimationFrame(T.raf);
  }

  function elapsed() {
    return T.startedAt ? (performance.now() - T.startedAt) / 1000 : 0;
  }

  function wpm() {
    const secs = elapsed();
    if (secs < 0.5) return 0;
    return (T.pos / 5) / (secs / 60);
  }

  function accuracy() {
    const total = T.typed + T.errors;
    return total ? (T.typed / total) * 100 : 100;
  }

  function paintHud(w, a, t) {
    el.hudWpm.textContent = Math.round(w);
    el.hudAcc.textContent = Math.round(a) + "%";
    el.hudTime.textContent = t.toFixed(1) + "s";
  }

  function loop() {
    if (!T.running) return;
    if (R.timed) {
      const left = remaining();
      paintHud(runWpm(), runAccuracy(), left);
      el.hudSnips.textContent = R.snips;
      if (R.endsAt && left <= 0) {
        timeUp();
        return;
      }
    } else {
      paintHud(wpm(), accuracy(), elapsed());
    }
    const now = performance.now();
    if (now - T.lastSend > 250) {
      T.lastSend = now;
      sendProgress();
      updateSelfBar();
    }
    T.raf = requestAnimationFrame(loop);
  }

  function autoSkipIndent() {
    // Strict lobbies make you type every space. It is the one real difficulty
    // lever the game has, so it belongs to the lobby, not to a preference.
    if (S.lobby && S.lobby.strict && !S.solo) return;
    if (T.pos === 0 || T.code[T.pos - 1] !== "\n") return;
    while (T.pos < T.code.length && (T.code[T.pos] === " " || T.code[T.pos] === "\t")) {
      T.chars[T.pos].classList.add("done");
      T.chars[T.pos].classList.remove("cur", "bad");
      T.pos++;
    }
  }

  function typeChar(ch) {
    if (!T.running || T.pos >= T.code.length) return;
    if (!T.startedAt) T.startedAt = performance.now();
    const expected = T.code[T.pos];
    const span = T.chars[T.pos];

    if (ch === expected) {
      T.bad = false;
      T.typed++;
      span.classList.remove("bad", "cur");
      span.classList.add("done");
      T.pos++;
      autoSkipIndent();
      recEvent(0);
      markCursor();
      scrollToCursor();
      paintSuggestion();
      el.hudLeft.textContent = T.code.length - T.pos;
      if (T.pos >= T.code.length) snippetDone();
      return;
    }

    T.errors++;
    T.bad = true;
    span.classList.add("bad");
    recEvent(1);
  }

  function backspace() {
    if (T.bad) {
      T.bad = false;
      const span = T.chars[T.pos];
      if (span) span.classList.remove("bad");
      return;
    }
    if (T.pos === 0) return;
    T.pos--;
    const span = T.chars[T.pos];
    span.classList.remove("done", "bad");
    recEvent(2);
    markCursor();
    scrollToCursor();
    paintSuggestion();
    el.hudLeft.textContent = T.code.length - T.pos;
  }

  /**
   * Tab, whatever the lobby is set to.
   *
   * It used to type a literal tab character, which only matched snippets that
   * were actually tab-indented - on a space-indented one, the indent key
   * scored an error. Now it clears the whitespace ahead of the caret in one
   * press: the whole run in a normal lobby, one level at a time in a strict
   * one, so strict still costs a keypress per level.
   *
   * With suggestions on it doubles as the accept key for a keyword, which is
   * only offered when the caret is on a word rather than on whitespace, so the
   * two uses never collide.
   */
  function tabKey() {
    if (!T.running || T.pos >= T.code.length) return;
    const ch = T.code[T.pos];
    if (ch !== " " && ch !== "\t") {
      if (suggestions()) acceptSuggestion();
      return;
    }
    if (!T.startedAt) T.startedAt = performance.now();
    const strict = suggestOff() && S.lobby && S.lobby.strict && !S.solo;
    let budget = strict ? INDENT : Infinity;
    while (T.pos < T.code.length && budget > 0) {
      const at = T.code[T.pos];
      if (at !== " " && at !== "\t") break;
      const span = T.chars[T.pos];
      span.classList.remove("bad", "cur");
      span.classList.add("done");
      T.typed++;
      budget -= at === "\t" ? INDENT : 1;
      T.pos++;
    }
    T.bad = false;
    recEvent(0);
    markCursor();
    scrollToCursor();
    paintSuggestion();
    el.hudLeft.textContent = T.code.length - T.pos;
    if (T.pos >= T.code.length) snippetDone();
  }

  function suggestOff() {
    return true;  // kept explicit: strict only limits Tab, never disables it
  }

  function onKeyDown(e) {
    if (!T.running || S.spectating) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "Backspace") { e.preventDefault(); backspace(); return; }
    if (e.key === "Enter") { e.preventDefault(); typeChar("\n"); return; }
    if (e.key === "Tab") { e.preventDefault(); tabKey(); return; }
    if (e.key.length === 1) { e.preventDefault(); typeChar(e.key); }
  }

  /* ---------- suggestions ----------
     A lobby option. The snippet is fixed, so a suggestion can only ever be the
     word the snippet already has at the caret - this is a speed aid, not free
     text. It is offered when that word is a keyword or builtin of the language
     being raced and you are partway into it; Tab types the rest.

     Prism already ships a keyword list per language, and using it means the
     suggestions match the highlighting the player is looking at rather than a
     second hand-kept list that would drift away from it. */
  const WORD_CHAR = /[A-Za-z0-9_$]/;
  const KEYWORDS = {};

  function keywordsFor(lang) {
    if (KEYWORDS[lang]) return KEYWORDS[lang];
    const found = new Set();
    const grammar = grammarFor(lang);
    const scan = (rule) => {
      if (!rule) return;
      if (Array.isArray(rule)) return rule.forEach(scan);
      if (rule instanceof RegExp) {
        // pull the plain words out of an alternation like \b(?:def|class)\b
        for (const word of String(rule.source).match(/[A-Za-z_][A-Za-z0-9_]{1,}/g) || []) {
          if (word.length >= 3) found.add(word);
        }
        return;
      }
      if (typeof rule === "object") {
        if (rule.pattern) scan(rule.pattern);
        if (rule.inside) scan(rule.inside);
        for (const key of Object.keys(rule)) {
          if (key === "pattern" || key === "inside") continue;
          scan(rule[key]);
        }
      }
    };
    for (const key of ["keyword", "builtin", "function", "class-name", "boolean"]) {
      if (grammar && grammar[key]) scan(grammar[key]);
    }
    KEYWORDS[lang] = found;
    return found;
  }

  function suggestions() {
    if (S.solo || !S.lobby || !S.lobby.suggest) return null;
    if (!T.running || T.bad || T.pos >= T.code.length) return null;
    // where the word under the caret starts and ends in the snippet
    let start = T.pos;
    while (start > 0 && WORD_CHAR.test(T.code[start - 1])) start--;
    if (start === T.pos) return null;      // not partway into a word yet
    let end = T.pos;
    while (end < T.code.length && WORD_CHAR.test(T.code[end])) end++;
    const word = T.code.slice(start, end);
    if (word.length < 3 || end === T.pos) return null;
    if (!keywordsFor(S.lobby.language).has(word)) return null;
    return { word, rest: T.code.slice(T.pos, end), end };
  }

  function acceptSuggestion() {
    const hit = suggestions();
    if (!hit) return;
    if (!T.startedAt) T.startedAt = performance.now();
    while (T.pos < hit.end) {
      const span = T.chars[T.pos];
      span.classList.remove("bad", "cur");
      span.classList.add("done");
      T.typed++;
      T.pos++;
    }
    T.bad = false;
    autoSkipIndent();
    recEvent(0);
    markCursor();
    scrollToCursor();
    paintSuggestion();
    el.hudLeft.textContent = T.code.length - T.pos;
    if (T.pos >= T.code.length) snippetDone();
  }

  /** The floating "⇥ print" hint, parked just under the caret. */
  function paintSuggestion() {
    const box = el.suggest;
    if (!box) return;
    const hit = suggestions();
    const span = hit ? T.chars[T.pos] : null;
    if (!hit || !span) {
      box.classList.add("hidden");
      return;
    }
    box.textContent = "\u21e5 " + hit.word;
    box.style.left = span.offsetLeft + "px";
    box.style.top = span.offsetTop + (span.offsetHeight || 24) + "px";
    box.classList.remove("hidden");
  }

  /** One snippet completed: bank it, then continue or end the race. */
  function snippetDone() {
    R.chars += T.code.length;
    R.typed += T.typed;
    R.errors += T.errors;
    R.snips += 1;
    el.hudSnips.textContent = R.snips;

    if (R.timed && remaining() > 0 && R.idx + 1 < R.playlist.length) {
      R.idx += 1;
      const next = R.playlist[R.idx];
      S.output = next.output || "";
      paintSnipMeta(next.level, next.topic);
      renderCode(next.code, S.lobby ? S.lobby.language : S.lang);
      armRace();
      recEvent(0);
      sendProgress();
      return;
    }
    finishRace();
  }

  /** The clock ran out. In a lobby the server has the last word. */
  function timeUp() {
    if (R.over) return;
    R.over = true;
    stopRace();
    el.codeBox.classList.add("locked");
    const w = runWpm();
    const a = runAccuracy();
    paintHud(w, a, 0);
    el.hint.textContent =
      "time — " + R.snips + " snippet(s), " + liveChars() + " chars, " + Math.round(w) + " wpm";
    const earned = starsFor(a, R.errors + T.errors, Math.max(1, liveChars()), R.snips > 0, false);
    showRun(earned, a, R.snips > 0);
    if (S.solo) {
      showTimedResult(w, a);
      recordSolo(w, a, runSeconds(), earned);
    } else {
      send({ t: "progress", p: T.pos / Math.max(1, T.code.length), wpm: w, acc: a,
             idx: R.idx, chars: liveChars(), snips: R.snips });
      // the clock ended this one, so nothing else carries the timeline
      const events = recTake();
      if (events) send({ t: "replay", events });
    }
  }

  function finishRace() {
    const timed = R.timed;
    const secs = timed ? runSeconds() : elapsed();
    const w = timed ? runWpm() : wpm();
    const a = timed ? runAccuracy() : accuracy();
    stopRace();
    paintHud(w, a, timed ? remaining() : secs);
    el.hint.textContent = timed
      ? "playlist cleared — " + R.snips + " snippet(s) at " + Math.round(w) + " wpm"
      : "done — " + Math.round(w) + " wpm / " + Math.round(a) + "% accuracy";
    el.codeBox.classList.add("locked");
    const earned = starsFor(a, R.errors + T.errors, Math.max(1, R.chars + T.code.length), true, false);
    showRun(earned, a, true);
    if (S.solo) {
      if (timed) showTimedResult(w, a);
      else showSoloResult(w, a, secs);
      recordSolo(w, a, secs, earned);
    } else {
      send({
        t: "finish",
        wpm: w,
        acc: a,
        time: secs,
        chars: liveChars(),
        snips: R.snips,
        replay: recTake(),
      });
      updateSelfBar(1);
    }
  }

  function focusTrap() {
    el.trap.focus({ preventScroll: true });
    el.codeBox.classList.add("focus");
  }

  // ---------- filters ----------
  function catalogFor(lang) {
    if (!S.meta) return null;
    return S.meta.catalog.find((c) => c.id === lang) || null;
  }

  function levelLabel(id) {
    const row = S.meta && S.meta.levels.find((l) => l.id === id);
    return row ? row.label : id;
  }

  function topicLabel(id) {
    const row = S.meta && S.meta.topics.find((t) => t.id === id);
    return row ? row.label : id;
  }

  /** Exact snippet count for a filter combination, from the level x topic table. */
  function countMatches(lang, levels, topics) {
    const cat = catalogFor(lang);
    if (!cat) return 0;
    const wantL = levels.length ? levels : S.meta.levels.map((l) => l.id);
    const wantT = topics.length ? topics : S.meta.topics.map((t) => t.id);
    let n = 0;
    for (const lv of wantL) {
      for (const tp of wantT) n += cat.combos[lv + "|" + tp] || 0;
    }
    return n;
  }

  function filterQuery() {
    const parts = [];
    if (S.levels.length) parts.push("levels=" + encodeURIComponent(S.levels.join(",")));
    if (S.topics.length) parts.push("topics=" + encodeURIComponent(S.topics.join(",")));
    return parts.join("&");
  }

  function chip(label, count, on, enabled, onClick) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip" + (on ? " on" : "") + (enabled ? "" : " off");
    b.innerHTML = '<span class="chip-label"></span><span class="chip-n"></span>';
    b.querySelector(".chip-label").textContent = label;
    b.querySelector(".chip-n").textContent = count;
    b.disabled = !enabled;
    if (enabled) b.onclick = onClick;
    return b;
  }

  function chipPlain(label, on, enabled, onClick) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "chip" + (on ? " on" : "") + (enabled ? "" : " off");
    b.textContent = label;
    b.disabled = !enabled;
    if (enabled) b.onclick = onClick;
    return b;
  }

  function toggle(list, id) {
    const i = list.indexOf(id);
    if (i >= 0) list.splice(i, 1);
    else list.push(id);
    return list;
  }

  function saveFilters() {
    localStorage.setItem("cr_levels", JSON.stringify(S.levels));
    localStorage.setItem("cr_topics", JSON.stringify(S.topics));
  }

  /** Drop topics that the chosen language has nothing for. */
  function pruneTopics() {
    const cat = catalogFor(S.lang);
    if (!cat) return;
    S.topics = S.topics.filter((t) => cat.topics[t]);
  }

  function renderFilters() {
    if (!S.meta) return;
    const cat = catalogFor(S.lang);
    if (!cat) return;

    el.levelChips.innerHTML = "";
    for (const lv of S.meta.levels) {
      const n = cat.levels[lv.id] || 0;
      el.levelChips.appendChild(
        chip(lv.label, n, S.levels.includes(lv.id), n > 0, () => {
          toggle(S.levels, lv.id);
          saveFilters();
          renderFilters();
        })
      );
    }

    el.topicChips.innerHTML = "";
    for (const tp of S.meta.topics) {
      const n = cat.topics[tp.id] || 0;
      if (!n) continue; // this language has nothing on that topic
      el.topicChips.appendChild(
        chip(tp.label, n, S.topics.includes(tp.id), true, () => {
          toggle(S.topics, tp.id);
          saveFilters();
          renderFilters();
        })
      );
    }

    const matches = countMatches(S.lang, S.levels, S.topics);
    el.levelHint.textContent = S.levels.length ? "" : "any";
    el.topicHint.textContent = S.topics.length ? S.topics.length + " picked" : "any";
    el.filterWarn.classList.toggle("hidden", matches > 0);
    el.filterWarn.textContent =
      "Nothing matches that combination for " +
      cat.label +
      " — a random " +
      cat.label +
      " snippet will be used instead.";
  }

  function renderRoomFilters(st) {
    if (!S.meta) return;
    const cat = catalogFor(st.language);
    if (!cat) return;
    const isHost = st.host === S.pid;
    const locked = !isHost || st.state === "countdown" || st.state === "racing";

    el.roomLevelChips.innerHTML = "";
    for (const lv of S.meta.levels) {
      const n = cat.levels[lv.id] || 0;
      el.roomLevelChips.appendChild(
        chip(lv.label, n, st.levels.includes(lv.id), n > 0 && !locked, () => {
          sendFilters(toggle(st.levels.slice(), lv.id), st.topics);
        })
      );
    }

    el.roomTopicChips.innerHTML = "";
    for (const tp of S.meta.topics) {
      const n = cat.topics[tp.id] || 0;
      if (!n) continue;
      el.roomTopicChips.appendChild(
        chip(tp.label, n, st.topics.includes(tp.id), !locked, () => {
          sendFilters(st.levels, toggle(st.topics.slice(), tp.id));
        })
      );
    }

    el.roomFilterNote.textContent = locked
      ? isHost
        ? "filters are locked while a race is running"
        : "only the host can change the filters"
      : st.matches + " snippet(s) match — next race picks one of them";
  }

  function durationLabel(seconds) {
    const row = DURATIONS.find((d) => d.v === seconds);
    if (row) return row.label;
    return seconds ? seconds + "s" : "One snippet";
  }

  function renderDurations() {
    el.durationChips.innerHTML = "";
    for (const d of DURATIONS) {
      el.durationChips.appendChild(
        chipPlain(d.label, S.duration === d.v, true, () => {
          S.duration = d.v;
          localStorage.setItem("cr_duration", String(d.v));
          renderDurations();
        })
      );
    }
    el.durationHint.textContent = S.duration ? "timed" : "classic";
  }

  function renderRoomDurations(st) {
    el.roomDurationChips.innerHTML = "";
    const locked = st.host !== S.pid || st.state === "countdown" || st.state === "racing";
    for (const d of DURATIONS) {
      el.roomDurationChips.appendChild(
        chipPlain(d.label, st.duration === d.v, !locked, () => {
          send({ t: "duration", v: d.v });
        })
      );
    }
  }

  function sendFilters(levels, topics) {
    S.levels = levels.slice();
    S.topics = topics.slice();
    saveFilters();
    send({ t: "filters", levels, topics });
  }

  function paintSnipMeta(level, topic) {
    S.snipLevel = level || "";
    S.snipTopic = topic || "";
    if (!level && !topic) {
      el.snipMeta.textContent = "";
      el.snipMeta.className = "snip-meta";
      return;
    }
    el.snipMeta.textContent = levelLabel(level) + " · " + topicLabel(topic);
    el.snipMeta.className = "snip-meta lvl-" + level;
  }

  // ---------- profile ----------
  function avatarUrl(uid, version) {
    return "/api/avatar/" + uid + "?v=" + (version || 0);
  }

  function paintAvatar(node, who) {
    // bots get a generated identicon instead of an upload
    if (who && who.bot && who.slug) {
      node.style.backgroundImage = 'url("/api/bot-avatar/' + who.slug + '")';
      node.textContent = "";
      node.classList.add("has-img", "is-bot");
      return;
    }
    node.classList.remove("is-bot");
    const uid = who.uid != null ? who.uid : who.id;
    const version = who.avatar || 0;
    if (uid) {
      // the server falls back to a generated identicon, so this always resolves
      node.style.backgroundImage = 'url("' + avatarUrl(uid, version) + '")';
      node.textContent = "";
      node.classList.add("has-img");
    } else {
      node.style.backgroundImage = "";
      node.classList.remove("has-img");
      node.textContent = ((who.name || "?").trim().charAt(0) || "?").toUpperCase();
    }
  }

  function starsHtml(count) {
    let out = "";
    for (let i = 0; i < 3; i++) {
      out += '<span class="star' + (i < count ? " on" : "") + '">' + (i < count ? "★" : "☆") + "</span>";
    }
    return out;
  }

  const STAR_NOTES = {
    3: "Clean run",
    2: "Solid, a few slips",
    1: "Messy - lots of corrections",
    0: "Rough one",
  };

  /** Same thresholds the server uses, so the panel and the DB agree. */
  function starsFor(acc, errors, length, completed, won) {
    if (!completed) return 0;
    const rate = Math.max(0, errors) / Math.max(1, length);
    let earned = 0;
    if (acc >= 96 && rate <= 0.04) earned = 3;
    else if (acc >= 88 && rate <= 0.12) earned = 2;
    else if (acc >= 72) earned = 1;
    // winning is worth a star, so out-typing everyone cannot score below a
    // tidier opponent who covered a third of the distance
    if (won && earned) earned = Math.min(3, earned + 1);
    return earned;
  }

  /* ---------- simulated run panel ---------- */
  function showRun(stars, acc, ok) {
    clearInterval(S.runTimer);
    el.runStars.innerHTML = starsHtml(stars) +
      '<em class="star-note">' + (STAR_NOTES[stars] || "") + "</em>";
    el.runPanel.classList.remove("hidden");

    if (!ok) {
      el.runTitle.textContent = "not run";
      el.runOut.textContent = "Snippet incomplete - nothing to run.";
      return;
    }
    el.runTitle.textContent = "simulated run";
    const text = S.output || "Compiled with no errors. This snippet produces no output.";
    // type the transcript out, so it reads like a program starting up
    el.runOut.textContent = "";
    let i = 0;
    S.runTimer = setInterval(() => {
      el.runOut.textContent = text.slice(0, i);
      i += Math.max(1, Math.ceil(text.length / 90));
      if (i > text.length) {
        el.runOut.textContent = text;
        clearInterval(S.runTimer);
      }
    }, 16);
  }

  /* ---------- outcome overlay ---------- */
  function showOutcome(st) {
    const me = st.players.find((p) => p.id === S.pid);
    if (!me || !me.finished) return;

    const others = st.players.filter((p) => p.id !== S.pid);
    const won = me.place === 1;
    const timed = st.duration > 0;
    const beaten = others.filter((p) => (p.place || 99) > (me.place || 99));
    const ahead = others.filter((p) => (p.place || 99) < (me.place || 99));

    el.winStars.innerHTML = "";
    for (let i = 0; i < 3; i++) {
      const star = document.createElement("span");
      star.className = "wstar" + (i < (me.stars || 0) ? " on" : "");
      star.textContent = i < (me.stars || 0) ? "★" : "☆";
      star.style.animationDelay = i * 140 + "ms";
      el.winStars.appendChild(star);
    }

    el.winModal.classList.toggle("won", won);
    el.winTitle.textContent = others.length
      ? won ? "You win!" : "Beaten this time"
      : "Run complete";

    if (!others.length) el.winSub.textContent = "";
    else if (won)
      el.winSub.textContent =
        "You beat " +
        (beaten.length === 1 ? beaten[0].name : beaten.length + " opponents");
    else
      el.winSub.textContent =
        (ahead.length === 1 ? ahead[0].name : ahead.length + " racers") + " got there first";

    el.winWpm.textContent = Math.round(me.wpm);
    el.winAcc.textContent = Math.round(me.acc) + "%";
    el.winPlace.textContent = me.place ? "#" + me.place : "-";
    el.winDeltaBox.classList.toggle("hidden", !me.delta);
    if (me.delta) {
      el.winDelta.textContent = (me.delta > 0 ? "+" : "") + me.delta;
      el.winDelta.className = me.delta > 0 ? "up" : "down";
    }
    el.winNote.textContent = timed
      ? (me.snips || 0) + " snippets, " + (me.chars || 0) + " characters - " +
        (STAR_NOTES[me.stars] || "")
      : (STAR_NOTES[me.stars] || "");

    el.winModal.classList.remove("hidden");
  }

  function hideOutcome() {
    el.winModal.classList.add("hidden");
  }

  function hideRun() {
    clearInterval(S.runTimer);
    el.runPanel.classList.add("hidden");
  }

  /* ---------- opponent carets ---------- */
  function paintGhosts() {
    if (!el.ghosts) return;
    if (!S.lobby || S.solo || !T.chars.length) {
      el.ghosts.innerHTML = "";
      return;
    }
    // Watching: nobody is typing here, so the carets get names on them and the
    // race is readable from the outside.
    el.ghosts.classList.toggle("labelled", !!S.spectating);
    const alive = new Set();
    for (const p of S.lobby.players) {
      if (p.id === S.pid || (p.finished && !S.spectating)) continue;
      // only show racers working on the same snippet as me
      if ((p.idx || 0) !== R.idx) continue;
      const span = T.chars[Math.min(p.pos || 0, T.chars.length - 1)];
      if (!span) continue;
      alive.add(p.id);
      let node = el.ghosts.querySelector('.peer[data-id="' + p.id + '"]');
      if (!node) {
        node = document.createElement("i");
        node.className = "peer";
        node.dataset.id = p.id;
        node.appendChild(document.createElement("b"));
        el.ghosts.appendChild(node);
      }
      const label = node.querySelector("b");
      if (label) label.textContent = p.name;
      node.style.setProperty("--c", ghostColor(p.id));
      node.style.left = span.offsetLeft + "px";
      node.style.top = span.offsetTop + "px";
      node.style.height = (span.offsetHeight || 22) + "px";
      node.title = p.name;  // hover only while racing: a label covers the code
      // flag whoever is ahead of me, so a rush is obvious
      const me = S.lobby.players.find((x) => x.id === S.pid);
      node.classList.toggle("ahead", !!me && (p.progress || 0) > (me.progress || 0));
    }
    for (const node of [...el.ghosts.children]) {
      if (!alive.has(node.dataset.id)) node.remove();
    }
  }

  function paintProfile() {
    const known = !!S.me;
    // accounts are automatic, so the button is only hidden with no database
    el.profileBtn.classList.toggle("hidden", !S.accounts);
    el.nameField.classList.toggle("hidden", S.accounts);
    if (known) {
      el.profileName.textContent = S.me.name;
      el.profileBtn.title = S.me.name + " - " + S.me.rank + " (" + S.me.rating + ")";
      el.profileRate.textContent = S.me.rating;
      el.profileRate.title = S.me.rank;
      paintAvatar(el.profileAvatar, S.me);
      el.name.value = S.me.name;
    }
  }

  async function loadMe() {
    try {
      const res = await fetch("/api/me", { credentials: "same-origin" });
      const data = await res.json();
      S.accounts = !!data.accounts;
      S.me = data.user || null;
    } catch (err) {
      S.accounts = false;
      S.me = null;
    }
    paintProfile();
    if (S.me && S.me.settings) adoptDisplay(S.me.settings);
    if (S.accounts) loadLeaderboard();
    if (S.me) startHeartbeat();
  }

  async function loadLeaderboard() {
    try {
      const res = await fetch("/api/leaderboard?limit=10");
      const { rows } = await res.json();
      if (!rows || !rows.length) {
        el.lbPanel.classList.add("hidden");
        return;
      }
      el.leaderboard.innerHTML = "";
      rows.forEach((row, i) => {
        const line = document.createElement("div");
        line.className = "lb-row" + (S.me && S.me.id === row.id ? " me" : "");
        line.innerHTML =
          '<span class="lb-i"></span><span class="avatar sm"></span>' +
          '<span class="lb-name"></span><b class="lb-wpm"></b><span class="lb-acc"></span>';
        line.querySelector(".lb-i").textContent = i + 1;
        line.querySelector(".lb-name").textContent = row.name;
        line.querySelector(".lb-wpm").textContent = Math.round(row.best_wpm) + " wpm";
        line.querySelector(".lb-acc").textContent = Math.round(row.best_acc) + "%";
        paintAvatar(line.querySelector(".avatar"), row);
        el.leaderboard.appendChild(line);
      });
      el.lbPanel.classList.remove("hidden");
    } catch (err) {
      el.lbPanel.classList.add("hidden");
    }
  }

  /* One swatch per theme. Clicking applies it immediately - a theme you have
     to save before you can see is a theme nobody tries. */
  function renderThemes() {
    const grid = el2("themeGrid");
    if (!grid) return;
    grid.innerHTML = "";
    for (const theme of THEMES) {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "theme-card" + (theme.id === DISPLAY.theme ? " on" : "");
      card.dataset.theme = theme.id;
      card.innerHTML =
        '<span class="theme-swatch">' +
        theme.swatch
          .map((c) => '<i style="background:' + c + '"></i>')
          .join("") +
        '</span><span class="theme-name"></span>';
      card.querySelector(".theme-name").textContent = theme.label;
      card.onclick = () => {
        DISPLAY.theme = theme.id;
        saveDisplay();
        renderThemes();
      };
      grid.appendChild(card);
    }
  }

  function wireDisplayToggles() {
    const pairs = [
      ["optLineNumbers", "lineNumbers"],
      ["optIndentGuides", "indentGuides"],
      ["optCaretScroll", "caretScroll"],
    ];
    for (const [id, key] of pairs) {
      const box = el2(id);
      if (!box) continue;
      box.checked = DISPLAY[key];
      box.onchange = () => {
        DISPLAY[key] = box.checked;
        saveDisplay();
      };
    }
  }

  /** Country and birth-year pickers, built once and reused. */
  function fillAboutFields() {
    if (!COUNTRY_COMBO) {
      // sorted by the name the reader actually sees, not by the code
      const items = [{ value: "", label: "Rather not say" }].concat(
        COUNTRY_CODES.map((code) => ({ value: code, label: countryName(code) })).sort(
          (a, b) => a.label.localeCompare(b.label)
        )
      );
      COUNTRY_COMBO = makeCombo("pfCountryCombo", { items });
    }

    const year = el2("pfBirthYear");
    if (year && !year.options.length) {
      const blank = document.createElement("option");
      blank.value = "";
      blank.textContent = "Rather not say";
      year.appendChild(blank);
      const now = new Date().getFullYear();
      for (let y = now; y >= now - 100; y--) {
        const opt = document.createElement("option");
        opt.value = String(y);
        // the age this year of birth works out to, so nobody has to do the sum
        opt.textContent = y + "  (" + (now - y) + ")";
        year.appendChild(opt);
      }
    }
  }

  function openProfile() {
    renderThemes();
    wireDisplayToggles();
    fillAboutFields();
    if (COUNTRY_COMBO) COUNTRY_COMBO.set((S.me && S.me.country) || "");
    el2("pfBirthYear").value = (S.me && S.me.birth_year) ? String(S.me.birth_year) : "";
    el2("pfGender").value = (S.me && S.me.gender) || "";
    el.pfErr.textContent = "";
    el.pfAvatar.value = "";
    el.pfTitle.textContent = "Your profile";
    el.pfName.value = S.me ? S.me.name : (el.name.value || "").trim();
    el.pfRemove.classList.toggle("hidden", !(S.me && S.me.avatar));
    paintAvatar(el.pfPreview, S.me || { name: el.pfName.value });
    el.pfNameNote.textContent = "";
    el.pfNameNote.className = "name-note";
    paintIdeas([]);
    closeCropper();
    closeCoverCropper();
    el.cvRemove.classList.toggle("hidden", !(S.me && S.me.cover));
    el.modal.classList.remove("hidden");
    el.pfName.focus();
  }

  function closeProfile() {
    el.modal.classList.add("hidden");
  }

  /* ---------- avatar cropper ---------- */
  const CROP_PX = 256;
  const CROP = { img: null, zoom: 1, x: 0, y: 0, drag: null };
  // The cover is the same cropper at a banner aspect. Its canvas carries the
  // output size, so the drawing code below never hard-codes either shape.
  const COVER = { img: null, zoom: 1, x: 0, y: 0, drag: null };

  function paintCrop(state, canvas) {
    const cw = canvas.width;
    const ch = canvas.height;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, cw, ch);
    if (!state.img) return;
    const img = state.img;
    // "cover" the frame, then apply the zoom and the drag offset
    const base = Math.max(cw / img.width, ch / img.height);
    const scale = base * state.zoom;
    const w = img.width * scale;
    const h = img.height * scale;
    const maxX = Math.max(0, (w - cw) / 2);
    const maxY = Math.max(0, (h - ch) / 2);
    state.x = Math.max(-maxX, Math.min(maxX, state.x));
    state.y = Math.max(-maxY, Math.min(maxY, state.y));
    ctx.drawImage(img, (cw - w) / 2 + state.x, (ch - h) / 2 + state.y, w, h);
  }

  function drawCrop() {
    paintCrop(CROP, el.pfCanvas);
  }

  function drawCover() {
    paintCrop(COVER, el.cvCanvas);
  }

  function openCoverCropper(file) {
    if (!file) return;
    if (!/^image\/(png|jpeg|gif|webp)$/.test(file.type)) {
      el.pfErr.textContent = "use a png, jpeg, gif or webp";
      return;
    }
    if (file.size > 12 * 1024 * 1024) {
      el.pfErr.textContent = "that cover is too big to load (12 MB max)";
      return;
    }
    el.pfErr.textContent = "";
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      COVER.img = img;
      COVER.zoom = 1;
      COVER.x = 0;
      COVER.y = 0;
      el.cvZoom.value = "100";
      el.cvCrop.classList.remove("hidden");
      el.cvDrop.classList.add("hidden");
      drawCover();
      URL.revokeObjectURL(url);
    };
    img.onerror = () => {
      el.pfErr.textContent = "could not read that image";
      URL.revokeObjectURL(url);
    };
    img.src = url;
  }

  function closeCoverCropper() {
    COVER.img = null;
    el.cvCrop.classList.add("hidden");
    el.cvDrop.classList.remove("hidden");
    el.cvFile.value = "";
  }

  function coverBlob() {
    if (!COVER.img) return Promise.resolve(null);
    return new Promise((resolve) => {
      el.cvCanvas.toBlob(
        (blob) => resolve(blob ? new File([blob], "cover.webp", { type: blob.type }) : null),
        "image/webp",
        0.86
      );
    });
  }

  /** Drag to reposition, for either cropper. */
  function dragCrop(stage, state, redraw) {
    if (!stage) return;
    const down = (e) => {
      if (!state.img) return;
      const point = e.touches ? e.touches[0] : e;
      state.drag = { x: point.clientX, y: point.clientY, ox: state.x, oy: state.y };
      e.preventDefault();
    };
    const move = (e) => {
      if (!state.drag) return;
      const point = e.touches ? e.touches[0] : e;
      state.x = state.drag.ox + (point.clientX - state.drag.x);
      state.y = state.drag.oy + (point.clientY - state.drag.y);
      redraw();
      e.preventDefault();
    };
    const up = () => { state.drag = null; };
    stage.addEventListener("mousedown", down);
    stage.addEventListener("touchstart", down, { passive: false });
    window.addEventListener("mousemove", move);
    window.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("mouseup", up);
    window.addEventListener("touchend", up);
  }

  function openCropper(file) {
    if (!file) return;
    if (!/^image\/(png|jpeg|gif|webp)$/.test(file.type)) {
      el.pfErr.textContent = "use a png, jpeg, gif or webp";
      return;
    }
    if (file.size > 8 * 1024 * 1024) {
      el.pfErr.textContent = "that image is too big to load (8 MB max)";
      return;
    }
    el.pfErr.textContent = "";
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      CROP.img = img;
      CROP.zoom = 1;
      CROP.x = 0;
      CROP.y = 0;
      el.pfZoom.value = "100";
      el.pfCrop.classList.remove("hidden");
      el.pfDrop.classList.add("hidden");
      drawCrop();
      URL.revokeObjectURL(url);
    };
    img.onerror = () => {
      el.pfErr.textContent = "could not read that image";
      URL.revokeObjectURL(url);
    };
    img.src = url;
  }

  function closeCropper() {
    CROP.img = null;
    el.pfCrop.classList.add("hidden");
    el.pfDrop.classList.remove("hidden");
    el.pfAvatar.value = "";
  }

  /** The cropped square as a file, or null when nothing was picked. */
  function croppedBlob() {
    if (!CROP.img) return Promise.resolve(null);
    return new Promise((resolve) => {
      el.pfCanvas.toBlob(
        (blob) => resolve(blob ? new File([blob], "avatar.webp", { type: blob.type }) : null),
        "image/webp",
        0.9
      );
    });
  }

  /* ---------- name availability ---------- */
  let nameTimer = 0;

  function paintIdeas(list) {
    el.pfIdeas.innerHTML = "";
    for (const idea of list || []) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "idea";
      chip.textContent = idea;
      chip.onclick = () => {
        el.pfName.value = idea;
        checkName();
      };
      el.pfIdeas.appendChild(chip);
    }
  }

  async function checkName() {
    const name = (el.pfName.value || "").trim();
    if (!name) {
      el.pfNameNote.textContent = "";
      el.pfNameNote.className = "name-note";
      paintIdeas([]);
      return true;
    }
    if (S.me && name.toLowerCase() === S.me.name.toLowerCase()) {
      el.pfNameNote.textContent = "this is your current name";
      el.pfNameNote.className = "name-note ok";
      paintIdeas([]);
      return true;
    }
    try {
      const res = await fetch("/api/name-check?name=" + encodeURIComponent(name));
      const data = await res.json();
      if (data.ok) {
        el.pfNameNote.textContent = "available";
        el.pfNameNote.className = "name-note ok";
        paintIdeas([]);
        return true;
      }
      el.pfNameNote.textContent = '"' + data.name + '" is already taken - try:';
      el.pfNameNote.className = "name-note bad";
      paintIdeas(data.suggestions);
      return false;
    } catch (err) {
      el.pfNameNote.textContent = "";
      return true;
    }
  }

  async function saveProfile() {
    const name = (el.pfName.value || "").trim().slice(0, 18);
    if (!name) {
      el.pfErr.textContent = "pick a display name";
      return;
    }
    el.pfSave.disabled = true;
    el.pfErr.textContent = "";
    try {
      const res = await fetch("/api/profile", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        // Blank means "rather not say", and the server stores that as unset.
        body: JSON.stringify({
          name,
          country: el2("pfCountry").value || "",
          birth_year: el2("pfBirthYear").value || "",
          gender: el2("pfGender").value || "",
        }),
      });
      const data = await res.json();
      if (res.status === 409) {
        el.pfNameNote.textContent = '"' + data.name + '" is already taken - try:';
        el.pfNameNote.className = "name-note bad";
        paintIdeas(data.suggestions);
        el.pfErr.textContent = "pick a free name";
        return;
      }
      if (!res.ok) {
        el.pfErr.textContent = data.error || "could not save";
        return;
      }
      S.me = data.user;
      localStorage.setItem("cr_name", name);

      // The cover goes up on its own request, after the profile itself, so a
      // failed banner never costs the player their name change.
      const cover = await coverBlob();
      if (cover) {
        const form = new FormData();
        form.append("file", cover);
        const up = await fetch("/api/cover", {
          method: "POST",
          credentials: "same-origin",
          body: form,
        });
        const upData = await up.json().catch(() => ({}));
        if (!up.ok) {
          el.pfErr.textContent =
            upData.error === "too_large"
              ? "the cover is over 1.5 MB"
              : upData.error || "cover upload failed";
          return;
        }
        S.me.cover = upData.cover_version;
        closeCoverCropper();
      }

      const file = await croppedBlob();
      if (file) {
        const form = new FormData();
        form.append("file", file);
        const up = await fetch("/api/avatar", {
          method: "POST",
          credentials: "same-origin",
          body: form,
        });
        const upData = await up.json();
        if (!up.ok) {
          el.pfErr.textContent =
            upData.error === "too_large"
              ? "image is over 512 KB"
              : upData.error === "unsupported_type"
              ? "use a png, jpeg, gif or webp"
              : upData.error || "image upload failed";
          paintProfile();
          return;
        }
        S.me.avatar = upData.avatar_version;
        closeCropper();
      }
      paintProfile();
      loadLeaderboard();
      closeProfile();
    } catch (err) {
      el.pfErr.textContent = "network error";
    } finally {
      el.pfSave.disabled = false;
    }
  }

  async function removeAvatar() {
    try {
      await fetch("/api/avatar", { method: "DELETE", credentials: "same-origin" });
      if (S.me) S.me.avatar = 0;
      el.pfRemove.classList.add("hidden");
      paintAvatar(el.pfPreview, S.me || { name: el.pfName.value });
      paintProfile();
      loadLeaderboard();
    } catch (err) {
      el.pfErr.textContent = "could not remove the image";
    }
  }

  async function recordSolo(w, a, secs, earned) {
    if (!S.me) return;
    try {
      await fetch("/api/race", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          language: S.lang,
          level: S.snipLevel,
          topic: S.snipTopic,
          wpm: w,
          acc: a,
          seconds: secs,
          length: Math.max(1, R.chars + T.code.length),
          errors: R.errors + T.errors,
          completed: true,
          replay: recTake(),
          snippets: recSnippets(),
        }),
      });
      loadLeaderboard();
      loadMe();
    } catch (err) {
      /* a lost stat must never break the run */
    }
  }

  // ---------- networking ----------
  function send(msg) {
    if (S.ws && S.ws.readyState === WebSocket.OPEN) S.ws.send(JSON.stringify(msg));
  }

  function sendProgress() {
    if (S.solo) return;
    send({
      t: "progress",
      p: T.pos / Math.max(1, T.code.length),
      wpm: R.timed ? runWpm() : wpm(),
      acc: R.timed ? runAccuracy() : accuracy(),
      pos: T.pos,
      idx: R.idx,
      chars: liveChars(),
      snips: R.snips,
    });
  }

  function connect(code, create, opts) {
    opts = opts || {};
    if (S.ws) { S.ws.onclose = null; S.ws.close(); }
    S.spectating = !!opts.spectate;
    S.lobby = null;  // a stale lobby made the next state look unchanged
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    const qs = new URLSearchParams({
      name: currentName(),
      pid: S.pid,
      create: create ? "1" : "0",
      lang: S.lang,
      levels: S.levels.join(","),
      topics: S.topics.join(","),
      duration: String(S.duration == null ? -1 : S.duration),
      spectate: opts.spectate ? "1" : "0",
      key: opts.key != null ? opts.key : S.lobbyKey || "",
      private: opts.private ? "1" : "0",
      title: opts.title || "",
    });
    const ws = new WebSocket(proto + "//" + location.host + "/ws/" + code + "?" + qs);
    S.ws = ws;
    ws.onmessage = (ev) => handle(JSON.parse(ev.data));
    ws.onclose = () => {
      if (S.room) addChat({ sys: true, text: "disconnected" });
    };
    ws.onerror = () => {};
  }

  function handle(m) {
    switch (m.t) {
      case "hello":
        S.pid = m.id;
        S.room = m.code;
        S.spectating = !!m.spectator;
        localStorage.setItem("cr_pid", m.id);
        el.name.value = m.name;
        el.roomCode.textContent = m.code;
        el.codeText.textContent = m.code;
        history.replaceState(null, "", "/race/" + m.code);
        showRoom();
        break;
      case "error":
        showHome();
        el.homeErr.textContent =
          m.code === "no_lobby"
            ? "lobby not found"
            : m.code === "bad_key"
            ? "that lobby needs a key"
            : m.code === "full"
            ? "that lobby is full (" + (m.limit || "") + ") — you can still spectate"
            : "connection error";
        break;
      case "chat":
        addChat(m);
        break;
      case "state":
        applyState(m);
        break;
      case "prog":
        applyProg(m);
        break;
      case "countdown":
        showCountdown(m.n);
        break;
      case "go": {
        el.countdown.classList.add("hidden");
        if (S.spectating) break;
        if (S.lobby) {
          initRun(S.lobby.duration > 0, S.lobby.playlist || []);
          const first = R.playlist[0];
          if (first) {
            S.output = first.output || "";
            paintSnipMeta(first.level, first.topic);
            renderCode(first.code, S.lobby.language);
          }
        }
        // start_ts is in the past for someone who joined mid-race, so a timed
        // race gives them what is left of the clock, not a fresh full one.
        const timed = S.lobby && S.lobby.duration > 0;
        const endsMs = m.ends_at ? m.ends_at * 1000 - Date.now() : 0;
        armRace(
          timed
            ? performance.now() +
                Math.max(0, m.ends_at ? endsMs : S.lobby.duration * 1000)
            : null
        );
        break;
      }
      case "time_up":
        timeUp();
        break;
    }
  }

  function applyState(st) {
    const prev = S.lobby;
    S.lobby = st;
    el.langSelect.value = st.language;
    el.langSelect.disabled = st.host !== S.pid || st.state !== "waiting";
    el.stateBadge.textContent = st.state;
    el.stateBadge.className = "badge " + st.state;
    paintSnipMeta(st.level, st.topic);
    renderRoomFilters(st);
    renderRoomDurations(st);

    const watching = S.spectating;
    const isHost = !watching && st.host === S.pid;
    const me = watching ? null : st.players.find((p) => p.id === S.pid);
    el.ready.classList.toggle("hidden", watching || st.state !== "waiting");
    el.start.classList.toggle("hidden", !(isHost && st.state === "waiting"));
    // Give up is only offered to someone actually racing and still going.
    el.resign.classList.toggle(
      "hidden",
      !(!watching && st.state === "racing" && me && !me.finished)
    );
    paintWatchers(st);

    // Lobby mode. Only the host may change either, and only before the start.
    const strictBox = el2("roomStrict");
    const rankedBox = el2("roomRanked");
    const limitBox = el2("roomLimit");
    const suggestBox = el2("roomSuggest");
    if (strictBox && rankedBox) {
      strictBox.checked = !!st.strict;
      rankedBox.checked = st.ranked !== false;
      const settled = !isHost || st.state === "countdown" || st.state === "racing";
      strictBox.disabled = settled;
      rankedBox.disabled = settled;
      if (suggestBox) {
        suggestBox.checked = !!st.suggest;
        suggestBox.disabled = settled;
      }
      if (limitBox) {
        limitBox.value = String(st.limit || 0);
        limitBox.disabled = settled;
      }
    }
    el.stateBadge.title =
      (st.strict ? "strict typing" : "indentation auto-skipped") +
      " · " + (st.suggest ? "suggestions on" : "no suggestions") +
      " · " + (st.ranked === false ? "unranked" : "ranked");
    const over = st.state === "finished";
    el.again.classList.toggle("hidden", !(isHost && over));
    el.newSnip.classList.toggle("hidden", !(isHost && over));
    if (over) {
      el.again.textContent = "Race again";
      el.hint.textContent = isHost
        ? "Race again for a fresh snippet, or Another snippet to pick one without starting"
        : "waiting for the host to start the next race…";
    }
    if (me) {
      el.ready.textContent = me.ready ? "Unready" : "Ready";
      el.ready.classList.toggle("accent", !!me.ready);
    }

    // Only a running race is off limits for a racer: during the countdown the
    // new snippet should already be on screen so they can read ahead.
    // A spectator, and anyone who walked in mid-race, is not typing, so they
    // get the snippet immediately - without this they sat in front of an empty
    // code area until the round ended.
    const idle = watching || !me || me.finished;
    const armed = st.state === "racing" && !idle;
    // Nothing rendered yet: either a fresh join or a walk-in on a race already
    // running. Either way the run has to be set up even though `armed` would
    // normally mean "leave the code alone, someone is typing on it".
    const fresh = !T.chars.length;
    if (
      fresh ||
      (!armed && (!prev || prev.state !== st.state || prev.snippet !== st.snippet))
    ) {
      initRun(st.duration > 0, st.playlist || []);
    }

    const snippetChanged =
      !prev || prev.snippet !== st.snippet || prev.language !== st.language;
    if (fresh || (snippetChanged && !armed)) {
      renderCode(st.snippet, st.language);
    }
    if (idle) el.codeBox.classList.add("locked");

    if (st.state === "waiting" || st.state === "finished") {
      stopRace();
      el.codeBox.classList.add("locked");
      if (st.state === "waiting") {
        el.hint.textContent = isHost
          ? "press Start (or everyone ready) to launch the race"
          : "waiting for the host to start…";
        el.results.classList.add("hidden");
        el.countdown.classList.add("hidden");
      }
    }
    S.output = st.output || "";
    if (st.state === "waiting" || st.state === "countdown") {
      hideRun();
      hideOutcome();
    }
    paintGhosts();
    el.addBotBtn.classList.toggle(
      "hidden",
      !(isHost && (st.state === "waiting" || st.state === "finished"))
    );
    if (!watching && st.state === "racing" && !T.running && !R.over && me && !me.finished) {
      // ends_at is a unix time in seconds; the server ends the race either way.
      const leftMs = st.ends_at ? st.ends_at * 1000 - Date.now() : 0;
      armRace(st.duration > 0 ? performance.now() + Math.max(0, leftMs) : null);
    }

    renderRacers(st);
    if (st.state === "finished") {
      renderResults(st);
      showOutcome(st);
      if (S.me) {
        loadLeaderboard();
        loadMe();  // the rating may have moved
      }
      if (!el.ranks.classList.contains("hidden")) loadRankings();
    }
  }

  function applyProg(m) {
    if (!S.lobby) return;
    const p = S.lobby.players.find((x) => x.id === m.id);
    if (!p) return;
    p.progress = m.p;
    p.wpm = m.wpm;
    p.acc = m.acc;
    if (m.chars != null) p.chars = m.chars;
    if (m.snips != null) p.snips = m.snips;
    if (m.idx != null) p.idx = m.idx;
    if (m.pos != null) p.pos = m.pos;
    paintRacer(p);
    paintGhosts();
  }

  function updateSelfBar(force) {
    if (!S.lobby) return;
    const me = S.lobby.players.find((p) => p.id === S.pid);
    if (!me) return;
    me.progress = force != null ? force : T.pos / Math.max(1, T.code.length);
    me.wpm = R.timed ? runWpm() : wpm();
    me.acc = R.timed ? runAccuracy() : accuracy();
    me.chars = liveChars();
    me.snips = R.snips;
    paintRacer(me);
  }

  function racerRow(p) {
    const row = document.createElement("div");
    row.className = "racer" + (p.id === S.pid ? " me" : "");
    row.dataset.id = p.id;
    row.innerHTML =
      '<div class="who"><span class="dotc"></span><span class="avatar sm"></span>' +
      '<span class="nm"></span><span class="rate sm"></span><span class="tag"></span></div>' +
      '<div class="bar"><i></i></div>' +
      '<div class="stat"><b class="w">0</b> wpm · <span class="a">100</span>%</div>';
    el.racers.appendChild(row);
    return row;
  }

  function paintRacer(p) {
    const row = el.racers.querySelector('.racer[data-id="' + p.id + '"]');
    if (!row) return;
    row.querySelector(".nm").textContent = p.name;
    paintAvatar(row.querySelector(".avatar"), p);
    row.classList.toggle("is-bot", !!p.bot);
    const dot = row.querySelector(".dotc");
    if (dot) {
      // matches this racer's caret colour in the code area
      dot.style.background = p.id === S.pid ? "var(--accent)" : ghostColor(p.id);
    }
    const rate = row.querySelector(".rate");
    if (rate) {
      rate.textContent = p.rating || "";
      rate.title = (p.rank || "") + (p.bot ? " (bot)" : "");
    }
    const tag = row.querySelector(".tag");
    const host = S.lobby && S.lobby.host === p.id;
    let label = "";
    if (p.place) label = "#" + p.place;
    else if (p.finished) label = "done";
    else if (p.ready) label = "ready";
    else if (host) label = "host";
    tag.textContent = label;
    tag.classList.toggle("ready", !!p.ready || !!p.place);
    row.querySelector(".bar > i").style.width = Math.round(p.progress * 100) + "%";
    row.querySelector(".w").textContent = Math.round(p.wpm);
    row.querySelector(".a").textContent = Math.round(p.acc);
  }

  function renderRacers(st) {
    const seen = new Set();
    for (const p of st.players) {
      seen.add(p.id);
      if (!el.racers.querySelector('.racer[data-id="' + p.id + '"]')) racerRow(p);
      paintRacer(p);
    }
    for (const row of [...el.racers.children]) {
      if (!seen.has(row.dataset.id)) row.remove();
    }
  }

  function renderResults(st) {
    const timed = st.duration > 0;
    const rows = [...st.players].sort((a, b) =>
      timed ? (b.chars || 0) - (a.chars || 0) : (a.place || 99) - (b.place || 99)
    );
    const head = timed
      ? "<tr><th>#</th><th>player</th><th>stars</th><th>snippets</th><th>chars</th><th>wpm</th><th>acc</th><th>&plusmn;</th></tr>"
      : "<tr><th>#</th><th>player</th><th>stars</th><th>wpm</th><th>acc</th><th>time</th><th>&plusmn;</th></tr>";
    el.results.innerHTML =
      "<h3>results" + (timed ? " · " + durationLabel(st.duration) : "") + "</h3><table>" +
      head +
      rows
        .map((p) => {
          const delta = p.delta
            ? '<span class="' + (p.delta > 0 ? "up" : "down") + '">' +
              (p.delta > 0 ? "+" : "") + p.delta + "</span>"
            : '<span class="flat">-</span>';
          const shown = p.bot
            ? '<span class="nostars" title="bots type at a fixed accuracy">-</span>'
            : starsHtml(p.stars || 0);
          const cells = timed
            ? '<td class="stars">' + shown + "</td><td>" +
              (p.snips || 0) + "</td><td>" + (p.chars || 0) + "</td><td>" +
              Math.round(p.wpm) + "</td><td>" + Math.round(p.acc) + "%</td><td>" + delta + "</td>"
            : '<td class="stars">' + shown + "</td><td>" +
              Math.round(p.wpm) + "</td><td>" + Math.round(p.acc) + "%</td><td>" +
              (p.time != null ? p.time.toFixed(1) + "s" : "-") + "</td><td>" + delta + "</td>";
          return (
            '<tr class="' + (p.id === S.pid ? "me" : "") + (p.bot ? " bot" : "") + '"><td>' +
            (p.place || "-") + "</td><td>" + escapeHtml(p.name) +
            (p.bot ? ' <em class="botflag">bot</em>' : "") + "</td>" + cells + "</tr>"
          );
        })
        .join("") +
      "</table>";
    el.results.classList.remove("hidden");
  }

  function showSoloResult(w, a, secs) {
    el.results.innerHTML =
      "<h3>results</h3><table><tr><th>wpm</th><th>acc</th><th>time</th><th>errors</th></tr>" +
      '<tr class="me"><td>' + Math.round(w) + "</td><td>" + Math.round(a) + "%</td><td>" +
      secs.toFixed(1) + "s</td><td>" + T.errors + "</td></tr></table>";
    el.results.classList.remove("hidden");
    el.again.classList.remove("hidden");
  }

  function showTimedResult(w, a) {
    el.results.innerHTML =
      "<h3>results</h3><table>" +
      "<tr><th>snippets</th><th>chars</th><th>wpm</th><th>acc</th><th>time</th></tr>" +
      '<tr class="me"><td>' + R.snips + "</td><td>" + liveChars() + "</td><td>" +
      Math.round(w) + "</td><td>" + Math.round(a) + "%</td><td>" +
      (S.duration || Math.round(runSeconds())) + "s</td></tr></table>";
    el.results.classList.remove("hidden");
    el.again.classList.remove("hidden");
  }

  function showCountdown(n) {
    el.countdown.classList.remove("hidden");
    el.countNum.textContent = n;
    el.results.classList.add("hidden");
    el.stateBadge.textContent = "countdown";
    el.stateBadge.className = "badge countdown";
  }

  function addChat(m) {
    const div = document.createElement("div");
    if (m.sys) {
      div.className = "msg sys";
      div.textContent = m.text;
    } else {
      div.className =
        "msg" + (m.id === S.pid ? " me" : "") + (m.bot ? " bot" : "");
      div.innerHTML =
        '<span class="avatar sm"></span><span class="who"></span><span class="body"></span>';
      paintAvatar(div.querySelector(".avatar"), m);
      div.querySelector(".who").textContent = m.name + ":";
      div.querySelector(".body").textContent = m.text;
    }
    el.chatLog.appendChild(div);
    el.chatLog.scrollTop = el.chatLog.scrollHeight;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  /* ---------- bots ---------- */
  function botCard(bot, onPick, label) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "bot-card";
    card.innerHTML =
      '<span class="bot-art"></span>' +
      '<span class="avatar"></span>' +
      '<span class="bot-mid"><span class="bot-name"></span>' +
      '<span class="bot-blurb muted"></span></span>' +
      '<span class="bot-right"><b class="bot-rate"></b>' +
      '<span class="bot-rank muted"></span></span>';
    if (bot.art) {
      // the face crop, not the full card: the card art has text baked into it
      card.querySelector(".bot-art").style.backgroundImage =
        'url("/api/bot-avatar/' + bot.slug + '")';
      card.classList.add("has-art");
    }
    paintAvatar(card.querySelector(".avatar"), { bot: true, slug: bot.slug, name: bot.name });
    card.querySelector(".bot-name").textContent = bot.name;
    card.querySelector(".bot-blurb").textContent = bot.blurb;
    card.querySelector(".bot-rate").textContent = bot.rating;
    card.querySelector(".bot-rank").textContent = bot.rank + " - " + bot.wpm + " wpm";
    card.title = label || ("Challenge " + bot.name);
    if (onPick) card.onclick = () => onPick(bot);
    else card.disabled = true;
    return card;
  }

  async function loadBots() {
    try {
      const res = await fetch("/api/bots");
      const data = await res.json();
      S.bots = data.bots || [];
    } catch (err) {
      S.bots = [];
    }
    el.botList.innerHTML = "";
    for (const bot of S.bots) el.botList.appendChild(botCard(bot, challengeBot));
    el.botPanel.classList.toggle("hidden", !S.bots.length);
  }

  async function challengeBot(bot) {
    el.homeErr.textContent = "";
    const qs =
      "lang=" + encodeURIComponent(S.lang) +
      "&duration=" + (S.duration || 0) +
      "&bot=" + encodeURIComponent(bot.slug) +
      (filterQuery() ? "&" + filterQuery() : "");
    const res = await fetch("/api/lobby/new?" + qs);
    const { code } = await res.json();
    S.solo = false;
    connect(code, true);
  }

  function openBotPicker() {
    el.botPickList.innerHTML = "";
    const seated = new Set(
      (S.lobby ? S.lobby.players : []).filter((p) => p.bot).map((p) => p.slug)
    );
    for (const bot of S.bots) {
      const taken = seated.has(bot.slug);
      el.botPickList.appendChild(
        botCard(
          bot,
          taken ? null : (b) => { send({ t: "bot", v: b.slug }); closeBotPicker(); },
          taken ? "already in the lobby" : "Add " + bot.name
        )
      );
    }
    el.botModal.classList.remove("hidden");
  }

  function closeBotPicker() {
    el.botModal.classList.add("hidden");
  }

  /* ---------- rankings ---------- */
  function rankRow(i, row, isMe) {
    const line = document.createElement("div");
    line.className = "rank-row" + (isMe ? " me" : "") + (row.bot ? " bot" : "");
    line.innerHTML =
      '<span class="rk-i"></span><span class="avatar sm"></span>' +
      '<span class="rk-name"></span><span class="rk-title muted"></span>' +
      '<b class="rk-rate"></b><span class="rk-sub muted"></span>';
    line.querySelector(".rk-i").textContent = i;
    paintAvatar(line.querySelector(".avatar"), row);
    line.querySelector(".rk-name").textContent = row.name;
    line.querySelector(".rk-title").textContent = row.rank || "";
    line.querySelector(".rk-rate").textContent = row.rating;
    line.querySelector(".rk-sub").textContent = row.bot
      ? row.wpm + " wpm"
      : (row.races || 0) + " races - " + Math.round(row.best_wpm || 0) + " wpm best";
    return line;
  }

  async function loadRankings() {
    try {
      const res = await fetch("/api/rankings?limit=50", { credentials: "same-origin" });
      const data = await res.json();
      const rows = data.rows || [];
      el.ranksTable.innerHTML = "";
      rows.forEach((row, i) =>
        el.ranksTable.appendChild(rankRow(i + 1, row, data.me && data.me.id === row.id))
      );
      el.ranksCount.textContent = rows.length ? rows.length + " rated" : "";
      el.ranksEmpty.classList.toggle("hidden", rows.length > 0);

      // your own row, when you are outside the top 50
      if (data.me && !rows.some((r) => r.id === data.me.id)) {
        const mine = rankRow("you", data.me, true);
        mine.classList.add("outside");
        el.ranksTable.appendChild(mine);
      }

      // Bots are deliberately not on this board. They are opposition, not
      // players: they have a fixed rating that never moves, so listing them
      // among people pushes every real player down a board they cannot beat.
      // The roster still lives on the home page, as something to pick.

      el.ranksLadder.innerHTML = "";
      for (const tier of data.ranks || []) {
        const chip = document.createElement("span");
        chip.className = "tier";
        chip.innerHTML = '<b></b><span></span>';
        chip.querySelector("b").textContent = tier.title;
        chip.querySelector("span").textContent = tier.floor + "+";
        el.ranksLadder.appendChild(chip);
      }
    } catch (err) {
      el.ranksEmpty.classList.remove("hidden");
    }
  }

  function showRanks() {
    screenOnly(el.ranks);
    loadRankings();
    clearInterval(S.ranksTimer);
    // live board: re-read while the page is open
    S.ranksTimer = setInterval(() => {
      if (!el.ranks.classList.contains("hidden")) loadRankings();
      else clearInterval(S.ranksTimer);
    }, 15000);
  }

  function hideRanks() {
    clearInterval(S.ranksTimer);
    backToGame();
  }

  // ---------- screens ----------
  function currentName() {
    if (S.me) return S.me.name;
    const v = (el.name.value || "").trim().slice(0, 18);
    return v || "Guest" + Math.floor(Math.random() * 900 + 100);
  }

  function showHome() {
    S.room = null;
    S.solo = false;
    S.spectating = false;
    S.lobbyKey = "";
    document.body.classList.remove("spectating");
    stopRace();
    hideRun();
    el.ranks.classList.add("hidden");
    for (const id of ["screen-feed", "screen-players", "screen-user", "screen-snippets",
                     "screen-lobbies", "screen-awards"]) {
      const node = document.getElementById(id);
      if (node) node.classList.add("hidden");
    }
    if (el.ghosts) el.ghosts.innerHTML = "";
    el.home.classList.remove("hidden");
    el.room.classList.add("hidden");
    el.leave.classList.add("hidden");
    el.name.disabled = false;
    el.roomFilters.classList.add("hidden");
    el.resign.classList.add("hidden");
    const tag = el2("watchTag");
    if (tag) tag.classList.add("hidden");
    const watchers = el2("watchers");
    if (watchers) watchers.classList.add("hidden");
    if (location.pathname !== "/") history.pushState(null, "", "/");
    document.title = PAGE_TITLES["/"];
    renderFilters();
    paintBackButton();
  }

  function showRoom() {
    el.ranks.classList.add("hidden");
    for (const id of ["screen-feed", "screen-players", "screen-user", "screen-snippets",
                     "screen-lobbies", "screen-awards"]) {
      const node = document.getElementById(id);
      if (node) node.classList.add("hidden");
    }
    el.hudSnipsBox.classList.toggle("hidden", !R.timed);
    el.homeErr.textContent = "";
    el.home.classList.add("hidden");
    el.room.classList.remove("hidden");
    el.leave.classList.remove("hidden");
    el.name.disabled = true;
    // A spectator keeps the chat and the racer bars, and loses everything that
    // would change the race.
    const watching = S.spectating;
    document.querySelector(".chat").classList.toggle("hidden", S.solo);
    el.racers.classList.toggle("hidden", S.solo);
    el.ready.classList.toggle("hidden", S.solo || watching);
    el.start.classList.toggle("hidden", S.solo || watching);
    el.filterBtn.classList.toggle("hidden", S.solo || watching);
    el.newSnip.classList.toggle("hidden", S.solo || watching);
    el.addBotBtn.classList.toggle("hidden", S.solo || watching);
    el.resign.classList.add("hidden");
    el.langSelect.disabled = watching;
    document.querySelector(".room-meta").classList.toggle("hidden", S.solo);
    document.body.classList.toggle("spectating", watching);
    // the code box was display:none until a moment ago, so every offset read
    // before this point was zero
    requestAnimationFrame(remeasure);
    const tag = el2("watchTag");
    if (tag) tag.classList.toggle("hidden", !watching);
    if (watching) {
      el.codeBox.classList.add("locked");
      el.hint.textContent = "watching - you can talk in chat, but not type";
    } else {
      focusTrap();
    }
    paintBackButton();
    if (S.room && S.room !== "solo") {
      document.title = "Lobby " + S.room + " — CodeRace";
    }
  }

  /** The strip of people watching this lobby. */
  function paintWatchers(st) {
    const bar = el2("watchers");
    if (!bar) return;
    const rows = st.watchers || [];
    bar.innerHTML = "";
    bar.classList.toggle("hidden", rows.length === 0);
    if (!rows.length) return;
    const label = document.createElement("span");
    label.className = "muted";
    label.textContent = rows.length === 1 ? "1 watching:" : rows.length + " watching:";
    bar.appendChild(label);
    for (const w of rows) {
      const chip = document.createElement("span");
      chip.className = "watcher";
      chip.innerHTML = '<span class="avatar sm"></span><span class="nm"></span>';
      paintAvatar(chip.querySelector(".avatar"), w);
      chip.querySelector(".nm").textContent = w.name;
      bar.appendChild(chip);
    }
  }

  /** Stop racing but stay in the room. */
  function giveUp() {
    if (S.spectating || S.solo) return;
    if (!S.lobby || S.lobby.state !== "racing") return;
    el.resign.classList.add("hidden");
    stopRace();
    R.over = true;
    el.codeBox.classList.add("locked");
    el.hint.textContent = "you gave up - the race carries on without you";
    send({ t: "resign", replay: recTake() });
  }

  async function startSolo() {
    S.solo = true;
    S.room = "solo";
    S.soloLevel = "";  // the first draw may be any selected level
    SOLO.deck = [];
    SOLO.key = "";
    el.stateBadge.textContent = "solo";
    el.stateBadge.className = "badge racing";
    showRoom();
    await loadSoloSnippet();
  }

  /* Solo classic: a shuffled deck fetched once, then walked one at a time. */
  const SOLO = { deck: [], key: "" };

  function soloKey() {
    return [S.lang, S.levels.join("+"), S.topics.join("+"), S.soloLevel || ""].join("|");
  }

  async function soloNext() {
    const key = soloKey();
    if (key !== SOLO.key || !SOLO.deck.length) {
      // unique=1 means one pass over the whole pool: no snippet twice until
      // every other one has been seen
      const qs =
        "lang=" + encodeURIComponent(S.lang) +
        "&size=400&unique=1" +
        (S.soloLevel ? "&level=" + encodeURIComponent(S.soloLevel) : "") +
        (filterQuery() ? "&" + filterQuery() : "");
      const res = await fetch("/api/playlist?" + qs);
      const data = await res.json();
      let deck = data.playlist || [];
      // a refetched deck should not open with the snippet just played
      if (deck.length > 1 && S.lastCode && deck[0].code === S.lastCode) deck.push(deck.shift());
      SOLO.deck = deck;
      SOLO.key = key;
    }
    return SOLO.deck.shift();
  }

  async function loadSoloSnippet() {
    el.results.classList.add("hidden");
    el.again.classList.remove("hidden");

    if (S.duration > 0) {
      const qs =
        "lang=" + encodeURIComponent(S.lang) +
        "&size=40" +
        (filterQuery() ? "&" + filterQuery() : "");
      const res = await fetch("/api/playlist?" + qs);
      const data = await res.json();
      initRun(true, data.playlist || []);
      if (!R.playlist.length) {
        el.hint.textContent = "no snippet matched those filters";
        return;
      }
      el.again.textContent = "Run again";
      const first = R.playlist[0];
      S.output = first.output || "";
      paintSnipMeta(first.level, first.topic);
      renderCode(first.code, S.lang);
      armRace(performance.now() + S.duration * 1000);
      return;
    }

    const next = await soloNext();
    initRun(false, []);
    el.again.textContent = "New snippet";
    if (!next) {
      el.hint.textContent = "no snippet matched those filters";
      return;
    }
    // stay on this level from now on
    S.soloLevel = next.level;
    S.lastCode = next.code;
    S.output = next.output || "";
    paintSnipMeta(next.level, next.topic);
    renderCode(next.code, S.lang);
    armRace();
  }

  function leave() {
    if (S.ws) { S.ws.onclose = null; S.ws.close(); S.ws = null; }
    S.lobby = null;
    el.racers.innerHTML = "";
    el.chatLog.innerHTML = "";
    el.results.classList.add("hidden");
    el.countdown.classList.add("hidden");
    el.again.textContent = "Race again";
    showHome();
  }

  // ---------- setup ----------
  async function initMeta() {
    S.meta = await (await fetch("/api/meta")).json();
    S.accounts = !!S.meta.accounts;
    el.langGrid.innerHTML = "";
    el.langSelect.innerHTML = "";
    for (const l of S.meta.languages) {
      const b = document.createElement("button");
      b.type = "button";
      b.textContent = l.label;
      b.dataset.id = l.id;
      b.className = l.id === S.lang ? "on" : "";
      b.onclick = () => setLang(l.id);
      el.langGrid.appendChild(b);

      const opt = document.createElement("option");
      opt.value = l.id;
      opt.textContent = l.label;
      el.langSelect.appendChild(opt);
    }
    el.langSelect.value = S.lang;

    // the stored choice wins; otherwise take the server default from cr_config
    const stored = localStorage.getItem("cr_duration");
    S.duration = stored != null ? parseInt(stored, 10) || 0 : (S.meta.race_seconds || 0);
    if (!DURATIONS.some((d) => d.v === S.duration)) {
      DURATIONS.push({ v: S.duration, label: S.duration + "s" });
      DURATIONS.sort((a, b) => a.v - b.v);
    }

    pruneTopics();
    saveFilters();
    renderFilters();
    renderDurations();
  }

  function setLang(id) {
    S.lang = id;
    localStorage.setItem("cr_lang", id);
    for (const b of el.langGrid.children) b.classList.toggle("on", b.dataset.id === id);
    el.langSelect.value = id;
    pruneTopics();
    saveFilters();
    renderFilters();
  }

  async function createLobby() {
    el.homeErr.textContent = "";
    const qs =
      "lang=" + encodeURIComponent(S.lang) +
      "&duration=" + (S.duration || 0) +
      (filterQuery() ? "&" + filterQuery() : "");
    const res = await fetch("/api/lobby/new?" + qs);
    const { code } = await res.json();
    S.solo = false;
    connect(code, true);
  }

  function joinLobby(code) {
    el.homeErr.textContent = "";
    S.solo = false;
    S.lobbyKey = "";
    connect(code.toUpperCase(), false);
  }

  /* A missing element used to throw here and abort the rest of the wiring,
     which left the whole page dead. Warn and carry on instead - usually it
     means a cached app.js is paired with newer markup. */
  function on(node, event, handler) {
    if (!node) {
      console.warn("CodeRace: no element to bind " + event + " to");
      return;
    }
    node.addEventListener(event, handler);
  }

  el.name.value = S.name || "";
  el.name.addEventListener("change", () => localStorage.setItem("cr_name", el.name.value.trim()));

  on(el.solo, "click", startSolo);
  on(el.create, "click", createLobby);
  on(el.joinForm, "submit", (e) => {
    e.preventDefault();
    const code = el.joinCode.value.trim();
    if (code.length >= 4) joinLobby(code);
  });
  on(el.leave, "click", leave);

  on(el.profileBtn, "click", openProfile);
  on(el.profileAvatar, "click", (e) => {
    if (!S.me) return;
    e.stopPropagation();
    showUser(S.me.id);
  });
  on(el.brand, "click", (e) => {
    e.preventDefault();
    hideRanks();
    if (S.room) leave();     // drop the lobby socket on the way out
    else showHome();
  });
  on(el.pfCancel, "click", closeProfile);
  on(el.pfSave, "click", saveProfile);
  on(el.pfRemove, "click", removeAvatar);
  on(el.pfAvatar, "change", () => openCropper(el.pfAvatar.files && el.pfAvatar.files[0]));
  on(el.pfRecrop, "click", closeCropper);
  on(el.pfZoom, "input", () => {
    CROP.zoom = parseInt(el.pfZoom.value, 10) / 100;
    drawCrop();
  });

  // drag and drop, plus keyboard access on the drop zone
  ["dragenter", "dragover"].forEach((evt) =>
    el.pfDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      el.pfDrop.classList.add("over");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    el.pfDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      el.pfDrop.classList.remove("over");
    })
  );
  el.pfDrop.addEventListener("drop", (e) => {
    const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    openCropper(file);
  });
  el.pfDrop.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      el.pfAvatar.click();
    }
  });

  // drag the picture inside the crop window
  el.pfStage.addEventListener("pointerdown", (e) => {
    if (!CROP.img) return;
    CROP.drag = { x: e.clientX, y: e.clientY };
    el.pfStage.setPointerCapture(e.pointerId);
  });
  el.pfStage.addEventListener("pointermove", (e) => {
    if (!CROP.drag || !CROP.img) return;
    CROP.x += e.clientX - CROP.drag.x;
    CROP.y += e.clientY - CROP.drag.y;
    CROP.drag = { x: e.clientX, y: e.clientY };
    drawCrop();
  });
  ["pointerup", "pointercancel"].forEach((evt) =>
    el.pfStage.addEventListener(evt, () => { CROP.drag = null; })
  );

  el.pfName.addEventListener("input", () => {
    clearTimeout(nameTimer);
    nameTimer = setTimeout(checkName, 320);
  });
  on(el.modal, "click", (e) => {
    if (e.target === el.modal) closeProfile();
  });

  on(el.ranksBtn, "click", () => (el.ranks.classList.contains("hidden") ? showRanks() : hideRanks()));
  on(el.ranksBack, "click", hideRanks);
  on(el.addBotBtn, "click", openBotPicker);
  on(el.botCancel, "click", closeBotPicker);
  on(el.botModal, "click", (e) => {
    if (e.target === el.botModal) closeBotPicker();
  });

  on(el.winClose, "click", hideOutcome);
  on(el.winAgain, "click", () => {
    hideOutcome();
    if (S.solo) loadSoloSnippet();
    else send({ t: "restart" });
  });
  on(el.winModal, "click", (e) => {
    if (e.target === el.winModal) hideOutcome();
  });

  on(el.topicAll, "click", () => {
    const cat = catalogFor(S.lang);
    S.topics = cat ? Object.keys(cat.topics) : [];
    saveFilters();
    renderFilters();
  });
  on(el.topicNone, "click", () => {
    S.topics = [];
    saveFilters();
    renderFilters();
  });

  on(el.filterBtn, "click", () => {
    el.roomFilters.classList.toggle("hidden");
    if (S.lobby) renderRoomFilters(S.lobby);
  });

  on(el.chatForm, "submit", (e) => {
    e.preventDefault();
    const text = el.chatInput.value.trim();
    if (!text) return;
    send({ t: "chat", text });
    el.chatInput.value = "";
    focusTrap();
  });

  on(el.ready, "click", () => {
    const me = S.lobby && S.lobby.players.find((p) => p.id === S.pid);
    send({ t: "ready", v: !(me && me.ready) });
  });
  on(el.start, "click", () => send({ t: "start" }));
  on(el.again, "click", () => (S.solo ? loadSoloSnippet() : send({ t: "restart" })));
  on(el.newSnip, "click", () => (S.solo ? loadSoloSnippet() : send({ t: "again" })));
  on(el.langSelect, "change", () => {
    setLang(el.langSelect.value);
    if (!S.solo) send({ t: "lang", v: el.langSelect.value });
  });
  on(el.copyLink, "click", () => {
    navigator.clipboard.writeText(location.origin + "/?l=" + (S.room || ""));
    el.copyLink.classList.add("accent");
    setTimeout(() => el.copyLink.classList.remove("accent"), 600);
  });

  on(el.codeBox, "click", focusTrap);
  el.trap.addEventListener("blur", () => el.codeBox.classList.remove("focus"));
  document.addEventListener("keydown", (e) => {
    if (!el.modal.classList.contains("hidden")) return;
    if (!el.botModal.classList.contains("hidden")) return;
    if (!el.winModal.classList.contains("hidden")) return;
    if (!el.ranks.classList.contains("hidden")) return;
    if (document.activeElement === el.chatInput || document.activeElement === el.name ||
        document.activeElement === el.joinCode) return;
    onKeyDown(e);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.activeElement === el.chatInput) focusTrap();
    if (e.key === "Escape" && !el.modal.classList.contains("hidden")) closeProfile();
    if (e.key === "Escape" && !el.botModal.classList.contains("hidden")) closeBotPicker();
    if (e.key === "Escape" && !el.winModal.classList.contains("hidden")) hideOutcome();
    if (e.key === "Escape" && !el.ranks.classList.contains("hidden")) hideRanks();
  });

  /* ==================== social layer ==================== */

  const SOCIAL = {
    feedBefore: 0,
    playersTimer: 0,
    lobbiesTimer: 0,
    beatTimer: 0,
    report: null,        // {kind, id, label}
    shownChallenges: new Set(),
    viewing: 0,          // profile being looked at
    ws: null,            // notification socket
    wsRetry: 0,          // reconnect backoff, in ms
    wsTimer: 0,
    toastTimer: 0,
    incoming: [],        // invitations waiting on an answer
    outgoing: [],
  };

  function el2(id) {
    return document.getElementById(id);
  }

  function ago(stamp) {
    if (!stamp) return "";
    const then = Date.parse(stamp.replace(" ", "T") + "Z");
    if (Number.isNaN(then)) return "";
    const secs = Math.max(0, (Date.now() - then) / 1000);
    if (secs < 60) return "just now";
    if (secs < 3600) return Math.floor(secs / 60) + "m ago";
    if (secs < 86400) return Math.floor(secs / 3600) + "h ago";
    return Math.floor(secs / 86400) + "d ago";
  }

  function idleText(seconds) {
    if (seconds <= 60) return "online now";
    if (seconds <= 300) return Math.floor(seconds / 60) + "m idle";
    if (seconds > 86400 * 365) return "not seen";
    return "last seen " + ago(new Date(Date.now() - seconds * 1000).toISOString());
  }

  /* ---------- routes ----------
     One URL per screen. screenOnly() pushes it, popstate opens it, and the
     first load reads it, so a page can be linked to, refreshed, and found. */
  const PAGE_TITLES = {
    "/": "CodeRace — type real code, race your friends",
    "/lobbies": "Lobbies — CodeRace",
    "/players": "Find players — CodeRace",
    "/feed": "Race feed — CodeRace",
    "/rankings": "Rankings — CodeRace",
    "/awards": "Achievements — CodeRace",
    "/snippets": "Your snippets — CodeRace",
  };
  const SCREEN_PATHS = {
    "screen-lobbies": "/lobbies",
    "screen-players": "/players",
    "screen-feed": "/feed",
    "screen-ranks": "/rankings",
    "screen-awards": "/awards",
    "screen-snippets": "/snippets",
  };
  let ROUTING = false;  // true while popstate is driving, so nothing pushes

  function routeTo(node) {
    if (!node || ROUTING) return;
    let path = SCREEN_PATHS[node.id];
    if (node.id === "screen-user" && SOCIAL.viewing) path = "/profile/" + SOCIAL.viewing;
    if (node.id === "screen-awards" && SOCIAL.awardsFor) path = "/awards?user=" + SOCIAL.awardsFor;
    if (node.id === "screen-room" && S.room && S.room !== "solo") path = "/race/" + S.room;
    if (node.id === "screen-home") path = "/";
    if (!path) return;
    const here = location.pathname + location.search;
    if (here !== path) history.pushState(null, "", path);
    document.title =
      node.id === "screen-user" && el2("userName")
        ? (el2("userName").textContent || "Profile") + " — CodeRace"
        : PAGE_TITLES[path.split("?")[0]] || PAGE_TITLES["/"];
  }

  function openPath(path, search) {
    const q = new URLSearchParams(search || "");
    if (path.startsWith("/profile/")) {
      const id = parseInt(path.slice(9), 10);
      if (id) return showUser(id);
    }
    if (path.startsWith("/race/")) {
      const code = path.slice(6).toUpperCase();
      if (code && S.room !== code) joinLobby(code);
      return;
    }
    switch (path) {
      case "/lobbies": return showLobbies();
      case "/players": return showPlayers();
      case "/feed": return showFeed();
      case "/rankings": return showRanks();
      case "/awards": return showAwards(parseInt(q.get("user") || "0", 10) || 0);
      case "/snippets": return showSnippets();
      default: return backToGame();
    }
  }

  window.addEventListener("popstate", () => {
    ROUTING = true;
    try {
      openPath(location.pathname, location.search);
    } finally {
      ROUTING = false;
    }
  });

  function screenOnly(node) {
    for (const s of [el.home, el.room, el.ranks, el2("screen-feed"),
                     el2("screen-players"), el2("screen-user"),
                     el2("screen-snippets"), el2("screen-lobbies"),
                     el2("screen-awards")]) {
      if (s) s.classList.toggle("hidden", s !== node);
    }
    clearInterval(S.ranksTimer);
    clearInterval(SOCIAL.playersTimer);
    clearInterval(SOCIAL.lobbiesTimer);
    paintBackButton();
    routeTo(node);
    // body does not scroll - each screen is its own scroll container
    if (node && node.scrollTo) node.scrollTo(0, 0);
  }

  function backToGame() {
    screenOnly(S.room ? el.room : el.home);
  }

  /* The way back is always on screen, whichever page is open. It says where it
     goes, because "back" means the lobby mid-race and the home page otherwise. */
  function paintBackButton() {
    const btn = el2("backBtn");
    if (!btn) return;
    const onGame = isOpen("screen-home") || isOpen("screen-room");
    btn.classList.toggle("hidden", onGame);
    btn.textContent = S.room
      ? S.spectating ? "back to the race" : "back to your lobby"
      : "back to the game";
  }

  /* ---------- replay player ----------
     Plays a keystroke timeline back onto a copy of the code area. It is its
     own set of spans, so watching a replay never touches the race you might
     be in the middle of. Time is walked with requestAnimationFrame against
     the recorded clock, so 2x and 4x are exact rather than "faster". */
  const RP = {
    data: null, spans: [], lineOf: [], chars: 0,
    at: 0,           // index of the next event to apply
    ms: 0,           // playback clock, in recorded milliseconds
    speed: 1, playing: false, raf: 0, wall: 0,
    idx: 0, pos: 0, misses: 0, typed: 0,
  };

  function rpRender(idx) {
    const code = (RP.data.snippets || [])[idx] || "";
    const lang = RP.data.language || "python";
    const area = el2("rpArea");
    area.innerHTML = Prism.highlight(code, grammarFor(lang), lang);
    RP.spans = wrapChars(area);
    if (RP.spans.length !== code.length) {
      area.textContent = code;
      RP.spans = wrapChars(area);
    }
    RP.chars = code.length;
    RP.idx = idx;
    RP.pos = 0;
    // line numbers, same as the live box
    const lines = code.split("\n").length;
    const gutter = el2("rpGutter");
    gutter.innerHTML = "";
    for (let n = 1; n <= lines; n++) {
      const i = document.createElement("i");
      i.textContent = n;
      gutter.appendChild(i);
    }
    el2("rpBox").style.setProperty("--ln-w", String(lines).length + 0.5 + "ch");
    // indent guides
    let col = 0, leading = true;
    for (let i = 0; i < code.length; i++) {
      const ch = code[i];
      if (ch === "\n") { col = 0; leading = true; continue; }
      if (leading && (ch === " " || ch === "\t")) {
        if (col % INDENT === 0) RP.spans[i].classList.add("ig");
        col += ch === "\t" ? INDENT : 1;
      } else { leading = false; col++; }
    }
  }

  function rpSeekTo(ms) {
    // Rebuild from the top to the requested time. Events are a few thousand at
    // most, so replaying them from zero is cheaper than keeping an undo log.
    const ev = RP.data.events;
    RP.at = 0; RP.ms = ms; RP.misses = 0; RP.typed = 0;
    rpRender(0);
    for (const span of RP.spans) span.classList.remove("done", "bad", "cur");
    while (RP.at < ev.length && ev[RP.at][0] <= ms) {
      rpApply(ev[RP.at]);
      RP.at++;
    }
    rpPaint();
  }

  function rpApply(row) {
    const [, pos, idx, flag] = row;
    if (idx !== RP.idx) {
      rpRender(idx);
    }
    if (flag === 1) {
      RP.misses++;
      const s = RP.spans[Math.min(pos, RP.spans.length - 1)];
      if (s) s.classList.add("bad");
      return;
    }
    // correct key or backspace: the caret simply lands on `pos`
    const from = Math.min(RP.pos, pos);
    const to = Math.max(RP.pos, pos);
    for (let i = from; i < to; i++) {
      const s = RP.spans[i];
      if (!s) continue;
      if (pos > RP.pos) { s.classList.add("done"); s.classList.remove("bad"); }
      else s.classList.remove("done", "bad");
    }
    if (pos > RP.pos) RP.typed += pos - RP.pos;
    RP.pos = pos;
  }

  function rpPaint() {
    for (const s of RP.spans) s.classList.remove("cur");
    const cur = RP.spans[RP.pos];
    if (cur) {
      cur.classList.add("cur");
      const box = el2("rpBox");
      const top = cur.offsetTop;
      const view = box.clientHeight;
      if (box.scrollHeight > view) {
        box.scrollTop = Math.max(0, Math.min(box.scrollHeight - view, top - view * 0.38));
      }
    }
    const secs = RP.ms / 1000;
    const wpm = secs > 0.5 ? (RP.typed / 5) / (secs / 60) : 0;
    const acc = RP.typed + RP.misses ? (RP.typed / (RP.typed + RP.misses)) * 100 : 100;
    el2("rpWpm").textContent = Math.round(wpm);
    el2("rpAcc").textContent = Math.round(acc) + "%";
    el2("rpTime").textContent = secs.toFixed(1) + "s";
    el2("rpErrors").textContent = RP.misses;
    const total = rpTotal();
    el2("rpScrub").value = total ? Math.round((RP.ms / total) * 1000) : 0;
  }

  function rpTotal() {
    const ev = RP.data && RP.data.events;
    return ev && ev.length ? ev[ev.length - 1][0] : 0;
  }

  function rpTick(now) {
    if (!RP.playing) return;
    const dt = now - RP.wall;
    RP.wall = now;
    RP.ms += dt * RP.speed;
    const ev = RP.data.events;
    while (RP.at < ev.length && ev[RP.at][0] <= RP.ms) {
      rpApply(ev[RP.at]);
      RP.at++;
    }
    rpPaint();
    if (RP.at >= ev.length) {
      RP.ms = rpTotal();
      rpPause();
      rpPaint();
      return;
    }
    RP.raf = requestAnimationFrame(rpTick);
  }

  function rpPlay() {
    if (!RP.data) return;
    if (RP.at >= RP.data.events.length) rpSeekTo(0);
    RP.playing = true;
    RP.wall = performance.now();
    el2("rpPlay").innerHTML = "&#10074;&#10074; pause";
    RP.raf = requestAnimationFrame(rpTick);
  }

  function rpPause() {
    RP.playing = false;
    cancelAnimationFrame(RP.raf);
    el2("rpPlay").innerHTML = "&#9654; play";
  }

  async function openReplay(postId, post) {
    const modal = el2("replayModal");
    if (!modal) return;
    rpPause();
    el2("rpTitle").textContent = "Replay";
    el2("rpSub").textContent = "loading…";
    el2("rpArea").textContent = "";
    modal.classList.remove("hidden");
    try {
      const res = await fetch("/api/replay/" + postId);
      if (!res.ok) throw new Error("no replay");
      const d = await res.json();
      RP.data = d;
      RP.speed = 1;
      for (const b of el2("rpSpeed").querySelectorAll("button")) {
        b.classList.toggle("on", b.dataset.speed === "1");
      }
      el2("rpTitle").textContent = d.name + (d.kind === "solo" ? " - solo run" : " - race");
      el2("rpSub").textContent =
        Math.round(d.wpm) + " wpm · " + Math.round(d.acc) + "% · " +
        (d.language || "") + (d.place ? " · #" + d.place : "") +
        " · " + d.created_at.slice(0, 10);
      rpSeekTo(0);
      rpPlay();
    } catch (err) {
      el2("rpSub").textContent = "this run has no replay";
    }
  }

  function closeReplay() {
    rpPause();
    RP.data = null;
    el2("replayModal").classList.add("hidden");
  }

  /* ---------- posts ---------- */
  function postCard(post) {
    const card = document.createElement("article");
    card.className = "post" + (post.mine ? " mine" : "");
    card.dataset.id = post.id;

    const won = post.place === 1;
    const head = document.createElement("div");
    head.className = "post-head";
    head.innerHTML =
      '<span class="avatar sm"></span>' +
      '<button class="post-who link" type="button"></button>' +
      '<span class="rate sm"></span>' +
      '<span class="post-when muted"></span>';
    paintAvatar(head.querySelector(".avatar"), post.user);
    head.querySelector(".post-who").textContent = post.user.name;
    head.querySelector(".post-who").onclick = () => showUser(post.user.id);
    head.querySelector(".rate").textContent = post.user.rating;
    head.querySelector(".rate").title = post.user.rank;
    head.querySelector(".post-when").textContent = ago(post.created_at);

    const body = document.createElement("div");
    body.className = "post-body";
    const label = post.kind === "solo" ? "solo run" : won ? "won a race" : "raced";
    const bits = [
      '<b>' + Math.round(post.wpm) + "</b> wpm",
      Math.round(post.acc) + "% acc",
      escapeHtml(post.language || "") +
        (post.level ? " &middot; " + escapeHtml(post.level) : ""),
    ];
    if (post.place) bits.push("#" + post.place);
    if (post.delta) {
      bits.push(
        '<span class="' + (post.delta > 0 ? "up" : "down") + '">' +
          (post.delta > 0 ? "+" : "") + post.delta + "</span>"
      );
    }
    body.innerHTML =
      '<span class="post-label">' + label + "</span>" +
      '<span class="post-stats">' + bits.join(" &middot; ") + "</span>" +
      '<span class="stars">' + starsHtml(post.stars) + "</span>";
    if (post.opponents) {
      const vs = document.createElement("p");
      vs.className = "post-vs muted";
      vs.textContent = "against " + post.opponents;
      body.appendChild(vs);
    }

    const bar = document.createElement("div");
    bar.className = "post-bar";
    bar.innerHTML =
      '<button class="react up-btn" type="button">&#9650; <b></b></button>' +
      '<button class="react down-btn" type="button">&#9660; <b></b></button>' +
      '<button class="react talk-btn" type="button">comments <b></b></button>' +
      (post.replay_id
        ? '<button class="react play-btn" type="button">&#9654; replay</button>'
        : "") +
      '<span class="post-grow"></span>' +
      '<button class="react flag-btn" type="button">report</button>' +
      (post.mine ? '<button class="react del-btn" type="button">delete</button>' : "");

    const up = bar.querySelector(".up-btn");
    const down = bar.querySelector(".down-btn");
    up.querySelector("b").textContent = post.likes;
    down.querySelector("b").textContent = post.dislikes;
    bar.querySelector(".talk-btn b").textContent = post.comments;
    up.classList.toggle("on", post.my_reaction === 1);
    down.classList.toggle("on", post.my_reaction === -1);

    const talk = document.createElement("div");
    talk.className = "post-talk hidden";
    talk.innerHTML =
      '<div class="comments"></div>' +
      '<form class="comment-form">' +
      '<input maxlength="500" placeholder="say something…" />' +
      "<button type=\"submit\">post</button></form>";

    up.onclick = () => sendReaction(post, card, post.my_reaction === 1 ? 0 : 1);
    down.onclick = () => sendReaction(post, card, post.my_reaction === -1 ? 0 : -1);
    bar.querySelector(".talk-btn").onclick = () => {
      talk.classList.toggle("hidden");
      if (!talk.classList.contains("hidden")) loadComments(post.id, talk);
    };
    bar.querySelector(".flag-btn").onclick = () =>
      openReport("post", post.id, "this race post");
    const play = bar.querySelector(".play-btn");
    if (play) play.onclick = () => openReplay(post.id, post);
    const del = bar.querySelector(".del-btn");
    if (del) del.onclick = () => deletePost(post.id, card);

    talk.querySelector(".comment-form").onsubmit = (e) => {
      e.preventDefault();
      const input = talk.querySelector("input");
      const text = input.value.trim();
      if (!text) return;
      sendComment(post.id, text, talk, bar);
      input.value = "";
    };

    card.append(head, body, bar, talk);
    return card;
  }

  async function sendReaction(post, card, value) {
    if (!S.me) return;
    try {
      const res = await fetch("/api/posts/" + post.id + "/react", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ value }),
      });
      if (!res.ok) return;
      const d = await res.json();
      post.likes = d.likes;
      post.dislikes = d.dislikes;
      post.my_reaction = d.my_reaction;
      card.querySelector(".up-btn b").textContent = d.likes;
      card.querySelector(".down-btn b").textContent = d.dislikes;
      card.querySelector(".up-btn").classList.toggle("on", d.my_reaction === 1);
      card.querySelector(".down-btn").classList.toggle("on", d.my_reaction === -1);
    } catch (err) {
      /* a lost vote is not worth shouting about */
    }
  }

  function commentRow(comment) {
    const row = document.createElement("div");
    row.className = "comment";
    row.innerHTML =
      '<span class="avatar sm"></span>' +
      '<button class="comment-who link" type="button"></button>' +
      '<span class="comment-body"></span>' +
      '<span class="comment-when muted"></span>' +
      '<button class="comment-flag link" type="button">report</button>';
    paintAvatar(row.querySelector(".avatar"), comment.user);
    row.querySelector(".comment-who").textContent = comment.user.name;
    row.querySelector(".comment-who").onclick = () => showUser(comment.user.id);
    row.querySelector(".comment-body").textContent = comment.body;
    row.querySelector(".comment-when").textContent = ago(comment.created_at);
    row.querySelector(".comment-flag").onclick = () =>
      openReport("comment", comment.id, "this comment");

    if (S.me && S.me.id === comment.user.id) {
      const del = document.createElement("button");
      del.className = "comment-flag link";
      del.type = "button";
      del.textContent = "delete";
      del.onclick = async () => {
        await fetch("/api/comments/" + comment.id, {
          method: "DELETE",
          credentials: "same-origin",
        });
        row.remove();
      };
      row.appendChild(del);
    }
    return row;
  }

  function paintComments(list, rows) {
    list.innerHTML = "";
    if (!rows.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = "No comments yet.";
      list.appendChild(empty);
      return;
    }
    for (const comment of rows) list.appendChild(commentRow(comment));
  }

  async function loadComments(postId, talk) {
    const list = talk.querySelector(".comments");
    list.innerHTML = '<p class="muted">loading…</p>';
    try {
      const res = await fetch("/api/posts/" + postId + "/comments");
      const d = await res.json();
      paintComments(list, d.comments || []);
    } catch (err) {
      list.innerHTML = '<p class="err">could not load the comments</p>';
    }
  }

  async function sendComment(postId, text, talk, bar) {
    try {
      const res = await fetch("/api/posts/" + postId + "/comments", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ body: text }),
      });
      const d = await res.json();
      if (!res.ok) {
        const list = talk.querySelector(".comments");
        list.innerHTML =
          '<p class="err">' +
          (d.error === "rate_limited"
            ? "too many comments this hour, give it a rest"
            : d.error === "not_registered"
            ? "you need a profile to comment"
            : "could not post that") +
          "</p>";
        return;
      }
      paintComments(talk.querySelector(".comments"), d.comments || []);
      bar.querySelector(".talk-btn b").textContent = (d.comments || []).length;
    } catch (err) {
      /* ignore */
    }
  }

  async function deletePost(postId, card) {
    try {
      const res = await fetch("/api/posts/" + postId, {
        method: "DELETE",
        credentials: "same-origin",
      });
      if (res.ok) card.remove();
    } catch (err) {
      /* ignore */
    }
  }

  /* ---------- feed ---------- */
  async function loadFeed(append) {
    const list = el2("feedList");
    const more = el2("feedMore");
    if (!append) {
      SOCIAL.feedBefore = 0;
      list.innerHTML = '<p class="muted">loading…</p>';
    }
    try {
      const qs = SOCIAL.feedBefore ? "?before=" + SOCIAL.feedBefore : "";
      const res = await fetch("/api/feed" + qs, { credentials: "same-origin" });
      const d = await res.json();
      const posts = d.posts || [];
      if (!append) list.innerHTML = "";
      for (const post of posts) list.appendChild(postCard(post));
      if (posts.length) SOCIAL.feedBefore = posts[posts.length - 1].id;
      el2("feedEmpty").classList.toggle("hidden", list.children.length > 0);
      more.classList.toggle("hidden", posts.length < 30);
    } catch (err) {
      list.innerHTML = '<p class="err">could not load the feed</p>';
    }
  }

  function showFeed() {
    screenOnly(el2("screen-feed"));
    loadFeed(false);
  }

  /* ---------- public profile ---------- */
  async function showUser(userId) {
    SOCIAL.viewing = userId;
    screenOnly(el2("screen-user"));
    el2("userName").textContent = "";
    el2("userPosts").innerHTML = '<p class="muted">loading…</p>';

    try {
      const res = await fetch("/api/profile/" + userId, { credentials: "same-origin" });
      if (!res.ok) {
        el2("userPosts").innerHTML = '<p class="err">no such player</p>';
        return;
      }
      const d = await res.json();
      const p = d.profile;

      el2("userTitle").textContent = d.me ? "Your profile" : "Profile";
      el2("userName").textContent = p.name;
      document.title = p.name + " — " + p.rank + " — CodeRace";
      const badge = el2("userRankBadge");
      badge.textContent = p.rank;
      badge.className = "rank-badge tier-" + rankTier(p.rating);
      el2("userRating").textContent = p.rating;
      paintBadges(p);
      paintProfileAwards(p, userId);
      el2("userAwards").onclick = () => showAwards(userId);
      el2("userSeen").textContent =
        (p.online ? "online now" : idleText(p.idle)) +
        (p.joined ? " · joined " + p.joined.slice(0, 10) : "");
      paintAvatar(el2("userAvatar"), p);
      const cover = el2("userCover");
      if (cover) {
        // The version in the URL is what makes a new upload show up instead of
        // the browser handing back the one it already has.
        cover.classList.toggle("hidden", !p.cover);
        cover.style.backgroundImage = p.cover
          ? 'url("/api/cover/' + userId + "?v=" + p.cover + '")'
          : "";
      }

      // Headline records. best_wpm is a decimal, and rounding a personal best
      // down to a whole number loses the thing that makes it a record.
      el2("recWpm").textContent = (Number(p.best_wpm) || 0).toFixed(2);
      el2("recWon").textContent = (p.wins || 0).toLocaleString();
      el2("recPlayed").textContent = (p.races || 0).toLocaleString();
      paintDetails(p);

      const stats = [
        ["races", p.races],
        ["wins", p.wins],
        ["best wpm", Math.round(p.best_wpm)],
        ["avg wpm", Math.round(p.avg_wpm)],
        ["avg acc", Math.round(p.avg_acc) + "%"],
        ["stars", p.stars],
        ["snippets", p.snippets],
      ];
      el2("userStats").innerHTML = stats
        .map((s) => "<div><b>" + s[1] + "</b><span>" + s[0] + "</span></div>")
        .join("");

      el2("userLangs").innerHTML = (p.by_language || [])
        .map(
          (row) =>
            '<span class="chip"><span class="chip-label">' +
            escapeHtml(row.language) +
            '</span><span class="chip-n">' +
            row.races +
            "</span></span>"
        )
        .join("");

      const canAct = !!S.me && !d.me;
      el2("userChallenge").classList.toggle("hidden", !canAct);
      el2("userReport").classList.toggle("hidden", !canAct);
      el2("userChallenge").onclick = () => challengePlayer(userId, p.name);
      el2("userReport").onclick = () => openReport("user", userId, p.name);

      const posts = el2("userPosts");
      posts.innerHTML = "";
      for (const post of d.posts || []) posts.appendChild(postCard(post));
      el2("userNoPosts").classList.toggle("hidden", (d.posts || []).length > 0);
    } catch (err) {
      el2("userPosts").innerHTML = '<p class="err">could not load that profile</p>';
    }
  }

  /** Which badge colour a rating earns. Mirrors the ladder in rating.py. */
  function rankTier(score) {
    const n = Number(score) || 0;
    if (n >= 2100) return "legend";
    if (n >= 1650) return "gold";
    if (n >= 1350) return "silver";
    return "bronze";
  }

  /**
   * Country, age and gender - whichever of them this player filled in. A field
   * they left blank is left out entirely rather than shown as "unknown", so an
   * empty row never reads as something withheld.
   */
  function paintDetails(p) {
    const box = el2("userDetails");
    if (!box) return;
    const rows = [];
    if (p.country) rows.push(["Country", countryName(p.country), p.country]);
    if (p.age != null) rows.push(["Age", String(p.age)]);
    if (p.gender) rows.push(["Gender", GENDER_LABELS[p.gender] || p.gender]);

    box.innerHTML = "";
    box.classList.toggle("hidden", rows.length === 0);
    for (const [label, value, code] of rows) {
      const item = document.createElement("div");
      item.className = "detail";
      item.innerHTML = "<span></span><b></b>";
      item.querySelector("span").textContent = label;
      const body = item.querySelector("b");
      if (code) body.appendChild(flagNode(code, 14));
      body.appendChild(document.createTextNode(value));
      box.appendChild(item);
    }
  }

  /* ---------- achievements ---------- */
  const TIER_ORDER = { legend: 0, gold: 1, silver: 2, bronze: 3 };

  function awardCard(a) {
    const card = document.createElement("div");
    card.className =
      "award tier-" + (a.tier || "bronze") + (a.earned ? " got" : " locked");
    card.innerHTML =
      '<span class="award-icon"></span>' +
      '<span class="award-body">' +
      '<b class="award-name"></b>' +
      '<span class="award-blurb muted"></span>' +
      '<span class="award-meta muted"></span>' +
      '<span class="award-track hidden"><i></i></span>' +
      "</span>";

    card.querySelector(".award-icon").textContent = a.icon || "\u2b50";
    card.querySelector(".award-name").textContent = a.name;
    card.querySelector(".award-blurb").textContent = a.blurb;

    // Rarity is the point of the page, so it leads on both halves.
    const share =
      a.share != null
        ? a.share.toFixed(1).replace(/\.0$/, "") + "% of players"
        : a.holders != null
        ? a.holders + (a.holders === 1 ? " player has this" : " players have this")
        : "";
    const meta = card.querySelector(".award-meta");
    meta.textContent = a.earned
      ? share + (a.earned_at ? " \u00b7 earned " + String(a.earned_at).slice(0, 10) : "")
      : share;

    // Only a countable achievement has a bar; a one-off has nothing to show.
    if (!a.earned && a.want) {
      const track = card.querySelector(".award-track");
      track.classList.remove("hidden");
      const pct = Math.max(0, Math.min(100, (a.have / a.want) * 100));
      track.querySelector("i").style.width = pct + "%";
      track.title = a.have + " of " + a.want;
      meta.textContent = (share ? share + " \u00b7 " : "") + a.have + " / " + a.want;
    }
    return card;
  }

  function sortAwards(rows) {
    return rows.slice().sort((a, b) => {
      const t = (TIER_ORDER[a.tier] ?? 9) - (TIER_ORDER[b.tier] ?? 9);
      return t || (a.share || 0) - (b.share || 0);
    });
  }

  async function loadAwards(userId) {
    const got = el2("awardsGot");
    const left = el2("awardsLeft");
    if (!got || !left) return;
    got.innerHTML = '<p class="muted">loading…</p>';
    left.innerHTML = "";
    try {
      const qs = userId ? "?user=" + userId : "";
      const res = await fetch("/api/achievements" + qs, { credentials: "same-origin" });
      const d = await res.json();
      const rows = d.achievements || [];
      const earned = sortAwards(rows.filter((a) => a.earned));
      const locked = sortAwards(rows.filter((a) => !a.earned));

      got.innerHTML = "";
      for (const a of earned) got.appendChild(awardCard(a));
      left.innerHTML = "";
      for (const a of locked) left.appendChild(awardCard(a));

      el2("awardsEarned").textContent = d.earned || 0;
      el2("awardsTotal").textContent = d.total || 0;
      el2("awardsGotCount").textContent = earned.length ? earned.length + "" : "";
      el2("awardsLeftCount").textContent = locked.length ? locked.length + "" : "";
      el2("awardsNone").classList.toggle("hidden", earned.length > 0);
      const pct = d.total ? (d.earned / d.total) * 100 : 0;
      el2("awardsBar").style.width = pct + "%";
      el2("awardsTitle").textContent =
        d.me || !userId ? "Your achievements" : "Achievements";
      el2("awardsSub").textContent = d.players
        ? "Everything there is to earn. The percentage is how many of the " +
          d.players + " players who have raced hold it."
        : "Everything there is to earn.";
    } catch (err) {
      got.innerHTML = '<p class="err">could not load achievements</p>';
    }
  }

  function showAwards(userId) {
    SOCIAL.awardsFor = userId || 0;
    screenOnly(el2("screen-awards"));
    loadAwards(userId || 0);
  }

  /**
   * The achievements this player holds, on their own profile rather than a
   * click away. Earned cards only - the full catalogue, with what is still to
   * get, is one button along.
   */
  function paintProfileAwards(p, userId) {
    const grid = el2("userAwardsGrid");
    if (!grid) return;
    const rows = p.awards || [];
    grid.innerHTML = "";
    for (const a of rows) {
      // Already earned by definition, so every card here is a lit one.
      grid.appendChild(awardCard({ ...a, earned: true }));
    }
    el2("userAwardsNone").classList.toggle("hidden", rows.length > 0);
    el2("userAwardsCount").textContent = p.awards_total
      ? rows.length + " of " + p.awards_total
      : String(rows.length);
    el2("userAwardsAll").onclick = () => showAwards(userId);
  }

  /** The badge row under a name on a profile. */
  function paintBadges(p) {
    const box = el2("userBadges");
    if (!box) return;
    const rows = p.awards || [];
    box.innerHTML = "";
    box.classList.toggle("hidden", rows.length === 0);
    for (const a of rows.slice(0, 12)) {
      const chip = document.createElement("span");
      chip.className = "badge-chip tier-" + (a.tier || "bronze");
      chip.innerHTML = '<i></i><span></span>';
      chip.querySelector("i").textContent = a.icon || "\u2b50";
      chip.querySelector("span").textContent = a.name;
      chip.title =
        a.blurb + (a.earned_at ? " · earned " + String(a.earned_at).slice(0, 10) : "");
      box.appendChild(chip);
    }
    if (rows.length > 12) {
      const more = document.createElement("span");
      more.className = "badge-chip more";
      more.textContent = "+" + (rows.length - 12);
      box.appendChild(more);
    }
  }

  /* ---------- find players ---------- */
  function playerRow(p) {
    const row = document.createElement("div");
    row.className = "rank-row" + (p.me ? " me" : "");
    row.innerHTML =
      '<span class="dotc"></span><span class="avatar sm"></span>' +
      '<button class="rk-name link" type="button"></button>' +
      '<span class="rk-title muted"></span>' +
      '<b class="rk-rate"></b>' +
      '<span class="rk-act"></span>';
    paintAvatar(row.querySelector(".avatar"), p);
    row.querySelector(".dotc").style.background = p.online
      ? "var(--accent)"
      : "var(--dim)";
    row.querySelector(".dotc").title = p.online ? "online" : idleText(p.idle);
    const name = row.querySelector(".rk-name");
    name.textContent = p.name;
    name.onclick = () => showUser(p.id);
    row.querySelector(".rk-title").textContent =
      p.rank + (p.racing ? " · in a race" : p.online ? "" : " · " + idleText(p.idle));
    row.querySelector(".rk-rate").textContent = p.rating;

    const act = row.querySelector(".rk-act");
    if (!p.me && p.watch) {
      // Mid-race: watching is the only thing you can usefully do with them.
      const eye = document.createElement("button");
      eye.type = "button";
      eye.className = "primary";
      eye.textContent = "Spectate";
      eye.onclick = () => spectate(p.watch);
      act.appendChild(eye);
    }
    if (!p.me && S.me) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ghost";
      btn.textContent = "Challenge";
      btn.onclick = () => challengePlayer(p.id, p.name, btn);
      act.appendChild(btn);
    }
    return row;
  }

  async function loadPlayers() {
    const list = el2("playersList");
    try {
      const res = await fetch("/api/players", { credentials: "same-origin" });
      const d = await res.json();
      const rows = (d.players || []).filter((p) => p.online || p.races > 0);
      list.innerHTML = "";
      for (const p of rows) list.appendChild(playerRow(p));
      el2("playersCount").textContent =
        rows.filter((p) => p.online).length + " online";
      el2("playersEmpty").classList.toggle("hidden", rows.length > 0);
    } catch (err) {
      list.innerHTML = '<p class="err">could not load the player list</p>';
    }
    loadChallenges();
  }

  function showPlayers() {
    screenOnly(el2("screen-players"));
    fillSelect(el2("chLang"), (S.meta && S.meta.catalog) || [], S.lang);
    loadPlayers();
    clearInterval(SOCIAL.playersTimer);
    // The notification socket pushes a "presence" event on every join and
    // leave, so this is only a safety net for a tab whose socket is down.
    SOCIAL.playersTimer = setInterval(() => {
      if (isOpen("screen-players")) loadPlayers();
      else clearInterval(SOCIAL.playersTimer);
    }, 30000);
  }

  /* ---------- lobby browser ---------- */
  function lobbyRow(r) {
    const row = document.createElement("div");
    row.className = "lobby-row" + (r.locked ? " locked" : "");
    row.innerHTML =
      '<span class="lb-code"></span>' +
      '<span class="lb-main"><b class="lb-title"></b><span class="lb-sub muted"></span></span>' +
      '<span class="badge lb-state"></span>' +
      '<span class="lb-people muted"></span>' +
      '<span class="lb-act"></span>';

    row.querySelector(".lb-code").textContent = r.locked ? "\u{1f512}" : r.code;
    row.querySelector(".lb-title").textContent =
      r.title || (r.host ? r.host + "'s lobby" : "open lobby");

    const mode = r.duration ? r.duration + "s run" : "one snippet";
    const bits = [r.language, mode];
    if (r.strict) bits.push("strict");
    if (r.suggest) bits.push("suggestions");
    if (r.ranked === false) bits.push("unranked");
    if (r.levels && r.levels.length) bits.push(r.levels.join("/"));
    if (r.topics && r.topics.length) bits.push(r.topics.join("/"));
    row.querySelector(".lb-sub").textContent = bits.join(" \u00b7 ");

    const state = row.querySelector(".lb-state");
    state.textContent = r.state;
    state.className = "badge lb-state " + r.state;

    const people = [
      r.limit
        ? r.humans + "/" + r.limit + " players"
        : r.humans + (r.humans === 1 ? " player" : " players"),
    ];
    if (r.bots) people.push(r.bots + " bot" + (r.bots === 1 ? "" : "s"));
    if (r.watchers) people.push(r.watchers + " watching");
    const who = row.querySelector(".lb-people");
    who.textContent = people.join(" \u00b7 ");
    who.title = (r.names || []).join(", ");

    const act = row.querySelector(".lb-act");
    const join = document.createElement("button");
    join.type = "button";
    join.className = "accent";
    join.textContent = r.locked ? "Enter key" : "Join";
    join.onclick = () => joinListed(r);
    act.appendChild(join);

    if (!r.locked) {
      const eye = document.createElement("button");
      eye.type = "button";
      eye.className = "ghost";
      eye.textContent = "Spectate";
      eye.onclick = () => spectate(r.code);
      act.appendChild(eye);
    }
    return row;
  }

  function joinListed(r) {
    if (!r.locked) {
      joinLobby(r.code);
      return;
    }
    openKeyPrompt(r);
  }

  function openKeyPrompt(r) {
    const modal = el2("keyModal");
    if (!modal) return;
    el2("keyTitle").textContent = "Lobby " + r.code + " is private";
    el2("keyInput").value = "";
    el2("keyErr").textContent = "";
    modal.dataset.code = r.code;
    modal.classList.remove("hidden");
    el2("keyInput").focus();
  }

  function closeKeyPrompt() {
    const modal = el2("keyModal");
    if (modal) modal.classList.add("hidden");
  }

  async function submitKey() {
    const modal = el2("keyModal");
    if (!modal) return;
    const code = modal.dataset.code || "";
    const key = el2("keyInput").value.trim();
    const err = el2("keyErr");
    err.textContent = "";
    if (!key) {
      err.textContent = "the key is required";
      return;
    }
    try {
      const res = await fetch("/api/lobby/" + encodeURIComponent(code) + "/key", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ key }),
      });
      if (!res.ok) {
        err.textContent = res.status === 404 ? "that lobby has closed" : "wrong key";
        return;
      }
    } catch (e) {
      err.textContent = "network error";
      return;
    }
    closeKeyPrompt();
    S.solo = false;
    S.lobbyKey = key;
    connect(code, false);
  }

  async function loadLobbies() {
    const list = el2("lobbyList");
    if (!list) return;
    try {
      const res = await fetch("/api/lobbies");
      const d = await res.json();
      const rows = d.lobbies || [];
      list.innerHTML = "";
      for (const r of rows) list.appendChild(lobbyRow(r));
      el2("lobbyCount").textContent =
        rows.length + (rows.length === 1 ? " lobby open" : " lobbies open");
      el2("lobbyEmpty").classList.toggle("hidden", rows.length > 0);
    } catch (err) {
      list.innerHTML = '<p class="err">could not load the lobby list</p>';
    }
  }

  function showLobbies() {
    screenOnly(el2("screen-lobbies"));
    fillSelect(el2("newLang"), (S.meta && S.meta.catalog) || [], S.lang);
    loadLobbies();
    clearInterval(SOCIAL.lobbiesTimer);
    SOCIAL.lobbiesTimer = setInterval(() => {
      if (isOpen("screen-lobbies")) loadLobbies();
      else clearInterval(SOCIAL.lobbiesTimer);
    }, 30000);
  }

  /** Open a room from the browser's create panel. */
  async function createListedLobby() {
    const btn = el2("newLobbyGo");
    const err = el2("newLobbyErr");
    err.textContent = "";
    const priv = el2("newPrivate").checked;
    const key = el2("newKey").value.trim();
    if (priv && key.length && key.length < 3) {
      err.textContent = "a key needs at least three characters";
      return;
    }
    btn.disabled = true;
    try {
      const qs = new URLSearchParams({
        lang: el2("newLang").value || S.lang,
        levels: S.levels.join(","),
        topics: S.topics.join(","),
        duration: String(parseInt(el2("newDuration").value || "0", 10)),
        private: priv ? "1" : "0",
        key: priv ? key : "",
        title: el2("newTitle").value.trim().slice(0, 40),
        strict: el2("newStrict").checked ? "1" : "0",
        suggest: el2("newSuggest").checked ? "1" : "0",
        ranked: el2("newRanked").checked ? "1" : "0",
        limit: el2("newLimit").value || "0",
      });
      const res = await fetch("/api/lobby/new?" + qs);
      const d = await res.json();
      S.solo = false;
      S.lobbyKey = priv ? key : "";
      connect(d.code, false);
    } catch (e) {
      err.textContent = "could not open a lobby";
    } finally {
      btn.disabled = false;
    }
  }

  /* ---------- spectating ---------- */
  function spectate(code) {
    if (!code) return;
    S.solo = false;
    S.spectating = true;
    connect(code, false, { spectate: true });
  }

  /* ---------- challenges ---------- */
  async function challengePlayer(userId, name, btn) {
    if (!S.me) return;
    if (btn) {
      btn.disabled = true;
      btn.textContent = "inviting…";
    }
    try {
      const res = await fetch("/api/challenge", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          to: userId,
          lang: (el2("chLang") && el2("chLang").value) || S.lang,
          levels: S.levels.join(","),
          topics: S.topics.join(","),
          duration: parseInt((el2("chDuration") && el2("chDuration").value) || "0", 10),
        }),
      });
      const d = await res.json();
      if (!res.ok) {
        if (btn) {
          btn.disabled = false;
          btn.textContent = "Challenge";
        }
        return;
      }
      if (btn) btn.textContent = "waiting…";
      // the challenger waits in the lobby they just opened
      S.solo = false;
      S.lobbyKey = "";
      connect(d.code, true);
    } catch (err) {
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Challenge";
      }
    }
  }

  function challengeRow(c, incoming) {
    const row = document.createElement("div");
    row.className = "ch-row";
    row.innerHTML =
      '<span class="avatar sm"></span>' +
      '<span class="ch-text"></span>' +
      '<span class="post-grow"></span>' +
      '<span class="ch-act"></span>';
    paintAvatar(row.querySelector(".avatar"), c.other);
    const when = c.duration ? c.duration + "s" : "one snippet";
    row.querySelector(".ch-text").textContent =
      (incoming ? c.other.name + " challenged you" : "waiting for " + c.other.name) +
      " · " + (c.language || "python") + " · " + when;

    const act = row.querySelector(".ch-act");
    if (incoming) {
      const yes = document.createElement("button");
      yes.className = "accent";
      yes.type = "button";
      yes.textContent = "Accept";
      yes.onclick = () => answerChallenge(c, "accept");
      const no = document.createElement("button");
      no.className = "ghost";
      no.type = "button";
      no.textContent = "Decline";
      no.onclick = () => answerChallenge(c, "decline");
      act.append(yes, no);
    } else {
      const tag = document.createElement("span");
      tag.className = "muted";
      tag.textContent = c.status === "accepted" ? "in the lobby" : "waiting";
      const drop = document.createElement("button");
      drop.className = "ghost";
      drop.type = "button";
      drop.textContent = "Cancel";
      drop.onclick = () => cancelChallenge(c);
      act.append(tag, drop);
    }
    return row;
  }

  async function answerChallenge(c, action) {
    dismissToast();
    try {
      const res = await fetch("/api/challenges/" + c.id + "/" + action, {
        method: "POST",
        credentials: "same-origin",
      });
      const d = await res.json();
      if (!res.ok) {
        if (action === "accept") alertLine("that invitation is no longer open");
        loadChallenges();
        return;
      }
      if (action === "accept") {
        S.solo = false;
        connect(d.lobby, false);
      }
    } catch (err) {
      /* the socket resends the list on reconnect */
    }
  }

  async function cancelChallenge(c) {
    try {
      await fetch("/api/challenges/" + c.id + "/cancel", {
        method: "POST",
        credentials: "same-origin",
      });
    } catch (err) {
      /* ignore */
    }
    loadChallenges();
  }

  function alertLine(text) {
    el.homeErr.textContent = text;
  }

  async function loadChallenges() {
    if (!S.me) return;
    try {
      const res = await fetch("/api/challenges", { credentials: "same-origin" });
      paintChallenges(await res.json());
    } catch (err) {
      /* ignore */
    }
  }

  function paintChallenges(d) {
    const incoming = d.incoming || [];
    const outgoing = d.outgoing || [];
    SOCIAL.incoming = incoming;
    SOCIAL.outgoing = outgoing;

    const panel = el2("chPanel");
    const list = el2("chList");
    if (panel && list) {
      list.innerHTML = "";
      for (const c of incoming) list.appendChild(challengeRow(c, true));
      for (const c of outgoing) list.appendChild(challengeRow(c, false));
      panel.classList.toggle("hidden", incoming.length + outgoing.length === 0);
      const count = el2("chCount");
      if (count) {
        count.textContent = incoming.length
          ? incoming.length + " waiting on you"
          : outgoing.length
          ? "waiting on them"
          : "";
      }
    }

    // The badge counts only what you can act on. It used to print a bare "0"
    // whenever the list emptied, because the text was written before the
    // element was hidden.
    const badge = el2("chBadge");
    if (badge) {
      const n = incoming.length;
      badge.textContent = n > 9 ? "9+" : String(n);
      badge.classList.toggle("hidden", n === 0);
      badge.title = n ? n + " invitation(s) waiting" : "";
    }

    // Forget toasts for invitations that are gone, so a re-invite pops again.
    const live = new Set(incoming.map((c) => c.id));
    for (const id of [...SOCIAL.shownChallenges]) {
      if (!live.has(id)) SOCIAL.shownChallenges.delete(id);
    }
    const toast = el2("chToast");
    if (toast && toast.dataset.id && !live.has(Number(toast.dataset.id))) {
      dismissToast();
    }
    for (const c of incoming) {
      if (SOCIAL.shownChallenges.has(c.id)) continue;
      SOCIAL.shownChallenges.add(c.id);
      showChallengeToast(c);
      break;
    }
  }

  function showChallengeToast(c) {
    const toast = el2("chToast");
    if (!toast) return;
    clearTimeout(SOCIAL.toastTimer);
    toast.dataset.id = c.id;
    paintAvatar(el2("chToastAvatar"), c.other);
    const when = c.duration ? c.duration + "s" : "one snippet";
    el2("chToastText").textContent =
      c.other.name + " (" + c.other.rating + ") challenged you";
    const sub = el2("chToastSub");
    if (sub) sub.textContent = (c.language || "python") + " \u00b7 " + when;
    el2("chToastAccept").onclick = () => answerChallenge(c, "accept");
    el2("chToastDecline").onclick = () => answerChallenge(c, "decline");
    toast.classList.remove("hidden");
    ding();
    // The invitation expires server-side; drop the card well before that, so a
    // stale one is never left sitting there to be clicked.
    SOCIAL.toastTimer = setTimeout(dismissToast, 45000);
  }

  function dismissToast() {
    const toast = el2("chToast");
    if (!toast) return;
    clearTimeout(SOCIAL.toastTimer);
    toast.dataset.id = "";
    toast.classList.add("hidden");
  }

  /* A short blip on an invitation. Synthesised rather than loaded, and silent
     until the page has been interacted with, which is what browsers require. */
  function ding() {
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      const ctx = new Ctx();
      if (ctx.state !== "running") {
        ctx.close();
        return;
      }
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.setValueAtTime(1180, ctx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.06, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.25);
      osc.connect(gain).connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.26);
      setTimeout(() => ctx.close(), 400);
    } catch (err) {
      /* audio is a nicety, never a requirement */
    }
  }

  /* ---------- notification socket ----------
     One socket per tab, held open for as long as the account is known. It
     carries invitations, presence and lobby-list changes, so none of those
     screens poll any more: an invitation lands the moment it is sent, and the
     socket closing is what marks the player offline. */
  function userSocket() {
    if (!S.me) return;
    if (
      SOCIAL.ws &&
      (SOCIAL.ws.readyState === WebSocket.OPEN ||
        SOCIAL.ws.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    let ws;
    try {
      ws = new WebSocket(proto + "//" + location.host + "/ws/user");
    } catch (err) {
      scheduleUserSocket();
      return;
    }
    SOCIAL.ws = ws;
    ws.onopen = () => {
      SOCIAL.wsRetry = 0;
      setLive(true);
    };
    ws.onmessage = (ev) => {
      let m;
      try {
        m = JSON.parse(ev.data);
      } catch (err) {
        return;
      }
      handleUser(m);
    };
    ws.onclose = () => {
      SOCIAL.ws = null;
      setLive(false);
      scheduleUserSocket();
    };
    ws.onerror = () => {};
  }

  function scheduleUserSocket() {
    if (!S.me) return;
    clearTimeout(SOCIAL.wsTimer);
    // back off to 15s, so a server restart does not become a retry storm
    SOCIAL.wsRetry = Math.min(15000, (SOCIAL.wsRetry || 500) * 2);
    SOCIAL.wsTimer = setTimeout(userSocket, SOCIAL.wsRetry);
  }

  function setLive(on) {
    for (const node of document.querySelectorAll(".live")) {
      node.classList.toggle("off", !on);
      node.textContent = on ? "live" : "reconnecting";
    }
  }

  function handleUser(m) {
    switch (m.t) {
      case "challenges":
        paintChallenges(m);
        break;
      case "challenge_accepted":
        // the other player said yes: walk into the lobby that was opened
        dismissToast();
        if (S.room !== m.code) {
          S.solo = false;
          connect(m.code, false);
        }
        flashNote(m.by + " accepted");
        break;
      case "challenge_declined":
        flashNote(m.by + " declined your challenge");
        break;
      case "challenge_cancelled":
        dismissToast();
        break;
      case "presence":
        if (isOpen("screen-players")) loadPlayers();
        break;
      case "lobbies":
        if (isOpen("screen-lobbies")) loadLobbies();
        if (isOpen("screen-players")) loadPlayers();
        break;
      case "ping":
        if (SOCIAL.ws && SOCIAL.ws.readyState === WebSocket.OPEN) {
          SOCIAL.ws.send(JSON.stringify({ t: "pong" }));
        }
        break;
    }
  }

  function isOpen(id) {
    const node = el2(id);
    return !!node && !node.classList.contains("hidden");
  }

  /* A one-line notice that does not warrant a dialog. */
  function flashNote(text) {
    const node = el2("flashNote");
    if (!node) return;
    node.textContent = text;
    node.classList.remove("hidden");
    clearTimeout(SOCIAL.noteTimer);
    SOCIAL.noteTimer = setTimeout(() => node.classList.add("hidden"), 4500);
  }

  /* The socket is what keeps the account online. This stays as a fallback for
     a browser or proxy that will not hold a websocket open. */
  function startHeartbeat() {
    userSocket();
    clearInterval(SOCIAL.beatTimer);
    SOCIAL.beatTimer = setInterval(async () => {
      if (!S.me) return;
      if (SOCIAL.ws && SOCIAL.ws.readyState === WebSocket.OPEN) return;
      try {
        const res = await fetch("/api/heartbeat", {
          method: "POST",
          credentials: "same-origin",
        });
        const d = await res.json();
        if (d.challenges) paintChallenges(d.challenges);
      } catch (err) {
        /* ignore */
      }
    }, 20000);
  }

  /* ---------- reports ---------- */
  function openReport(kind, id, label) {
    if (!S.me) return;
    SOCIAL.report = { kind, id, label };
    el2("reportTitle").textContent = "Report " + label;
    el2("reportNote").value = "";
    el2("reportErr").textContent = "";
    el2("reportModal").classList.remove("hidden");
  }

  function closeReport() {
    el2("reportModal").classList.add("hidden");
    SOCIAL.report = null;
  }

  async function sendReport() {
    if (!SOCIAL.report) return;
    const btn = el2("reportSend");
    btn.disabled = true;
    try {
      const res = await fetch("/api/report", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          kind: SOCIAL.report.kind,
          id: SOCIAL.report.id,
          reason: el2("reportReason").value,
          note: el2("reportNote").value,
        }),
      });
      const d = await res.json();
      if (!res.ok) {
        el2("reportErr").textContent = d.error || "could not send that";
        return;
      }
      closeReport();
      alertLine(
        d.hidden
          ? "reported — that has now been hidden"
          : "reported (" + d.reports + " of " + d.threshold + ")"
      );
    } catch (err) {
      el2("reportErr").textContent = "network error";
    } finally {
      btn.disabled = false;
    }
  }

  /* ---------- my snippets ---------- */
  function fillSelect(node, rows, value) {
    node.innerHTML = "";
    for (const row of rows) {
      const opt = document.createElement("option");
      opt.value = row.id;
      opt.textContent = row.label + (row.custom ? " (yours)" : "");
      node.appendChild(opt);
    }
    if (value) node.value = value;
  }

  function showSnippets() {
    screenOnly(el2("screen-snippets"));
    if (S.meta) {
      fillSelect(el2("snipLang"), S.meta.languages, S.lang);
      fillSelect(el2("snipLevel"), S.meta.levels, "easy");
      fillSelect(el2("snipTopic"), S.meta.topics, "algorithms");
    }
    loadMySnippets();
  }

  async function loadMySnippets() {
    const list = el2("snipList");
    if (!S.me) {
      list.innerHTML = '<p class="muted">you need a profile first</p>';
      return;
    }
    list.innerHTML = '<p class="muted">loading…</p>';
    try {
      const res = await fetch("/api/snippets/mine", { credentials: "same-origin" });
      const d = await res.json();
      const rows = d.snippets || [];
      list.innerHTML = "";
      for (const row of rows) list.appendChild(snippetRow(row));
      el2("snipCount").textContent = rows.length ? rows.length + " added" : "";
      el2("snipEmpty").classList.toggle("hidden", rows.length > 0);
      el2("snipQuota").textContent = "Up to " + d.per_day + " a day.";
    } catch (err) {
      list.innerHTML = '<p class="err">could not load your snippets</p>';
    }
  }

  function snippetRow(row) {
    const card = document.createElement("div");
    card.className = "snip-card" + (row.active ? "" : " hidden-snip");
    card.innerHTML =
      '<div class="snip-meta">' +
      '<span class="snip-tag"></span>' +
      '<span class="snip-state muted"></span>' +
      '<span class="post-grow"></span>' +
      '<button class="react vis-btn" type="button"></button>' +
      '<button class="react del-btn" type="button">delete</button>' +
      "</div>" +
      '<pre class="snip-code"></pre>';
    card.querySelector(".snip-tag").textContent =
      row.language + " · " + row.level + " · " + row.topic;
    card.querySelector(".snip-state").textContent = row.active
      ? row.status === "public"
        ? "public"
        : "private"
      : "hidden after " + row.reports + " reports";
    card.querySelector(".snip-code").textContent = row.code;

    const vis = card.querySelector(".vis-btn");
    vis.textContent = row.status === "public" ? "make private" : "publish";
    vis.onclick = async () => {
      vis.disabled = true;
      await fetch("/api/snippets/" + row.id + "/status", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ public: row.status !== "public" }),
      });
      loadMySnippets();
      initMeta();
    };
    card.querySelector(".del-btn").onclick = async () => {
      await fetch("/api/snippets/" + row.id, {
        method: "DELETE",
        credentials: "same-origin",
      });
      loadMySnippets();
      initMeta();
    };
    return card;
  }

  async function saveSnippet() {
    const err = el2("snipErr");
    err.textContent = "";
    if (!S.me) {
      err.textContent = "you need a profile first";
      return;
    }
    const code = el2("snipCode").value;
    if (code.trim().length < 20) {
      err.textContent = "that is too short — at least 20 characters";
      return;
    }
    const btn = el2("snipSave");
    btn.disabled = true;
    try {
      const res = await fetch("/api/snippets", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          language: el2("snipLang").value,
          level: el2("snipLevel").value,
          topic: el2("snipTopic").value,
          new_topic: el2("snipNewTopic").value.trim(),
          code,
          output: el2("snipOutput").value,
          public: el2("snipPublic").checked,
        }),
      });
      const d = await res.json();
      if (!res.ok) {
        err.textContent =
          d.error === "duplicate"
            ? "that snippet is already in the library"
            : d.error === "rate_limited"
            ? "you have hit today's limit of " + d.per_day
            : d.error === "too_short"
            ? "at least " + d.min + " characters"
            : d.error === "too_long"
            ? "keep it under " + d.max + " characters"
            : d.error === "bad_topic"
            ? "pick a topic or give the new one a real name"
            : "could not save that";
        return;
      }
      el2("snipCode").value = "";
      el2("snipOutput").value = "";
      el2("snipNewTopic").value = "";
      err.textContent = "";
      await initMeta();
      fillSelect(el2("snipTopic"), S.meta.topics, d.topic);
      loadMySnippets();
    } catch (e) {
      err.textContent = "network error";
    } finally {
      btn.disabled = false;
    }
  }

  /* ---------- wiring ---------- */
  on(el2("feedBtn"), "click", showFeed);
  on(el2("playersBtn"), "click", showPlayers);
  on(el2("lobbiesBtn"), "click", showLobbies);
  on(el2("awardsBtn"), "click", () => showAwards(0));
  on(el.cvDrop, "click", () => el.cvFile.click());
  on(el.cvFile, "change", (e) => openCoverCropper(e.target.files && e.target.files[0]));
  on(el2("cvRecrop"), "click", closeCoverCropper);
  on(el.cvZoom, "input", () => {
    COVER.zoom = parseInt(el.cvZoom.value, 10) / 100;
    drawCover();
  });
  on(el.cvRemove, "click", async () => {
    await fetch("/api/cover", { method: "DELETE", credentials: "same-origin" }).catch(() => {});
    if (S.me) S.me.cover = 0;
    el.cvRemove.classList.add("hidden");
    closeCoverCropper();
  });
  on(el.cvDrop, "dragover", (e) => { e.preventDefault(); el.cvDrop.classList.add("over"); });
  on(el.cvDrop, "dragleave", () => el.cvDrop.classList.remove("over"));
  on(el.cvDrop, "drop", (e) => {
    e.preventDefault();
    el.cvDrop.classList.remove("over");
    openCoverCropper(e.dataTransfer.files && e.dataTransfer.files[0]);
  });
  dragCrop(el.cvStage, COVER, drawCover);

  on(el2("rpClose"), "click", closeReplay);
  on(el2("rpPlay"), "click", () => (RP.playing ? rpPause() : rpPlay()));
  on(el2("rpRestart"), "click", () => { rpSeekTo(0); rpPlay(); });
  on(el2("rpScrub"), "input", () => {
    if (!RP.data) return;
    rpPause();
    rpSeekTo((parseInt(el2("rpScrub").value, 10) / 1000) * rpTotal());
  });
  on(el2("rpSpeed"), "click", (e) => {
    const b = e.target.closest("button[data-speed]");
    if (!b) return;
    RP.speed = parseFloat(b.dataset.speed) || 1;
    for (const x of el2("rpSpeed").querySelectorAll("button")) x.classList.toggle("on", x === b);
  });
  on(el2("replayModal"), "click", (e) => {
    if (e.target === el2("replayModal")) closeReplay();
  });

  on(el2("pfViewPublic"), "click", () => {
    closeProfile();
    if (S.me) showUser(S.me.id);
  });
  on(el2("roomStrict"), "change", () =>
    send({ t: "mode", strict: el2("roomStrict").checked })
  );
  on(el2("roomRanked"), "change", () =>
    send({ t: "mode", ranked: el2("roomRanked").checked })
  );
  on(el2("roomSuggest"), "change", () =>
    send({ t: "mode", suggest: el2("roomSuggest").checked })
  );
  on(el2("roomLimit"), "change", () =>
    send({ t: "mode", limit: parseInt(el2("roomLimit").value || "0", 10) })
  );
  on(el2("backBtn"), "click", backToGame);
  on(el.resign, "click", giveUp);
  on(el2("newLobbyGo"), "click", createListedLobby);
  on(el2("lobbyRefresh"), "click", loadLobbies);
  on(el2("newPrivate"), "change", () => {
    const box = el2("newKeyField");
    if (box) box.classList.toggle("hidden", !el2("newPrivate").checked);
  });
  on(el2("keyCancel"), "click", closeKeyPrompt);
  on(el2("keyGo"), "click", submitKey);
  on(el2("keyInput"), "keydown", (e) => {
    if (e.key === "Enter") submitKey();
  });
  on(el2("chToastOpen"), "click", () => {
    dismissToast();
    showPlayers();
  });
  on(el2("snippetsBtn"), "click", showSnippets);
  on(el2("feedMore"), "click", () => loadFeed(true));
  on(el2("snipSave"), "click", saveSnippet);
  on(el2("reportCancel"), "click", closeReport);
  on(el2("reportSend"), "click", sendReport);
  on(el2("reportModal"), "click", (e) => {
    if (e.target === el2("reportModal")) closeReport();
  });
  for (const b of document.querySelectorAll(".js-back")) {
    on(b, "click", backToGame);
  }

  loadDisplay();
  paintBackButton();
  let resizeTimer = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(remeasure, 120);
  });
  Promise.all([initMeta(), loadMe(), loadBots()]).then(() => {
    // the old ?l=CODE links keep working
    const code = new URLSearchParams(location.search).get("l");
    if (code) {
      history.replaceState(null, "", "/race/" + code.toUpperCase());
      joinLobby(code);
      return;
    }
    if (location.pathname !== "/") {
      ROUTING = true;
      try {
        openPath(location.pathname, location.search);
      } finally {
        ROUTING = false;
      }
    }
  });
})();
