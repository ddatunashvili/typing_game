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
    pfRecrop: $("pfRecrop"),
    ranksBtn: $("ranksBtn"),
    ranksBack: $("ranksBack"),
    ranks: $("screen-ranks"),
    ranksTable: $("ranksTable"),
    ranksBots: $("ranksBots"),
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
    if (!R.startedAt) R.startedAt = performance.now();
    if (endsAtMs != null) R.endsAt = endsAtMs;
    el.codeBox.classList.remove("locked");
    el.hint.textContent = R.timed
      ? "type! — a new snippet appears while the clock runs"
      : "type! — indentation is auto-skipped";
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
      markCursor();
      scrollToCursor();
      el.hudLeft.textContent = T.code.length - T.pos;
      if (T.pos >= T.code.length) snippetDone();
      return;
    }

    T.errors++;
    T.bad = true;
    span.classList.add("bad");
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
    markCursor();
    scrollToCursor();
    el.hudLeft.textContent = T.code.length - T.pos;
  }

  function onKeyDown(e) {
    if (!T.running || S.spectating) return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === "Backspace") { e.preventDefault(); backspace(); return; }
    if (e.key === "Enter") { e.preventDefault(); typeChar("\n"); return; }
    if (e.key === "Tab") { e.preventDefault(); typeChar("\t"); return; }
    if (e.key.length === 1) { e.preventDefault(); typeChar(e.key); }
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

  function openProfile() {
    renderThemes();
    wireDisplayToggles();
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
    el.modal.classList.remove("hidden");
    el.pfName.focus();
  }

  function closeProfile() {
    el.modal.classList.add("hidden");
  }

  /* ---------- avatar cropper ---------- */
  const CROP_PX = 256;
  const CROP = { img: null, zoom: 1, x: 0, y: 0, drag: null };

  function drawCrop() {
    const ctx = el.pfCanvas.getContext("2d");
    ctx.clearRect(0, 0, CROP_PX, CROP_PX);
    if (!CROP.img) return;
    const img = CROP.img;
    // "cover" the square, then apply the zoom and the drag offset
    const base = Math.max(CROP_PX / img.width, CROP_PX / img.height);
    const scale = base * CROP.zoom;
    const w = img.width * scale;
    const h = img.height * scale;
    const maxX = Math.max(0, (w - CROP_PX) / 2);
    const maxY = Math.max(0, (h - CROP_PX) / 2);
    CROP.x = Math.max(-maxX, Math.min(maxX, CROP.x));
    CROP.y = Math.max(-maxY, Math.min(maxY, CROP.y));
    ctx.drawImage(img, (CROP_PX - w) / 2 + CROP.x, (CROP_PX - h) / 2 + CROP.y, w, h);
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
        body: JSON.stringify({ name }),
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
        history.replaceState(null, "", "/?l=" + m.code);
        showRoom();
        break;
      case "error":
        showHome();
        el.homeErr.textContent =
          m.code === "no_lobby"
            ? "lobby not found"
            : m.code === "bad_key"
            ? "that lobby needs a key"
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
      case "go":
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
        armRace(
          S.lobby && S.lobby.duration > 0
            ? performance.now() + S.lobby.duration * 1000
            : null
        );
        break;
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
    if (!armed && (!prev || prev.state !== st.state || prev.snippet !== st.snippet)) {
      initRun(st.duration > 0, st.playlist || []);
    }

    const snippetChanged =
      !prev || prev.snippet !== st.snippet || prev.language !== st.language;
    if ((snippetChanged && !armed) || (!T.chars.length && st.snippet)) {
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

      el.ranksBots.innerHTML = "";
      (data.bots || []).slice().reverse().forEach((bot, i) =>
        el.ranksBots.appendChild(rankRow(i + 1, bot, false))
      );

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
                     "screen-lobbies"]) {
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
    history.replaceState(null, "", "/");
    renderFilters();
    paintBackButton();
  }

  function showRoom() {
    el.ranks.classList.add("hidden");
    for (const id of ["screen-feed", "screen-players", "screen-user", "screen-snippets",
                     "screen-lobbies"]) {
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
    send({ t: "resign" });
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

  function screenOnly(node) {
    for (const s of [el.home, el.room, el.ranks, el2("screen-feed"),
                     el2("screen-players"), el2("screen-user"),
                     el2("screen-snippets"), el2("screen-lobbies")]) {
      if (s) s.classList.toggle("hidden", s !== node);
    }
    clearInterval(S.ranksTimer);
    clearInterval(SOCIAL.playersTimer);
    clearInterval(SOCIAL.lobbiesTimer);
    paintBackButton();
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
      el2("userRank").textContent = p.rank + " · " + p.rating;
      el2("userSeen").textContent =
        (p.online ? "online now" : idleText(p.idle)) +
        (p.joined ? " · joined " + p.joined.slice(0, 10) : "");
      paintAvatar(el2("userAvatar"), p);

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
    if (r.levels && r.levels.length) bits.push(r.levels.join("/"));
    if (r.topics && r.topics.length) bits.push(r.topics.join("/"));
    row.querySelector(".lb-sub").textContent = bits.join(" \u00b7 ");

    const state = row.querySelector(".lb-state");
    state.textContent = r.state;
    state.className = "badge lb-state " + r.state;

    const people = [r.humans + (r.humans === 1 ? " player" : " players")];
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
    const code = new URLSearchParams(location.search).get("l");
    if (code) joinLobby(code);
  });
})();
