/* 박시은의 매일매일 공부방 */
(function () {
  'use strict';
  const { shuffle, pick } = window.GEN;
  const $ = (s) => document.querySelector(s);
  const PER_DAY = 10;

  const SUBJECTS = [
    { key: 'korean', name: '국어', icon: '📖' },
    { key: 'english', name: '영어', icon: '🔤' },
    { key: 'calc', name: '연산', icon: '➕' },
    { key: 'math', name: '창의 수학', icon: '🧩' },
    { key: 'time', name: '시간', icon: '🕰️' },
    { key: 'hanja', name: '한자', icon: '🀄' },
    { key: 'art', name: '미술', icon: '🖼️' },
    { key: 'world', name: '세계', icon: '🌏' },
    { key: 'nature', name: '자연', icon: '🦁' },
    { key: 'store', name: '가게', icon: '🏪' },
    { key: 'sports', name: '운동', icon: '⚽' },
    { key: 'music', name: '악기', icon: '🎻' },
    { key: 'recycle', name: '분리수거', icon: '♻️' },
    { key: 'env', name: '환경', icon: '🌱' },
    { key: 'people', name: '사람', icon: '🧑‍🚒' },
    { key: 'society', name: '사회', icon: '🏘️' },
    { key: 'folktale', name: '전래동화', icon: '📜' },
    { key: 'draw', name: '그림', icon: '🎨', draw: true },
  ];
  // 생성기 문제 비율(하루 10문제 중)
  const GEN_SHARE = { calc: 10, math: 5, time: 7, store: 5, hanja: 2 };

  const PRAISE = ['시은아, 정답이야! 🎉', '역시 시은이!', '시은이 천재인걸?', '우와, 맞았어요! 👏', '최고예요, 시은아!', '딩동댕! 정답!', '시은이 정말 똑똑하다!', '멋져요! ⭐', '척척박사 시은이!', '와, 대단해요!'];
  const RETRY = ['아깝다, 시은아! 한 번 더 해볼까?', '괜찮아, 다시 해볼까?', '조금만 더 생각해 볼까?', '천천히 다시 골라 봐요!'];
  const SHOW = ['정답은 이거예요. 다음엔 꼭 맞힐 수 있어요!', '괜찮아요! 정답을 같이 볼까요?', '이번엔 어려웠지? 정답은 이거야!'];
  const DONE = ['오늘도 시은이가 해냈어요! ⭐', '시은이 오늘 10문제 끝! 🎉', '와! 시은이 최고! 오늘 공부 끝!', '참 잘했어요, 시은아! 🏆'];

  // ---------- 저장 ----------
  const STORE_KEY = 'sieun-study-v1';
  function today() { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; }
  function addDays(n) { const d = new Date(); d.setDate(d.getDate() + n); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; }
  let S;
  function load() {
    try { S = JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch (e) { S = {}; }
    S.seen = S.seen || {}; S.wrong = S.wrong || {}; S.daily = S.daily || {}; S.stars = S.stars || 0; S.solved = S.solved || {};
  }
  function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(S)); } catch (e) {} }
  function day(subj) { const t = today(); S.daily[t] = S.daily[t] || {}; S.daily[t][subj] = S.daily[t][subj] || { done: 0, correct: 0, stars: 0 }; return S.daily[t][subj]; }

  // ---------- 음성 ----------
  let voices = [];
  function loadVoices() { voices = window.speechSynthesis ? speechSynthesis.getVoices() : []; }
  if (window.speechSynthesis) { loadVoices(); speechSynthesis.onvoiceschanged = loadVoices; }
  // 자연스러운 음성 우선: 부모님이 고른 음성 > Google/Natural/Neural/Online 음성 > 기기 기본
  const GOOD = /natural|neural|online|google|premium|enhanced|siri|yuna|sunhi|injoon|samantha|ava|jenny|aria/i;
  function voiceFor(lang) {
    const l = lang.toLowerCase(), base = l.split('-')[0];
    const same = voices.filter(v => v.lang.toLowerCase().replace('_', '-') === l);
    const cands = same.length ? same : voices.filter(v => v.lang.toLowerCase().startsWith(base));
    const pref = (S && S.voice || {})[base];
    return cands.find(v => v.name === pref) || cands.find(v => GOOD.test(v.name) && !v.localService) || cands.find(v => GOOD.test(v.name)) || cands[0];
  }
  // parts: [{text, lang}]
  function speak(parts, { cancel = true } = {}) {
    if (!window.speechSynthesis) return;
    if (cancel) speechSynthesis.cancel();
    if (typeof parts === 'string') parts = [{ text: parts }];
    for (const p of parts) {
      if (!p.text) continue;
      const u = new SpeechSynthesisUtterance(cleanForSpeech(p.text));
      u.lang = p.lang || 'ko-KR';
      const v = voiceFor(u.lang); if (v) u.voice = v;
      const sp = (S && S.speechRate) || 1;
      u.rate = (u.lang.startsWith('ko') ? 1.0 : 0.85) * sp;
      u.pitch = 1.0;
      speechSynthesis.speak(u);
    }
  }
  function mathSpeech(t) {
    return String(t).replace(/(\d|□)\s*\+\s*/g, '$1 더하기 ').replace(/(\d|□)\s*[−-]\s*(?=\d|□)/g, '$1 빼기 ').replace(/\s*=\s*/g, ' 은 ').replace(/→/g, '은').replace(/\?$/, '');
  }
  const NATIVE = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두'];
  function cleanForSpeech(t) {
    return String(t).replace(/(\d{1,2})\s?(시간|시|바퀴|달)(?![가-힣]*요일)/g, (m0, n, u) => { n = +n; if (n === 24) return '스물네 ' + u; return n >= 1 && n <= 12 ? NATIVE[n] + ' ' + u : m0; })
      .replace(/(^|[^\d])6월/g, '$1유월').replace(/(^|[^\d])10월/g, '$1시월').replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}️‍]/gu, '').replace(/□/g, '네모').replace(/\(\s*\?\s*\)/g, '빈칸').replace(/[〈〉'"]/g, ' ');
  }

  // ---------- 효과음 (칭찬 소리) ----------
  let actx;
  function chime(ok) {
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const notes = ok ? [523.25, 659.25, 783.99, 1046.5] : [392, 330];
      notes.forEach((f, i) => {
        const o = actx.createOscillator(), g = actx.createGain();
        o.type = ok ? 'triangle' : 'sine'; o.frequency.value = f;
        const t = actx.currentTime + i * (ok ? 0.09 : 0.16);
        g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.25, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
        o.connect(g).connect(actx.destination); o.start(t); o.stop(t + 0.4);
      });
    } catch (e) {}
  }
  let audioEl = null;
  // 칭찬 녹음·소리·음성을 모두 멈춤 (다음 문제로 넘어갈 때 겹치지 않게)
  function stopAll() {
    if (audioEl) { audioEl.pause(); audioEl = null; }
    if (window.speechSynthesis) speechSynthesis.cancel();
  }
  function playSound(src) {
    if (!src) return;
    if (audioEl) { audioEl.pause(); }
    if (window.speechSynthesis) speechSynthesis.cancel();
    audioEl = new Audio(src); audioEl.play().catch(() => {});
  }

  // ---------- AI 녹음 칭찬 목소리 (assets/voice/voice.json 이 있으면 사용, 없으면 TTS) ----------
  let VOICE = {};
  fetch('assets/voice/voice.json').then(r => r.ok ? r.json() : {}).then(j => VOICE = j || {}).catch(() => {});
  function sayPhrase(text) {
    const key = cleanForSpeech(text).trim();
    const f = VOICE[key];
    if (f) { if (window.speechSynthesis) speechSynthesis.cancel(); if (audioEl) audioEl.pause(); const au = new Audio(f); audioEl = au; setTimeout(() => { if (audioEl === au) au.play().catch(() => speak(text)); }, 350); return; }
    speak(text);
  }

  // ---------- 데이터 ----------
  const DATA = {};
  async function loadSubject(key) {
    if (DATA[key]) return DATA[key];
    const r = await fetch(`data/${key}.json`);
    DATA[key] = await r.json();
    return DATA[key];
  }

  // ---------- 출제 ----------
  // 창의 수학은 킨더팩토·키즈팩토를 마친 수준이라 레벨 2부터 시작
  const GROUP_WEIGHT = { 'kor-ant': 5, 'kor-syn': 5, 'kor-mimic': 5, 'kor-honor': 6, 'kor-conj': 6, 'kor-cho': 1.3, 'nat-wonder': 5, 'nat-sound': 3, 'nat-name': 0.4, 'nat-habitat': 0.5, 'nat-birth': 0.4, 'nat-food': 0.5 };
  const LEVEL_BOOST = { math: 1, nature: 1, korean: 1 };
  function maxLevel(key) { const n = S.solved[key] || 0; return Math.min(3, (n < 30 ? 1 : n < 90 ? 2 : 3) + (LEVEL_BOOST[key] || 0)); }
  function buildSession(key, d) {
    const items = d.items;
    const byId = Object.fromEntries(items.map(i => [i.id, i]));
    let seen = new Set(S.seen[key] || []);
    const out = [];
    const usedGroups = {};
    const usedAnswers = new Set();
    const ansKey = (it) => { const c = it.choices && it.choices[it.answer]; return typeof c === 'string' ? c : (c && (c.label || c.fallbackEmoji)) || it.id; };
    const push = (it, review) => { out.push({ item: it, review }); usedGroups[it.group] = (usedGroups[it.group] || 0) + 1; usedAnswers.add(ansKey(it)); };

    // 1) 복습: 틀린 문제 중 날짜가 된 것 (최대 3개)
    const due = Object.entries(S.wrong).filter(([id, w]) => w.subject === key && w.due <= today() && byId[id]).map(([id]) => byId[id]);
    shuffle(due).slice(0, 3).forEach(it => push(it, true));

    // 2) 생성기
    const gens = d.generators || [];
    const ng = GEN_SHARE[key] || 0;
    if (gens.length && ng) {
      const ml = maxLevel(key);
      const ok = gens.filter(g => g.level <= ml + 1);
      const bag = []; ok.forEach(g => { for (let i = 0; i < (g.weight || 1); i++) bag.push(g); });
      const chosen = [];
      for (let i = 0; i < ng && out.length + chosen.length < PER_DAY; i++) {
        let g = pick(bag), tries = 0;
        while (tries++ < 5 && chosen.filter(x => x === g).length >= 2) g = pick(bag);
        chosen.push(g);
      }
      chosen.forEach(g => out.push({ gen: g }));
    }

    // 3) 안 푼 문제 먼저 (레벨에 맞게, 같은 유형/같은 정답 겹치지 않게)
    let pool = items.filter(it => !seen.has(it.id));
    if (pool.length < PER_DAY - out.length) { // 다 풀었으면 다시 섞기
      S.seen[key] = []; seen = new Set(); pool = items.slice();
    }
    const ml = maxLevel(key);
    let lvPool = pool.filter(it => (it.level || 1) <= ml);
    if (lvPool.length < PER_DAY) lvPool = pool;
    // 많이 나왔으면 하는 유형은 더 자주 (자연: '왜? 어떻게?'·울음소리 ↑, 이름 맞히기 같은 기본 문제 ↓)
    const wOf = (it) => { const g = it.group || ''; for (const k in GROUP_WEIGHT) if (g.startsWith(k)) return GROUP_WEIGHT[k]; return 1; };
    const cand = lvPool.map(it => ({ it, k: Math.pow(Math.random(), 1 / wOf(it)) })).sort((a, b) => b.k - a.k).map(x => x.it);
    const groupCap = Math.max(2, Math.ceil(PER_DAY / 3));
    for (const pass of [0, 1]) {
      for (const it of cand) {
        if (out.length >= PER_DAY) break;
        if (out.some(o => o.item === it)) continue;
        if (pass === 0 && ((usedGroups[it.group] || 0) >= groupCap || usedAnswers.has(ansKey(it)))) continue;
        push(it, false);
      }
    }
    // 복습을 맨 앞에 몰지 않게 섞기
    return shuffle(out).slice(0, PER_DAY);
  }

  // 문제 한 개를 화면용으로 만들기 (보기 섞기, 오답 바꾸기, 생성기 실행)
  function materialize(entry, d) {
    const ctx = { coins: d.coins, objects: d.objects, goods: d.goods };
    let q;
    if (entry.gen) {
      q = window.GEN.G[entry.gen.gen](ctx);
      q.id = entry.gen.id; q.type = q.type || 'choice'; q.isGen = true;
    } else {
      const it = entry.item;
      if (it.type === 'word') q = { ...window.GEN.wordProblem(it, ctx), id: it.id, type: 'choice' };
      else if (it.type === 'shop') q = { ...window.GEN.shopProblem(it, ctx), id: it.id };
      else q = JSON.parse(JSON.stringify(it));
      q.type = q.type || 'choice';
      q.review = entry.review;
    }
    if (q.type === 'clockInput') { q._choices = []; return q; }
    // 오답 보기 바꾸기
    const isImg = q.type === 'imageChoice';
    let correct = q.choices[q.answer];
    let wrongs = q.choices.filter((_, i) => i !== q.answer);
    const poolW = isImg ? q.poolImages : q.pool;
    if (poolW && poolW.length >= 2 && !q.fixedOrder) {
      const keyOf = (c) => typeof c === 'string' ? c : (c.url || c.color || c.fallbackEmoji) + '|' + (c.label || '');
      const ck = keyOf(correct);
      const cand = shuffle(poolW.filter(c => keyOf(c) !== ck));
      const uniq = []; const seenK = new Set([ck]);
      for (const c of cand) { const k = keyOf(c); if (!seenK.has(k)) { seenK.add(k); uniq.push(c); } if (uniq.length >= wrongs.length) break; }
      if (uniq.length === wrongs.length) wrongs = uniq;
    }
    let choices = [correct, ...wrongs].map((c, i) => ({ c, ok: i === 0 }));
    if (!q.fixedOrder) choices = shuffle(choices);
    else choices = q.choices.map((c, i) => ({ c, ok: i === q.answer }));
    q._choices = choices;
    return q;
  }

  // ---------- 화면 ----------
  function show(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.toggle('active', s.id === id));
    window.scrollTo(0, 0);
  }
  function renderHome() {
    const t = S.daily[today()] || {};
    let total = 0; Object.values(t).forEach(v => total += v.done);
    $('#todayCount').textContent = total;
    $('#starCount').textContent = S.stars;
    const tiles = $('#tiles'); tiles.innerHTML = '';
    for (const s of SUBJECTS) {
      const b = document.createElement('button');
      b.className = 'tile';
      const dd = t[s.key];
      const done = dd ? Math.min(dd.done, PER_DAY) : 0;
      if (s.draw) {
        b.innerHTML = `<div class="ic">${s.icon}</div><div class="nm">${s.name}</div><div class="sub">자유롭게 그려요</div>`;
        b.onclick = () => { show('draw'); window.DRAW && window.DRAW.open(); };
      } else {
        if (dd && dd.done >= PER_DAY) b.classList.add('done');
        b.innerHTML = `<div class="ic">${s.icon}</div><div class="nm">${s.name}</div><div class="sub">${done} / ${PER_DAY}문제 ${dd && dd.stars ? '· ⭐' + dd.stars : ''}</div><div class="bar"><i style="width:${done * 10}%"></i></div>`;
        b.onclick = () => startSubject(s.key);
      }
      tiles.appendChild(b);
    }
  }

  let cur = null; // {key, d, list, idx, q, tries, stars}
  async function startSubject(key) {
    speak('');
    const d = await loadSubject(key);
    const list = buildSession(key, d);
    const dd = day(key);
    const startIdx = dd.done % PER_DAY; // 중간에 나갔다 오면 이어서 (새 문제로)
    cur = { key, d, list, idx: dd.done >= PER_DAY ? 0 : startIdx, stars: 0, base: dd.done >= PER_DAY ? 0 : startIdx, extra: dd.done >= PER_DAY };
    cur.list = list;
    show('quiz');
    nextQuestion(true);
  }

  function setProgress() {
    const n = cur.idx + 1;
    $('#progressFill').style.width = `${n * 10}%`;
    $('#progressText').textContent = `${n} / ${PER_DAY}`;
    $('#quizStars').textContent = S.stars;
  }

  function imgEl(im, cls = '') {
    const wrap = document.createElement('div');
    wrap.className = 'photo ' + cls + (im.flag ? ' flag' : '');
    if (im.color) { wrap.innerHTML = `<div class="swatch" style="background:${im.color}"></div>`; wrap.style.background = 'transparent'; return wrap; }
    if (im.url) {
      const i = new Image();
      i.alt = ''; i.decoding = 'async';
      i.onerror = () => {
        if (im.remote && i.src.indexOf(im.remote) < 0 && !i.dataset.tried) { i.dataset.tried = 1; i.src = im.remote; return; }
        wrap.innerHTML = `<div class="emoji">${im.fallbackEmoji || '❓'}</div>`;
      };
      if (im.zoom) { wrap.classList.add('zoom'); i.style.transform = `scale(${im.zoom.scale})`; i.style.transformOrigin = `${im.zoom.x}% ${im.zoom.y}%`; }
      i.src = im.url;
      wrap.appendChild(i);
    } else {
      wrap.innerHTML = `<div class="emoji">${im.fallbackEmoji || '❓'}</div>`;
    }
    return wrap;
  }
  function thumbHTML(c) {
    if (c.color) return `<div class="thumb"><div class="sw" style="background:${c.color};border:3px solid #eee;border-radius:12px"></div></div>`;
    if (c.url) return `<div class="thumb ${c.flag ? 'flag' : ''}"><img src="${c.url}" alt="" data-remote="${c.remote || ''}" data-fb="${c.fallbackEmoji || '❓'}" onerror="if(this.dataset.remote&&this.src!==this.dataset.remote){this.src=this.dataset.remote;this.dataset.remote=''}else{this.parentNode.innerHTML=this.dataset.fb}"></div>`;
    return `<div class="thumb">${c.fallbackEmoji || '❓'}</div>`;
  }

  function nextQuestion(first) {
    stopAll();
    if (!first) cur.idx++;
    if (cur.idx >= PER_DAY || cur.idx - cur.base >= cur.list.length) return finish();
    const entry = cur.list[cur.idx - cur.base];
    let q;
    try { q = materialize(entry, cur.d); } catch (e) { console.error(e); cur.list.splice(cur.idx - cur.base, 1); return nextQuestion(true); }
    cur.q = q; cur.tries = 0; cur.answered = false;
    setProgress();
    renderQuestion(q);
    preloadNext();
  }
  function preloadNext() {
    const e = cur.list[cur.idx - cur.base + 1];
    if (!e || !e.item) return;
    const urls = [];
    const it = e.item;
    if (it.image && it.image.url) urls.push(it.image.url);
    (it.choices || []).forEach(c => c && c.url && urls.push(c.url));
    urls.forEach(u => { const i = new Image(); i.src = u; });
  }

  function renderQuestion(q) {
    $('#prompt').innerHTML = (q.review ? '🔁 복습! ' : '') + emphasize(q.prompt);
    const media = $('#media'); media.innerHTML = '';
    const fb = $('#feedback'); fb.className = 'feedback'; fb.innerHTML = '';
    $('#nextBtn').classList.add('hidden');
    if (q.image && q.type !== 'sort') media.appendChild(imgEl(q.image));
    if (q.display) {
      const d = document.createElement('div');
      d.className = 'display' + (q.display.length > 12 ? ' sentence' : '') + (q.display.length <= 2 ? ' huge' : '') + (/^[一-鿿]+$/.test(q.display) || q.hanja ? ' hanja' : '');
      if (q.displayClass) d.classList.add(q.displayClass);
      if (q.displayLang) d.lang = q.displayLang;
      d.textContent = q.display;
      if (q.displayLang && q.displayLang.startsWith('en')) d.style.fontFamily = '"Comic Sans MS","Chalkboard SE",system-ui,sans-serif';
      media.appendChild(d);
    }
    if (q.dots) { const d = document.createElement('div'); d.className = 'dots'; d.textContent = '●'.repeat(q.dots); media.appendChild(d); }
    if (q.html) { const d = document.createElement('div'); d.innerHTML = q.html; media.appendChild(d); }
    if (q.hanjaHint) {
      const card = hanjaHintCard(q.hanjaHint);
      if (q.showHint) media.appendChild(card);
      else { card.classList.add('hidden'); addHintButton(media, () => { card.classList.remove('hidden'); speak(q.hanjaHint.story); }); media.appendChild(card); }
    } else if (q.hint) {
      const box = document.createElement('div'); box.className = 'hint-text hidden'; box.textContent = '💡 ' + q.hint;
      addHintButton(media, () => { box.classList.remove('hidden'); speak(q.hint); });
      media.appendChild(box);
    }
    if (q.sound) {
      const b = document.createElement('button'); b.className = 'play-btn' + (q.soundAfter ? ' small' : ''); b.textContent = q.soundAfter ? '🎵 소리 들어 보기' : '🔊 소리 듣기';
      b.onclick = () => playSound(q.sound.url); media.appendChild(b);
    }
    if (q.sayWord && q.listenOnly) {
      const b = document.createElement('button'); b.className = 'play-btn'; b.textContent = '🔊 다시 듣기';
      b.onclick = () => speak([{ text: q.sayWord.text, lang: q.sayWord.lang }]); media.appendChild(b);
    }
    if (!media.children.length) media.style.margin = '4px 0'; else media.style.margin = '';

    const box = $('#choices'); box.innerHTML = '';
    box.className = 'choices';
    if (q.type === 'sort') return renderSort(q, media, box);
    if (q.type === 'clockInput') return renderClockInput(q, box);
    const isImg = q.type === 'imageChoice';
    if (isImg) box.classList.add('img');
    if (q.clocks) box.classList.add('clocks');
    else if (q._choices.length === 3 && q._choices.every(c => String(c.c).length <= 3)) { box.classList.add('grid3'); if (q._choices.some(c => String(c.c).length === 3)) box.classList.add('g3long'); }
    else if (q._choices.length === 2 && q._choices.every(c => String(c.c).length <= 8)) box.classList.add('two');
    q._choices.forEach((ch, i) => {
      const b = document.createElement('button');
      b.className = 'choice';
      if (isImg) {
        b.innerHTML = thumbHTML(ch.c) + (ch.c.label ? `<small>${ch.c.label}</small>` : '');
      } else {
        const text = String(ch.c) + (q.suffix && /^\d[\d,]*$/.test(String(ch.c)) ? q.suffix : '');
        b.textContent = text;
        if (q.big) b.classList.add('big');
        if (q.choiceLang && q.choiceLang.startsWith('en')) b.classList.add('en');
        if (q.speakChoices && !q.choiceLang) {
          const s = document.createElement('span'); s.className = 'say'; s.textContent = '🔈';
          s.onclick = (e) => { e.stopPropagation(); speak(text); };
          b.appendChild(s);
        }
      }
      b.onclick = () => answer(b, ch, i);
      box.appendChild(b);
    });
    speakQuestion(q);
  }

  function addHintButton(media, onShow) {
    const b = document.createElement('button'); b.className = 'hint-btn'; b.textContent = '💡 힌트 볼래요';
    b.onclick = () => { b.remove(); onShow(); };
    media.appendChild(b);
  }
  function hanjaHintCard(h) {
    const d = document.createElement('div'); d.className = 'hanja-hint';
    let anc = '';
    if (h.ancient && (h.ancient.url || h.ancient.remote)) anc = `<span class="arrow">➜</span><span class="anc"><img src="${h.ancient.url}" alt="옛 글자" onerror="this.parentNode.previousSibling.remove();this.parentNode.remove()"><small>옛날 글자</small></span>`;
    d.innerHTML = `<div class="row"><span class="pic">${h.emoji}</span>${anc}</div><p>${esc(h.story)}</p>`;
    return d;
  }
  function speakQuestion(q) {
    const parts = [{ text: q.speak || q.prompt, lang: 'ko-KR' }];
    if (q.hanjaHint && q.showHint) parts.push({ text: '힌트! ' + q.hanjaHint.story, lang: 'ko-KR' });
    if (q.sayWord) parts.push({ text: q.sayWord.text, lang: q.sayWord.lang });
    if (q.display && !q.sayWord && !q.speak && /[一-鿿]/.test(q.display) === false && q.subject !== '국어' && q.display.length > 1) parts.push({ text: mathSpeech(q.display), lang: 'ko-KR' });
    if (q.speakChoices && q.type === 'choice') q._choices.forEach(c => parts.push({ text: String(c.c), lang: q.choiceLang || 'ko-KR' }));
    if (q.sound && !q.soundAfter) { speak(parts); const wait = setInterval(() => { if (!speechSynthesis.speaking) { clearInterval(wait); if (cur && cur.q === q) playSound(q.sound.url); } }, 300); setTimeout(() => clearInterval(wait), 15000); return; }
    speak(parts);
  }

  function answer(btn, ch, i) {
    if (cur.answered) return;
    const q = cur.q;
    const fb = $('#feedback');
    if (ch.ok) {
      cur.answered = true;
      btn.classList.add('correct');
      chime(true);
      const msg = pick(PRAISE);
      fb.className = 'feedback ok'; fb.innerHTML = msg + (q.explain ? `<span class="explain">${q.explain}</span>` : '');
      const firstTry = cur.tries === 0;
      record(true, firstTry);
      flyStar();
      sayPhrase(msg);
      if (q.choiceLang && typeof ch.c === 'string') setTimeout(() => speak([{ text: ch.c, lang: q.choiceLang }], { cancel: false }), 50);
      $('#nextBtn').classList.remove('hidden');
      document.querySelectorAll('#choices .choice').forEach(b => b.disabled = true);
    } else {
      cur.tries++;
      btn.classList.add('wrong'); btn.disabled = true;
      chime(false);
      if (cur.tries === 1) {
        const msg = pick(RETRY);
        fb.className = 'feedback no'; fb.textContent = msg; sayPhrase(msg);
      } else {
        cur.answered = true;
        const idx = q._choices.findIndex(c => c.ok);
        const right = document.querySelectorAll('#choices .choice')[idx];
        if (right) right.classList.add('correct');
        const msg = pick(SHOW);
        fb.className = 'feedback no'; fb.innerHTML = msg + (q.explain ? `<span class="explain">${q.explain}</span>` : '');
        sayPhrase(msg);
        record(false, false);
        $('#nextBtn').classList.remove('hidden');
        document.querySelectorAll('#choices .choice').forEach(b => b.disabled = true);
      }
    }
  }

  function record(ok, firstTry) {
    const q = cur.q, key = cur.key;
    const dd = day(key);
    dd.done++;
    if (ok) { dd.correct++; dd.stars++; S.stars++; cur.stars++; }
    S.solved[key] = (S.solved[key] || 0) + 1;
    if (!q.isGen) {
      S.seen[key] = S.seen[key] || [];
      if (!S.seen[key].includes(q.id)) S.seen[key].push(q.id);
      if (!ok || !firstTry) S.wrong[q.id] = { subject: key, due: addDays(!ok ? 2 : 4), n: ((S.wrong[q.id] || {}).n || 0) + 1 };
      else if (S.wrong[q.id] && q.review) delete S.wrong[q.id]; // 복습에서 맞히면 졸업
    }
    save();
    $('#quizStars').textContent = S.stars;
  }

  function flyStar() {
    const s = $('#starFly'); s.classList.remove('go'); void s.offsetWidth; s.classList.add('go');
  }

  function finish() {
    const dd = day(cur.key);
    show('done');
    const t = pick(DONE);
    $('#doneTitle').textContent = t;
    const subj = SUBJECTS.find(s => s.key === cur.key);
    $('#doneText').textContent = `${subj.name} 10문제 중에 ${Math.min(dd.correct, dd.done)}문제를 맞혔어요!`;
    $('#doneStars').textContent = '⭐'.repeat(Math.max(cur.stars, 0));
    sayPhrase(t);
    confetti();
  }
  function confetti() {
    const c = $('#confetti'); c.innerHTML = '';
    const em = ['⭐', '🎉', '🌸', '💖', '🎈', '✨'];
    for (let i = 0; i < 40; i++) {
      const e = document.createElement('i'); e.textContent = pick(em);
      e.style.left = Math.random() * 100 + 'vw'; e.style.animationDuration = 2 + Math.random() * 2.5 + 's'; e.style.animationDelay = Math.random() * 1.2 + 's';
      c.appendChild(e);
    }
    setTimeout(() => c.innerHTML = '', 6000);
  }

  // ---------- 시계: 시·분 직접 고르기 ----------
  function renderClockInput(q, box) {
    box.className = 'clock-input';
    const mLabel = (m) => m === 0 ? '정각' : m + '분';
    box.innerHTML = `<div class="ci-read"><b id="ciH">?</b>시 <b id="ciM">?</b></div>
      <div class="ci-label">짧은바늘 👉 몇 시?</div><div class="ci-row hours">${Array.from({ length: 12 }, (_, i) => `<button class="ci" data-h="${i + 1}">${i + 1}</button>`).join('')}</div>
      <div class="ci-label">긴바늘 👉 몇 분?</div><div class="ci-row mins ${q.minutes.length > 4 ? 'many' : ''}">${q.minutes.map(m => `<button class="ci" data-m="${m}">${mLabel(m)}</button>`).join('')}</div>
      <button class="next-btn ci-ok" disabled>확인 ✔</button>`;
    let sh = null, sm = null;
    const ok = box.querySelector('.ci-ok');
    const upd = () => {
      box.querySelectorAll('[data-h]').forEach(b => b.classList.toggle('sel', +b.dataset.h === sh));
      box.querySelectorAll('[data-m]').forEach(b => b.classList.toggle('sel', +b.dataset.m === sm));
      $('#ciH').textContent = sh == null ? '?' : sh;
      $('#ciM').textContent = sm == null ? '?' : (sm === 0 ? '정각' : sm + '분');
      ok.disabled = sh == null || sm == null || cur.answered;
    };
    box.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { if (cur.answered) return; sh = +b.dataset.h; b.classList.remove('wrong'); upd(); speak(sh + '시'); });
    box.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { if (cur.answered) return; sm = +b.dataset.m; b.classList.remove('wrong'); upd(); speak(mLabel(sm)); });
    ok.onclick = () => {
      if (cur.answered || sh == null || sm == null) return;
      const okH = sh === q.h, okM = sm === q.m, fb = $('#feedback');
      const ansTxt = `${q.h}시` + (q.m ? ` ${q.m}분` : '');
      const explain = `짧은바늘은 ${q.h}${q.m ? ' 근처' : ''}, 긴바늘은 ${q.m === 0 ? 12 : q.m / 5}에 있어요. 그래서 ${ansTxt}!`;
      const finish = (right) => {
        cur.answered = true;
        box.querySelectorAll('.ci').forEach(b => b.disabled = true); ok.classList.add('hidden');
        box.querySelector(`[data-h="${q.h}"]`).classList.add('correct'); box.querySelector(`[data-m="${q.m}"]`).classList.add('correct');
        $('#nextBtn').classList.remove('hidden');
        const msg = right ? pick(PRAISE) : pick(SHOW);
        fb.className = 'feedback ' + (right ? 'ok' : 'no'); fb.innerHTML = msg + `<span class="explain">${right ? '' : '정답: ' + ansTxt + '. '}${explain}</span>`;
        sayPhrase(msg);
      };
      if (okH && okM) { chime(true); const first = cur.tries === 0; record(true, first); flyStar(); return finish(true); }
      cur.tries++; chime(false);
      if (cur.tries === 1) {
        if (!okH) { box.querySelector(`[data-h="${sh}"]`).classList.add('wrong'); sh = null; }
        if (!okM) { box.querySelector(`[data-m="${sm}"]`).classList.add('wrong'); sm = null; }
        const msg = okH ? '시는 맞았어요! 긴바늘을 다시 볼까요?' : okM ? '분은 맞았어요! 짧은바늘을 다시 볼까요?' : pick(RETRY);
        fb.className = 'feedback no'; fb.textContent = msg; sayPhrase(msg); upd();
        return;
      }
      record(false, false); finish(false);
    };
    upd();
    speakQuestion(q);
  }

  // ---------- 분리수거: 끌어다 놓기 ----------
  function renderSort(q, media, box) {
    const item = imgEl(q.image || { fallbackEmoji: '🗑️' }, 'sort-item');
    media.appendChild(item);
    const hint = document.createElement('div'); hint.className = 'sort-hint'; hint.textContent = '👆 그림을 알맞은 통으로 끌어다 놓거나, 통을 눌러요';
    media.appendChild(hint);
    box.className = 'bins';
    const bins = [];
    q._choices.forEach((ch, i) => {
      const b = document.createElement('button');
      b.className = 'bin choice';
      const ic = (q.binIcons || {})[ch.c] || '🗑️';
      b.innerHTML = `<span class="bi">${ic}</span>${ch.c}`;
      b.onclick = () => answer(b, ch, i);
      box.appendChild(b); bins.push({ b, ch, i });
    });
    // 드래그
    let sx, sy, dragging = false;
    item.addEventListener('pointerdown', (e) => {
      if (cur.answered) return;
      dragging = true; sx = e.clientX; sy = e.clientY; item.setPointerCapture(e.pointerId); item.classList.add('dragging');
    });
    item.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      item.style.transform = `translate(${e.clientX - sx}px, ${e.clientY - sy}px) scale(.6)`;
      bins.forEach(({ b }) => { const r = b.getBoundingClientRect(); b.classList.toggle('hover', e.clientX > r.left && e.clientX < r.right && e.clientY > r.top && e.clientY < r.bottom); });
    });
    const end = (e) => {
      if (!dragging) return;
      dragging = false; item.classList.remove('dragging'); item.style.transform = '';
      const hit = bins.find(({ b }) => { const r = b.getBoundingClientRect(); return e.clientX > r.left && e.clientX < r.right && e.clientY > r.top && e.clientY < r.bottom; });
      bins.forEach(({ b }) => b.classList.remove('hover'));
      if (hit && !hit.b.disabled) answer(hit.b, hit.ch, hit.i);
    };
    item.addEventListener('pointerup', end); item.addEventListener('pointercancel', end);
    speakQuestion(q);
  }

  // ---------- 출처 ----------
  async function renderCredits() {
    show('credits');
    const body = $('#creditsBody'); body.textContent = '불러오는 중…';
    const parts = [];
    let sounds = {};
    try { sounds = await (await fetch('assets/sounds/sounds.json')).json(); } catch (e) {}
    for (const s of SUBJECTS.filter(s => !s.draw)) {
      const d = await loadSubject(s.key);
      const seen = new Map();
      const walk = (o) => { if (!o || typeof o !== 'object') return; if (Array.isArray(o)) return o.forEach(walk); if (o.credit && (o.url || o.remote)) seen.set(o.source || o.url, o); Object.values(o).forEach(walk); };
      walk(d);
      if (!seen.size) continue;
      parts.push(`<h3>${s.icon} ${s.name} — 사진 ${seen.size}장</h3><ul>` + [...seen.values()].map(o => `<li>${esc(o.credit)}${o.source ? ` · <a href="${o.source}" target="_blank" rel="noopener">원본</a>` : ''}</li>`).join('') + '</ul>');
    }
    const sl = Object.entries(sounds);
    if (sl.length) parts.push(`<h3>🔊 소리 ${sl.length}개</h3><ul>` + sl.map(([k, v]) => `<li>${esc(k.split(':')[1])}: ${esc(v.credit)}${v.source ? ` · <a href="${v.source}" target="_blank" rel="noopener">원본</a>` : ''}</li>`).join('') + '</ul>');
    body.innerHTML = '<p>이 앱의 사진과 소리는 위키미디어 커먼즈 등에서 자유 이용 허락(퍼블릭 도메인, CC0, CC BY, CC BY-SA)된 자료를 사용했어요. 만든 분들께 감사드려요!</p>' + parts.join('');
  }
  // 문제 속 중요한 말(아닌 것, 맞는 것, 틀린 것 …)은 굵게 + 밑줄
  const KEY = /(나오지 않는|아니요|아닌|아니|맞는|맞으면|틀린|틀리게|틀리면|틀려요|잘못|바른|바르게|바로 뒤|바로 앞|더 큰|더 작은|더 긴|더 짧은|더 무거운|더 가벼운|더 비싼|더 싼|더 많|안 좋은|좋은 행동|아프게 하는|않은)/g;
  function emphasize(t) { return esc(t).replace(KEY, '<b class="em">$1</b>'); }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  // ---------- 부모님 메뉴 ----------
  function renderParents() {
    show('parents');
    const days = Object.keys(S.daily).sort().reverse().slice(0, 14);
    let rows = '';
    for (const dt of days) {
      const v = S.daily[dt]; let done = 0, ok = 0;
      const subs = Object.entries(v).map(([k, x]) => { done += x.done; ok += x.correct; return `${(SUBJECTS.find(s => s.key === k) || {}).name || k} ${x.correct}/${x.done}`; }).join(', ');
      rows += `<tr><td>${dt}</td><td>${ok}/${done}</td><td style="font-size:13px">${subs}</td></tr>`;
    }
    const wrongN = Object.keys(S.wrong).length;
    $('#parentsBody').innerHTML = `
      <p>모은 별: <b>${S.stars}</b>개 · 복습 대기 문제: <b>${wrongN}</b>개</p>
      <p>과목별로 푼 문제: ${SUBJECTS.filter(s => !s.draw).map(s => `${s.name} ${(S.seen[s.key] || []).length}`).join(' · ')}</p>
      <table><tr><th>날짜</th><th>맞힘</th><th>과목</th></tr>${rows || '<tr><td colspan=3>아직 기록이 없어요</td></tr>'}</table>
      <p style="margin-top:14px;font-size:14px;color:#8a7a72">문제는 <code>data/과목.json</code> 파일에 들어 있어요. 파일을 고치면 바로 반영돼요.</p>
      <h3 style="margin:14px 0 4px">🔊 목소리</h3>
      <p style="font-size:14px;color:#8a7a72;margin:0 0 6px">목소리는 휴대폰에 설치된 음성을 써요. 'Google' 또는 '자연스러운(Natural)' 음성이 가장 부드러워요.</p>
      <label>한국어 <select id="voiceKo"></select></label><br>
      <label>영어 <select id="voiceEn"></select></label><br>
      <label>빠르기 <select id="speechRate"><option value="0.85">천천히</option><option value="1">보통</option><option value="1.15">조금 빠르게</option></select></label><br>
      <button id="testVoice">🔊 음성 테스트</button>
      <button id="resetToday">오늘 기록 지우기</button>
      <button id="resetAll">전체 기록 지우기</button>`;
    const fill = (sel, base) => {
      const vs = voices.filter(v => v.lang.toLowerCase().startsWith(base));
      const cur = voiceFor(base === 'ko' ? 'ko-KR' : 'en-US');
      sel.innerHTML = vs.length ? vs.map(v => `<option ${cur && v.name === cur.name ? 'selected' : ''}>${esc(v.name)}</option>`).join('') : '<option>기본 음성</option>';
      sel.onchange = () => { S.voice = S.voice || {}; S.voice[base] = sel.value; save(); speak([{ text: base === 'ko' ? '시은아, 안녕!' : 'Hello, Sieun!', lang: base === 'ko' ? 'ko-KR' : 'en-US' }]); };
    };
    fill($('#voiceKo'), 'ko'); fill($('#voiceEn'), 'en');
    $('#speechRate').value = String(S.speechRate || 1);
    $('#speechRate').onchange = (e) => { S.speechRate = +e.target.value; save(); speak('이 빠르기로 읽어 줄게요.'); };
    $('#testVoice').onclick = () => speak([{ text: '시은아, 안녕! 오늘도 같이 공부하자!' }, { text: 'Hello, Sieun!', lang: 'en-US' }]);
    $('#resetToday').onclick = () => { if (confirm('오늘 기록을 지울까요?')) { delete S.daily[today()]; save(); renderParents(); } };
    $('#resetAll').onclick = () => { if (confirm('정말 모든 기록(별, 푼 문제)을 지울까요?')) { localStorage.removeItem(STORE_KEY); load(); renderParents(); } };
  }

  // ---------- 연결 ----------
  function init() {
    load();
    renderHome();
    $('#quizHome').onclick = () => { stopAll(); renderHome(); show('home'); };
    $('#speakBtn').onclick = () => cur && cur.q && speakQuestion(cur.q);
    $('#nextBtn').onclick = () => nextQuestion(false);
    $('#doneHome').onclick = () => { stopAll(); renderHome(); show('home'); };
    $('#doneMore').onclick = () => { const k = cur.key; startExtra(k); };
    $('#openCredits').onclick = renderCredits;
    $('#openParents').onclick = renderParents;
    document.querySelectorAll('[data-home]').forEach(b => b.onclick = () => { stopAll(); renderHome(); show('home'); });
    window.addEventListener('popstate', () => { renderHome(); show('home'); });
  }
  async function startExtra(key) {
    const d = await loadSubject(key);
    cur = { key, d, list: buildSession(key, d), idx: 0, base: 0, stars: 0, extra: true };
    show('quiz'); nextQuestion(true);
  }
  // 테스트용
  // 미리보기용: 특정 문제 하나 띄우기 (예: APP.preview('hanja', 'han-078'))
  async function preview(key, id) {
    const d = await loadSubject(key);
    const it = d.items.find(x => x.id === id) || (d.generators || []).find(g => g.id === id);
    cur = { key, d, list: [it.gen ? { gen: it } : { item: it }], idx: 0, base: 0, stars: 0, extra: true };
    show('quiz'); nextQuestion(true);
  }
  window.APP = { buildSession, materialize, loadSubject, SUBJECTS, preview, get state() { return S; } };
  init();
})();
