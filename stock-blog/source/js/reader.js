/* ============================================================
   朗读全文 · 语音播报（TTS）
   - 在含正文（#article-container）的页面右下角显示「朗读」按钮
   - 点击后展开控制条：播放/暂停、停止、语速、语音选择、进度
   - 朗读时高亮正在朗读的段落，并自动滚动到视野内
   - 使用浏览器原生 Web Speech API（SpeechSynthesis），无需后端
   ============================================================ */
(function () {
  'use strict';

  if (window.__stockReaderLoaded) return;
  window.__stockReaderLoaded = true;

  // 不支持语音合成的环境直接退出
  if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) return;

  var container =
    document.querySelector('#article-container.post-content') ||
    document.querySelector('#article-container');
  if (!container) return;

  /* ---------------- 1. 抽取正文朗读单元 ---------------- */
  var SKIP_SEL =
    'script,style,pre,code,.katex,.katex-display,[hidden],noscript,svg,.reader-root';
  var BLOCK_SEL =
    'p,li,h1,h2,h3,h4,h5,h6,td,th,blockquote,figcaption,dt,dd,caption,.summary-card,.reflection-card';

  function isVisible(el) {
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  // 长段落按句切分，避免单次朗读过长
  function splitLong(text) {
    var parts = text.match(/[^。！？；…\n]+[。！？；…]?/g) || [text];
    var out = [];
    var buf = '';
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (buf && (buf + p).length > 160) {
        out.push(buf);
        buf = p;
      } else {
        buf += p;
      }
    }
    if (buf) out.push(buf);
    return out;
  }

  function buildUnits() {
    var units = [];
    var map = new Map(); // el -> { el, parts: [] }
    var order = [];
    var walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      var parent = node.parentElement;
      if (!parent) continue;
      if (parent.closest(SKIP_SEL)) continue;
      var t = (node.nodeValue || '').replace(/\s+/g, ' ').trim();
      if (!t) continue;
      var el = parent.closest(BLOCK_SEL) || parent;
      if (!el || !isVisible(el)) continue;
      if (!map.has(el)) {
        map.set(el, { el: el, parts: [] });
        order.push(el);
      }
      map.get(el).parts.push(t);
    }
    for (var k = 0; k < order.length; k++) {
      var item = map.get(order[k]);
      var text = item.parts.join(' ');
      if (!text) continue;
      var chunks = text.length > 160 ? splitLong(text) : [text];
      for (var c = 0; c < chunks.length; c++) {
        var trimmed = chunks[c].trim();
        if (trimmed) units.push({ el: item.el, text: trimmed });
      }
    }
    return units;
  }

  var units = buildUnits();
  if (!units.length) return;

  /* ---------------- 2. 语音与状态 ---------------- */
  var state = {
    idx: 0, // 当前单元下标
    playing: false,
    paused: false,
    stopped: true,
    rate: 1.5,
    voice: null,
    lastEl: null
  };

  var storeKey = 'stock-reader';
  try {
    var saved = JSON.parse(localStorage.getItem(storeKey) || '{}');
    if (typeof saved.rate === 'number') state.rate = saved.rate;
    if (typeof saved.voiceName === 'string') state.savedVoice = saved.voiceName;
  } catch (e) {}

  function savePrefs() {
    try {
      localStorage.setItem(
        storeKey,
        JSON.stringify({ rate: state.rate, voiceName: state.voice ? state.voice.name : '' })
      );
    } catch (e) {}
  }

  var PREFERRED_ZH = [
    'Xiaoxiao', 'Yunxi', 'Yunyang', 'Yunjian', 'Yunxia', 'Xiaoyi',
    'Huihui', 'Yaoyao', 'Kangkang', 'Tingting', 'Lili', 'Meijia',
    'Yating', 'Yuqing', 'Shengnan', 'Xiaobei', 'Xiaomei', 'Xiaohan', 'Xiaoxuan'
  ];

  function zhVoices() {
    var vs = speechSynthesis.getVoices();
    var zh = vs.filter(function (v) { return /^zh/i.test(v.lang); });
    // 优先自然语音
    zh.sort(function (a, b) {
      var na = a.name.toLowerCase().indexOf('natural') > -1 ? 1 : 0;
      var nb = b.name.toLowerCase().indexOf('natural') > -1 ? 1 : 0;
      return nb - na;
    });
    return zh.length ? zh : vs;
  }

  function pickDefault() {
    var vs = zhVoices();
    if (state.savedVoice) {
      var hit = vs.filter(function (v) { return v.name === state.savedVoice; })[0];
      if (hit) return hit;
    }
    for (var i = 0; i < PREFERRED_ZH.length; i++) {
      var f = vs.filter(function (v) { return v.name.indexOf(PREFERRED_ZH[i]) > -1; })[0];
      if (f) return f;
    }
    return vs[0] || null;
  }

  /* ---------------- 3. 界面构建 ---------------- */
  var root = document.createElement('div');
  root.className = 'reader-root';
  root.id = 'reader-root';
  root.innerHTML =
    '<button type="button" class="reader-toggle" id="reader-toggle" title="朗读全文">' +
    '<span class="reader-toggle-icon">&#128266;</span><span class="reader-toggle-text">朗读</span></button>' +
    '<div class="reader-panel" id="reader-panel" hidden>' +
    '  <div class="reader-panel-head">' +
    '    <span class="reader-title">全文朗读</span>' +
    '    <button type="button" class="reader-close" id="reader-close" title="关闭">&#10005;</button>' +
    '  </div>' +
    '  <div class="reader-row reader-buttons">' +
    '    <button type="button" class="reader-btn reader-btn-play" id="reader-play">&#9654; 播放</button>' +
    '    <button type="button" class="reader-btn reader-btn-stop" id="reader-stop">&#9632; 停止</button>' +
    '    <label class="reader-rate">语速 ' +
    '      <input type="range" id="reader-rate" min="0.5" max="2" step="0.1" value="' + state.rate + '">' +
    '      <span class="reader-rate-val" id="reader-rate-val">' + state.rate.toFixed(1) + 'x</span>' +
    '    </label>' +
    '  </div>' +
    '  <div class="reader-row reader-voice-row">' +
    '    <label class="reader-voice">语音' +
    '      <select id="reader-voice"></select>' +
    '    </label>' +
    '  </div>' +
    '  <div class="reader-progress">' +
    '    <span class="reader-progress-text" id="reader-pos">第 1 / ' + units.length + ' 段</span>' +
    '    <div class="reader-bar"><i id="reader-bar-fill" style="width:0%"></i></div>' +
    '  </div>' +
    '</div>';

  var style = document.createElement('style');
  style.textContent =
    '.reader-root{--rd-main:#0d47a1;--rd-hover:#00bcd4;--rd-bg:#ffffff;--rd-text:#1f2937;--rd-border:rgba(13,71,161,.18);--rd-shadow:0 8px 28px rgba(13,71,161,.22);}' +
    'html.dark .reader-root{--rd-main:#ff8a3c;--rd-hover:#ffb74d;--rd-bg:#2a2626;--rd-text:#f2ecec;--rd-border:rgba(255,138,60,.25);--rd-shadow:0 8px 28px rgba(0,0,0,.4);}' +
    '.reader-toggle{position:fixed;right:20px;bottom:96px;z-index:1000;display:inline-flex;align-items:center;gap:6px;padding:9px 16px;border:none;border-radius:24px;cursor:pointer;font-size:14px;font-weight:600;color:#fff;background:linear-gradient(135deg,var(--rd-main),#00838f);box-shadow:0 4px 16px rgba(0,188,212,.35);transition:transform .2s,box-shadow .2s;}' +
    '.reader-toggle:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,188,212,.45);}' +
    'html.dark .reader-toggle{background:linear-gradient(135deg,#e65100,#f57c00);box-shadow:0 4px 16px rgba(0,0,0,.4);}' +
    '.reader-toggle.is-playing{background:linear-gradient(135deg,#e65100,#f57c00);}' +
    '.reader-toggle-icon{font-size:16px;line-height:1;}' +
    '.reader-panel{position:fixed;right:20px;bottom:150px;z-index:1001;width:340px;max-width:calc(100vw - 32px);padding:12px 14px;border-radius:14px;background:var(--rd-bg);color:var(--rd-text);border:1px solid var(--rd-border);box-shadow:var(--rd-shadow);font-size:13px;}' +
    '.reader-panel-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}' +
    '.reader-title{font-weight:700;font-size:14px;color:var(--rd-main);}' +
    '.reader-close{border:none;background:none;cursor:pointer;font-size:15px;color:var(--rd-text);opacity:.7;padding:0 2px;}' +
    '.reader-close:hover{opacity:1;}' +
    '.reader-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;}' +
    '.reader-btn{border:none;cursor:pointer;border-radius:8px;padding:7px 14px;font-size:13px;font-weight:600;color:#fff;transition:filter .15s;}' +
    '.reader-btn-play{background:linear-gradient(135deg,#0d47a1,#00bcd4);}' +
    '.reader-btn-stop{background:linear-gradient(135deg,#e65100,#f57c00);}' +
    'html.dark .reader-btn-play{background:linear-gradient(135deg,#e65100,#f57c00);}' +
    'html.dark .reader-btn-stop{background:linear-gradient(135deg,#0d47a1,#00bcd4);}' +
    '.reader-btn:hover{filter:brightness(1.08);}' +
    '.reader-rate{display:inline-flex;align-items:center;gap:6px;color:var(--rd-text);}' +
    '.reader-rate input[type=range]{width:90px;accent-color:var(--rd-main);}' +
    '.reader-rate-val{min-width:34px;text-align:right;font-weight:600;}' +
    '.reader-voice-row .reader-voice{display:flex;align-items:center;gap:6px;color:var(--rd-text);width:100%;}' +
    '.reader-voice select{flex:1;min-width:0;padding:4px 6px;border-radius:6px;border:1px solid var(--rd-border);background:var(--rd-bg);color:var(--rd-text);font-size:12px;}' +
    '.reader-progress{display:flex;align-items:center;gap:8px;margin-top:2px;}' +
    '.reader-progress-text{flex:0 0 auto;font-size:12px;color:var(--rd-text);opacity:.75;}' +
    '.reader-bar{flex:1;height:6px;border-radius:3px;background:rgba(128,128,128,.18);overflow:hidden;}' +
    '.reader-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--rd-main),var(--rd-hover));transition:width .3s;}' +
    '.reader-active{background:#fff3cd !important;border-radius:4px;box-shadow:0 0 0 3px rgba(255,193,7,.25);}' +
    'html.dark .reader-active{background:#4a3b18 !important;box-shadow:0 0 0 3px rgba(255,193,7,.2);}' +
    '@media (max-width:768px){.reader-toggle{right:16px;bottom:84px;}.reader-panel{right:12px;bottom:138px;}}';

  document.body.appendChild(style);
  document.body.appendChild(root);

  var toggle = root.querySelector('#reader-toggle');
  var panel = root.querySelector('#reader-panel');
  var playBtn = root.querySelector('#reader-play');
  var stopBtn = root.querySelector('#reader-stop');
  var closeBtn = root.querySelector('#reader-close');
  var rateInput = root.querySelector('#reader-rate');
  var rateVal = root.querySelector('#reader-rate-val');
  var voiceSel = root.querySelector('#reader-voice');
  var posEl = root.querySelector('#reader-pos');
  var barFill = root.querySelector('#reader-bar-fill');
  var toggleText = root.querySelector('.reader-toggle-text');

  /* ---------------- 4. 语音列表 ---------------- */
  function fillVoices() {
    var vs = zhVoices();
    if (!vs.length) return;
    voiceSel.innerHTML = '';
    vs.forEach(function (v) {
      var opt = document.createElement('option');
      opt.value = v.name;
      opt.textContent = v.name + ' (' + v.lang + ')';
      voiceSel.appendChild(opt);
    });
    if (state.voice) voiceSel.value = state.voice.name;
    else {
      state.voice = pickDefault();
      if (state.voice) voiceSel.value = state.voice.name;
    }
  }

  function syncVoiceFromSelect() {
    var vs = speechSynthesis.getVoices();
    var found = vs.filter(function (v) { return v.name === voiceSel.value; })[0];
    if (found) state.voice = found;
    savePrefs();
  }

  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = function () {
      fillVoices();
      if (!state.voice) state.voice = pickDefault();
    };
  }
  fillVoices();

  /* ---------------- 5. 朗读流程 ---------------- */
  function clearHighlight() {
    if (state.lastEl) {
      state.lastEl.classList.remove('reader-active');
      state.lastEl = null;
    }
  }

  function updateUi() {
    posEl.textContent = '第 ' + (state.idx + 1) + ' / ' + units.length + ' 段';
    barFill.style.width = (units.length ? ((state.idx + 1) / units.length) * 100 : 0) + '%';
    playBtn.textContent = state.paused ? '\u25B6 继续' : '\u25B6 播放';
    toggleText.textContent = state.playing ? '朗读中' : '朗读';
    toggle.classList.toggle('is-playing', state.playing);
  }

  function scrollToEl(el) {
    if (!el) return;
    var r = el.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    if (r.top < 90 || r.bottom > vh - 90) {
      el.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
  }

  function clearWatchdog() {
    if (state.watchdog) {
      clearInterval(state.watchdog);
      state.watchdog = null;
    }
  }

  function speakUnit() {
    if (state.stopped || !state.playing) return;
    if (state.idx >= units.length) {
      stop(true);
      return;
    }
    var u = units[state.idx];
    clearHighlight();
    u.el.classList.add('reader-active');
    state.lastEl = u.el;
    scrollToEl(u.el);
    updateUi();

    var utter = new SpeechSynthesisUtterance(u.text);
    if (state.voice) utter.voice = state.voice;
    utter.lang = state.voice && state.voice.lang ? state.voice.lang : 'zh-CN';
    utter.rate = state.rate;

    var advanced = false;
    var retried = false;
    function advance() {
      if (advanced) return;
      advanced = true;
      state.stall = 0;
      state.idx++;
      speakUnit();
    }
    utter.onend = advance;
    utter.onerror = function (e) {
      if (e.error === 'canceled' || e.error === 'interrupted') return;
      // 合成出错：原地重试一次，绝不自动向下跳段
      if (!retried) {
        retried = true;
        clearWatchdog();
        try { speechSynthesis.cancel(); } catch (err) {}
        state.retryPending = true;
        setTimeout(function () {
          state.retryPending = false;
          if (state.stopped || !state.playing) return;
          speakUnit();
        }, 150);
      }
    };
    speechSynthesis.speak(utter);

    // 规避 Chromium「连续播报约 15 秒后静音停摆」的 Bug：
    // 每隔数秒 pause+resume 重置引擎内部计时；若引擎停摆（既没在说话
    // 也没触发 onend）则原地重播当前段，避免出现「跳着读」。
    clearWatchdog();
    state.watchdog = setInterval(function () {
      if (state.stopped || !state.playing || state.paused) return;
      if (state.retryPending) return;
      if (speechSynthesis.speaking) {
        try { speechSynthesis.pause(); speechSynthesis.resume(); } catch (err) {}
      } else if (!advanced) {
        state.stall = (state.stall || 0) + 1;
        if (state.stall > 2) { stop(true); return; }
        try { speechSynthesis.cancel(); } catch (err) {}
        speakUnit();
      }
    }, 8000);
  }

  function play() {
    if (state.playing && !state.stopped) {
      // 已播放 -> 暂停/继续
      if (state.paused) {
        speechSynthesis.resume();
        state.paused = false;
      } else {
        speechSynthesis.pause();
        state.paused = true;
      }
      updateUi();
      return;
    }
    // 从头或继续开始
    if (state.stopped || state.idx >= units.length) state.idx = 0;
    state.playing = true;
    state.stopped = false;
    state.paused = false;
    state.stall = 0;
    updateUi();
    speakUnit();
  }

  function stop(done) {
    if (speechSynthesis.speaking || speechSynthesis.pending) {
      try { speechSynthesis.cancel(); } catch (e) {}
    }
    clearWatchdog();
    state.playing = false;
    state.stopped = true;
    state.paused = false;
    state.stall = 0;
    state.retryPending = false;
    clearHighlight();
    if (!done) state.idx = 0;
    updateUi();
  }

  /* ---------------- 6. 事件绑定 ---------------- */
  toggle.addEventListener('click', function () {
    var hidden = panel.hidden;
    panel.hidden = !hidden;
    if (!hidden) fillVoices();
  });
  closeBtn.addEventListener('click', function () {
    panel.hidden = true;
  });
  playBtn.addEventListener('click', play);
  stopBtn.addEventListener('click', function () { stop(false); });
  rateInput.addEventListener('input', function () {
    state.rate = parseFloat(rateInput.value) || 1;
    rateVal.textContent = state.rate.toFixed(1) + 'x';
    savePrefs();
    // 正在播放时立即生效
    if (state.playing && !state.stopped) {
      speechSynthesis.cancel();
      speakUnit();
    }
  });
  voiceSel.addEventListener('change', function () {
    syncVoiceFromSelect();
    if (state.playing && !state.stopped) {
      speechSynthesis.cancel();
      speakUnit();
    }
  });

  // 页面离开时停止，避免后台残留声音
  window.addEventListener('beforeunload', function () {
    clearWatchdog();
    try { speechSynthesis.cancel(); } catch (e) {}
  });
})();
