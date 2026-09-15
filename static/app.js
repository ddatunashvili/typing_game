/* CodeRace client: typing engine, filters, profile and lobby websocket. */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);

  const el = {
    home: $("screen-home"),
    room: $("screen-room"),
    name: $("nameInput"),
    nameField: $("nameField"),
    register: $("registerBtn"),
    profileBox: $("profileBox"),
    profileAvatar: $("profileAvatar"),
    profileName: $("profileName"),
    profileEdit: $("profileEdit"),
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
  };

  const LANG_FALLBACK = { markup: "markup", html: "markup" };

  function readList(key) {
    try {
      const raw = JSON.parse(localStorage.getItem(key) || "[]");
      return Array.isArray(raw) ? raw.filter((v) => typeof v === "string") : [];
    } catch (err) {
      return [];
    }
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
    lobby: null,
    snipLevel: "",
    snipTopic: "",
    soloLevel: "",  // level the solo session is pinned to
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

  function renderCode(code, lang) {
    T.code = code;
    el.codeArea.innerHTML = Prism.highlight(code, grammarFor(lang), lang);
    T.chars = wrapChars(el.codeArea);
    if (T.chars.length !== code.length) {
      // highlighting desynced from source: fall back to plain text
      el.codeArea.textContent = code;
      T.chars = wrapChars(el.codeArea);
    }
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
    for (const span of T.chars) span.className = span.className.replace(/ (done|cur|bad)/g, "");
    el.codeBox.scrollTop = 0;
    paintHud(0, 100, 0);
    el.hudLeft.textContent = T.code.length;
    markCursor();
  }

  function markCursor() {
    for (const span of T.chars) span.classList.remove("cur");
    const span = T.chars[T.pos];
    if (span) span.classList.add("cur");
  }

  function scrollToCursor() {
    const span = T.chars[T.pos];
    if (!span) return;
    const box = el.codeBox;
    const top = span.offsetTop;
    const h = span.offsetHeight || 24;
    if (top < box.scrollTop + 24) box.scrollTop = Math.max(0, top - 24);
    else if (top + h > box.scrollTop + box.clientHeight - 24)
      box.scrollTop = top + h - box.clientHeight + 24;
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
    if (!T.running) return;
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
    if (S.solo) {
      showTimedResult(w, a);
      recordSolo(w, a, runSeconds());
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
    if (S.solo) {
      if (timed) showTimedResult(w, a);
      else showSoloResult(w, a, secs);
      recordSolo(w, a, secs);
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
    const uid = who.uid != null ? who.uid : who.id;
    const version = who.avatar || 0;
    if (uid && version) {
      node.style.backgroundImage = 'url("' + avatarUrl(uid, version) + '")';
      node.textContent = "";
      node.classList.add("has-img");
    } else {
      node.style.backgroundImage = "";
      node.classList.remove("has-img");
      node.textContent = ((who.name || "?").trim().charAt(0) || "?").toUpperCase();
    }
  }

  function paintProfile() {
    const known = !!S.me;
    el.profileBox.classList.toggle("hidden", !known);
    el.nameField.classList.toggle("hidden", known);
    el.register.classList.toggle("hidden", known || !S.accounts);
    if (known) {
      el.profileName.textContent = S.me.name;
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
    if (S.accounts) loadLeaderboard();
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

  function openProfile() {
    el.pfErr.textContent = "";
    el.pfAvatar.value = "";
    el.pfTitle.textContent = S.me ? "Your profile" : "Create your profile";
    el.pfName.value = S.me ? S.me.name : (el.name.value || "").trim();
    el.pfRemove.classList.toggle("hidden", !(S.me && S.me.avatar));
    paintAvatar(el.pfPreview, S.me || { name: el.pfName.value });
    el.modal.classList.remove("hidden");
    el.pfName.focus();
  }

  function closeProfile() {
    el.modal.classList.add("hidden");
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
      const endpoint = S.me ? "/api/profile" : "/api/register";
      const res = await fetch(endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name }),
      });
      const data = await res.json();
      if (!res.ok) {
        el.pfErr.textContent = data.error || "could not save";
        return;
      }
      S.me = data.user;
      localStorage.setItem("cr_name", name);

      const file = el.pfAvatar.files && el.pfAvatar.files[0];
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

  async function recordSolo(w, a, secs) {
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
        }),
      });
      loadLeaderboard();
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
      idx: R.idx,
      chars: liveChars(),
      snips: R.snips,
    });
  }

  function connect(code, create) {
    if (S.ws) { S.ws.onclose = null; S.ws.close(); }
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    const qs = new URLSearchParams({
      name: currentName(),
      pid: S.pid,
      create: create ? "1" : "0",
      lang: S.lang,
      levels: S.levels.join(","),
      topics: S.topics.join(","),
      duration: String(S.duration == null ? -1 : S.duration),
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
        localStorage.setItem("cr_pid", m.id);
        el.name.value = m.name;
        el.roomCode.textContent = m.code;
        el.codeText.textContent = m.code;
        history.replaceState(null, "", "/?l=" + m.code);
        showRoom();
        break;
      case "error":
        showHome();
        el.homeErr.textContent = m.code === "no_lobby" ? "lobby not found" : "connection error";
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
        if (S.lobby) {
          initRun(S.lobby.duration > 0, S.lobby.playlist || []);
          const first = R.playlist[0];
          if (first) {
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

    const isHost = st.host === S.pid;
    const me = st.players.find((p) => p.id === S.pid);
    el.ready.classList.toggle("hidden", st.state !== "waiting");
    el.start.classList.toggle("hidden", !(isHost && st.state === "waiting"));
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

    // Only a running race is off limits: during the countdown we want the new
    // snippet on screen already, so players can read ahead.
    const armed = st.state === "racing";
    if (!armed && (!prev || prev.state !== st.state || prev.snippet !== st.snippet)) {
      initRun(st.duration > 0, st.playlist || []);
    }

    const snippetChanged = !prev || prev.snippet !== st.snippet || prev.language !== st.language;
    if (snippetChanged && !armed) renderCode(st.snippet, st.language);

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
    if (st.state === "racing" && !T.running && !R.over && me && !me.finished) {
      // ends_at is a unix time in seconds; the server ends the race either way.
      const leftMs = st.ends_at ? st.ends_at * 1000 - Date.now() : 0;
      armRace(st.duration > 0 ? performance.now() + Math.max(0, leftMs) : null);
    }

    renderRacers(st);
    if (st.state === "finished") {
      renderResults(st);
      if (S.me) loadLeaderboard();
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
    paintRacer(p);
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
      '<div class="who"><span class="avatar sm"></span><span class="nm"></span><span class="tag"></span></div>' +
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
      ? "<tr><th>#</th><th>player</th><th>snippets</th><th>chars</th><th>wpm</th><th>acc</th></tr>"
      : "<tr><th>#</th><th>player</th><th>wpm</th><th>acc</th><th>time</th></tr>";
    el.results.innerHTML =
      "<h3>results" + (timed ? " · " + durationLabel(st.duration) : "") + "</h3><table>" +
      head +
      rows
        .map((p) => {
          const cells = timed
            ? "<td>" + (p.snips || 0) + "</td><td>" + (p.chars || 0) + "</td><td>" +
              Math.round(p.wpm) + "</td><td>" + Math.round(p.acc) + "%</td>"
            : "<td>" + Math.round(p.wpm) + "</td><td>" + Math.round(p.acc) + "%</td><td>" +
              (p.time != null ? p.time.toFixed(1) + "s" : "-") + "</td>";
          return (
            '<tr class="' + (p.id === S.pid ? "me" : "") + '"><td>' +
            (p.place || "-") + "</td><td>" + escapeHtml(p.name) + "</td>" + cells + "</tr>"
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
      div.className = "msg" + (m.id === S.pid ? " me" : "");
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

  // ---------- screens ----------
  function currentName() {
    if (S.me) return S.me.name;
    const v = (el.name.value || "").trim().slice(0, 18);
    return v || "Guest" + Math.floor(Math.random() * 900 + 100);
  }

  function showHome() {
    S.room = null;
    S.solo = false;
    stopRace();
    el.home.classList.remove("hidden");
    el.room.classList.add("hidden");
    el.leave.classList.add("hidden");
    el.name.disabled = false;
    el.roomFilters.classList.add("hidden");
    history.replaceState(null, "", "/");
    renderFilters();
  }

  function showRoom() {
    el.hudSnipsBox.classList.toggle("hidden", !R.timed);
    el.homeErr.textContent = "";
    el.home.classList.add("hidden");
    el.room.classList.remove("hidden");
    el.leave.classList.remove("hidden");
    el.name.disabled = true;
    document.querySelector(".chat").classList.toggle("hidden", S.solo);
    el.racers.classList.toggle("hidden", S.solo);
    el.ready.classList.toggle("hidden", S.solo);
    el.start.classList.toggle("hidden", S.solo);
    el.filterBtn.classList.toggle("hidden", S.solo);
    el.newSnip.classList.toggle("hidden", S.solo);
    document.querySelector(".room-meta").classList.toggle("hidden", S.solo);
    focusTrap();
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
      const qs =
        "lang=" + encodeURIComponent(S.lang) +
        "&size=40" +
        (S.soloLevel ? "&level=" + encodeURIComponent(S.soloLevel) : "") +
        (filterQuery() ? "&" + filterQuery() : "");
      const res = await fetch("/api/playlist?" + qs);
      const data = await res.json();
      SOLO.deck = data.playlist || [];
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
    connect(code.toUpperCase(), false);
  }

  el.name.value = S.name || "";
  el.name.addEventListener("change", () => localStorage.setItem("cr_name", el.name.value.trim()));

  el.solo.onclick = startSolo;
  el.create.onclick = createLobby;
  el.joinForm.onsubmit = (e) => {
    e.preventDefault();
    const code = el.joinCode.value.trim();
    if (code.length >= 4) joinLobby(code);
  };
  el.leave.onclick = leave;

  el.register.onclick = openProfile;
  el.profileEdit.onclick = openProfile;
  el.pfCancel.onclick = closeProfile;
  el.pfSave.onclick = saveProfile;
  el.pfRemove.onclick = removeAvatar;
  el.pfAvatar.onchange = () => {
    const file = el.pfAvatar.files && el.pfAvatar.files[0];
    if (!file) return;
    if (file.size > 512 * 1024) {
      el.pfErr.textContent = "image is over 512 KB";
      el.pfAvatar.value = "";
      return;
    }
    el.pfErr.textContent = "";
    el.pfPreview.style.backgroundImage = 'url("' + URL.createObjectURL(file) + '")';
    el.pfPreview.textContent = "";
    el.pfPreview.classList.add("has-img");
  };
  el.modal.onclick = (e) => {
    if (e.target === el.modal) closeProfile();
  };

  el.topicAll.onclick = () => {
    const cat = catalogFor(S.lang);
    S.topics = cat ? Object.keys(cat.topics) : [];
    saveFilters();
    renderFilters();
  };
  el.topicNone.onclick = () => {
    S.topics = [];
    saveFilters();
    renderFilters();
  };

  el.filterBtn.onclick = () => {
    el.roomFilters.classList.toggle("hidden");
    if (S.lobby) renderRoomFilters(S.lobby);
  };

  el.chatForm.onsubmit = (e) => {
    e.preventDefault();
    const text = el.chatInput.value.trim();
    if (!text) return;
    send({ t: "chat", text });
    el.chatInput.value = "";
    focusTrap();
  };

  el.ready.onclick = () => {
    const me = S.lobby && S.lobby.players.find((p) => p.id === S.pid);
    send({ t: "ready", v: !(me && me.ready) });
  };
  el.start.onclick = () => send({ t: "start" });
  el.again.onclick = () => (S.solo ? loadSoloSnippet() : send({ t: "restart" }));
  el.newSnip.onclick = () => (S.solo ? loadSoloSnippet() : send({ t: "again" }));
  el.langSelect.onchange = () => {
    setLang(el.langSelect.value);
    if (!S.solo) send({ t: "lang", v: el.langSelect.value });
  };
  el.copyLink.onclick = () => {
    navigator.clipboard.writeText(location.origin + "/?l=" + (S.room || ""));
    el.copyLink.classList.add("accent");
    setTimeout(() => el.copyLink.classList.remove("accent"), 600);
  };

  el.codeBox.onclick = focusTrap;
  el.trap.addEventListener("blur", () => el.codeBox.classList.remove("focus"));
  document.addEventListener("keydown", (e) => {
    if (!el.modal.classList.contains("hidden")) return;
    if (document.activeElement === el.chatInput || document.activeElement === el.name ||
        document.activeElement === el.joinCode) return;
    onKeyDown(e);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.activeElement === el.chatInput) focusTrap();
    if (e.key === "Escape" && !el.modal.classList.contains("hidden")) closeProfile();
  });

  Promise.all([initMeta(), loadMe()]).then(() => {
    const code = new URLSearchParams(location.search).get("l");
    if (code) joinLobby(code);
  });
})();
