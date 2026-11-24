/* 문제 생성기: 수학 · 가게 · 한자 숫자.  매번 새 숫자로 문제를 만든다. */
(function () {
  const R = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const fmt = (n) => n.toLocaleString('ko-KR');

  // 흔한 실수로 오답 만들기
  function numChoices(ans, mistakes, min = 0) {
    const set = new Set([ans]);
    for (const m of shuffle(mistakes)) { if (set.size >= 3) break; if (m >= min && m !== ans && Number.isInteger(m)) set.add(m); }
    let k = 1;
    while (set.size < 3) { const c = ans + (k % 2 ? 1 : -1) * Math.ceil(k / 2); if (c >= min) set.add(c); k++; }
    return { choices: [...set].map(String), answer: 0 };
  }
  function batchim(word) { const c = String(word).slice(-1).charCodeAt(0); if (c >= 0xac00 && c <= 0xd7a3) return (c - 0xac00) % 28 !== 0; return /[013678]$/.test(String(word)); }
  const J = (w, a, b) => w + (batchim(w) ? a : b);

  // 시은이 또는 또래 친구 (문장에 나이·형제·숙제가 나와도 자연스럽게)
  function person() {
    if (Math.random() < 0.5) return { 가: '시은이가', 는: '시은이는', 의: '시은이의', 랑: '시은이랑', 에게: '시은이에게', 보다: '시은이보다', 까지: '시은이까지', 를: '시은이를' };
    const p = pick(['민지', '준호', '하린', '도윤', '서아', '지호']);
    const n = batchim(p) ? p + '이' : p;  // 하린 → 하린이
    return { 가: n + '가', 는: n + '는', 의: n + '의', 랑: n + '랑', 에게: n + '에게', 보다: n + '보다', 까지: n + '까지', 를: n + '를' };
  }

  // ---------- SVG 도우미 ----------
  function clockSVG(h, m) {
    const ha = ((h % 12) + m / 60) * 30, ma = m * 6;
    let ticks = '';
    for (let i = 1; i <= 12; i++) {
      const a = (i * 30 - 90) * Math.PI / 180;
      ticks += `<text x="${100 + 72 * Math.cos(a)}" y="${100 + 72 * Math.sin(a) + 8}" font-size="22" text-anchor="middle" fill="#3b2f2f">${i}</text>`;
    }
    return `<svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="94" fill="#fff" stroke="#ff8fab" stroke-width="8"/>${ticks}
      <line x1="100" y1="100" x2="${100 + 45 * Math.sin(ha * Math.PI / 180)}" y2="${100 - 45 * Math.cos(ha * Math.PI / 180)}" stroke="#3b2f2f" stroke-width="9" stroke-linecap="round"/>
      <line x1="100" y1="100" x2="${100 + 68 * Math.sin(ma * Math.PI / 180)}" y2="${100 - 68 * Math.cos(ma * Math.PI / 180)}" stroke="#e2577e" stroke-width="5" stroke-linecap="round"/>
      <circle cx="100" cy="100" r="7" fill="#3b2f2f"/></svg>`;
  }
  const SHAPES = {
    '동그라미': (x, y, c) => `<circle cx="${x}" cy="${y}" r="17" fill="${c}"/>`,
    '세모': (x, y, c) => `<polygon points="${x},${y - 19} ${x - 19},${y + 15} ${x + 19},${y + 15}" fill="${c}"/>`,
    '네모': (x, y, c) => `<rect x="${x - 16}" y="${y - 16}" width="32" height="32" rx="3" fill="${c}"/>`,
    '별': (x, y, c) => { let p = ''; for (let i = 0; i < 10; i++) { const r = i % 2 ? 8 : 19, a = (i * 36 - 90) * Math.PI / 180; p += `${x + r * Math.cos(a)},${y + r * Math.sin(a)} `; } return `<polygon points="${p}" fill="${c}"/>`; },
  };
  const COLORS = ['#ff6b6b', '#4cc38a', '#6aa9ff', '#ffb703', '#b388eb'];

  // ---------- 수학 ----------
  const G = {};
  G.split10 = () => {
    const n = R(5, 10), a = R(1, n - 1), b = n - a;
    if (Math.random() < 0.5) {
      return { prompt: `${n}${batchim(n) ? '은' : '는'} ${a}${batchim(a) ? '과' : '와'} 몇으로 가를 수 있을까요?`, display: `${n} → ${a} 와 □`, ...numChoices(b, [b + 1, b - 1, n, a]) };
    }
    return { prompt: `${a}${batchim(a) ? '과' : '와'} 몇을 모으면 ${n}${batchim(n) ? '이' : '가'} 될까요?`, display: `${a} + □ = ${n}`, ...numChoices(b, [b + 1, b - 1, n + a]) };
  };
  G.add10 = () => { const a = R(1, 8), b = R(1, 9 - a + 1); const s = a + b; return { prompt: '덧셈을 해 봐요.', display: `${a} + ${b} = □`, ...numChoices(s, [s + 1, s - 1, Math.abs(a - b)]) }; };
  G.sub10 = () => { const a = R(3, 10), b = R(1, a - 1); const s = a - b; return { prompt: '뺄셈을 해 봐요.', display: `${a} − ${b} = □`, ...numChoices(s, [s + 1, s - 1, a + b]) }; };
  G.add20 = () => {
    const a = R(3, 9), b = R(11 - a, 9), s = a + b;
    const p = person();
    const pr = Math.random() < 0.4 ? `${p.가} 받아올림 덧셈에 도전해요!` : '받아올림이 있는 덧셈이에요.';
    return { prompt: pr, display: `${a} + ${b} = □`, ...numChoices(s, [s - 10, s + 1, s - 1, s + 10]) };
  };
  G.sub20 = () => {
    const a = R(11, 18), u = a % 10, b = R(u + 1, 9), s = a - b;
    return { prompt: '받아내림이 있는 뺄셈이에요.', display: `${a} − ${b} = □`, ...numChoices(s, [10 + (b - u), s + 1, s - 1, s + 10]) };
  };
  G.add2d = () => {
    const t = R(1, 8), u = R(0, 9), b = R(1, 9), a = t * 10 + u, s = a + b;
    return { prompt: '두 자리 수 더하기 한 자리 수!', display: `${a} + ${b} = □`, ...numChoices(s, [s - 10, s + 10, s + 1, s - 1, t * 10 + ((u + b) % 10)]) };
  };
  G.sub2d = () => {
    const t = R(2, 9), u = R(0, 9), b = R(1, 9), a = t * 10 + u, s = a - b;
    return { prompt: '두 자리 수 빼기 한 자리 수!', display: `${a} − ${b} = □`, ...numChoices(s, [s + 10, s - 10, s + 1, s - 1, t * 10 + Math.abs(u - b)]) };
  };
  G.blank = () => {
    const kind = R(0, 3), a = R(2, 9), b = R(2, 9), s = a + b;
    if (kind === 0) return { prompt: '□ 안에 알맞은 수는?', display: `${a} + □ = ${s}`, ...numChoices(b, [s, b + 1, b - 1, s + a]) };
    if (kind === 1) return { prompt: '□ 안에 알맞은 수는?', display: `□ + ${b} = ${s}`, ...numChoices(a, [s, a + 1, a - 1]) };
    if (kind === 2) return { prompt: '□ 안에 알맞은 수는?', display: `${s} − □ = ${a}`, ...numChoices(b, [s + a, b + 1, b - 1]) };
    return { prompt: '□ 안에 알맞은 수는?', display: `□ − ${b} = ${a}`, ...numChoices(s, [a - b > 0 ? a - b : s + 2, s + 1, s - 1]) };
  };
  G.tens = () => {
    const t = R(1, 9), u = R(0, 9), n = t * 10 + u;
    let html = '<div class="obj-grid">';
    for (let i = 0; i < t; i++) html += '<div class="obj" style="width:28px;height:70px;font-size:12px;flex-direction:column;background:#ffe3ec">' + '🟥'.repeat(1) + '<b>10</b></div>';
    html += '<span class="plus"></span>';
    for (let i = 0; i < u; i++) html += '<div class="obj" style="width:30px;height:30px;font-size:22px">🟥</div>';
    html += '</div>';
    return { prompt: `10개씩 묶음 ${t}개와 낱개 ${u}개는 모두 몇일까요?`, html, ...numChoices(n, [u * 10 + t, n + 10, n - 10, t + u]) };
  };
  const PAT_SETS = [['🍎', '🍌'], ['⭐', '🌙'], ['🔴', '🔵'], ['🐶', '🐱', '🐰'], ['▲', '●'], ['🍓', '🍇', '🍋'], ['🟥', '🟨', '🟦'], ['🌸', '🍀']];
  G.pattern = () => {
    const set = pick(PAT_SETS);
    const unitLens = set.length === 2 ? [[0, 1], [0, 1, 1], [0, 0, 1], [0, 1, 0, 1, 1]] : [[0, 1, 2], [0, 1, 1, 2], [0, 0, 1, 2]];
    const unit = pick(unitLens).map(i => set[i]);
    const len = unit.length * 2 + R(1, unit.length);
    const seq = []; for (let i = 0; i < len; i++) seq.push(unit[i % unit.length]);
    const ans = unit[len % unit.length];
    const others = shuffle(set.filter(s => s !== ans).concat(['💜', '🟢', '🍉', '🐻'].filter(x => !set.includes(x)))).slice(0, 2);
    return { prompt: '규칙을 찾아봐요! ? 에 들어갈 것은?', html: `<div class="dots" style="font-size:36px">${seq.join(' ')} ❓</div>`, choices: [ans, ...others], answer: 0, big: true };
  };
  G.numpattern = () => {
    const step = pick([1, 2, 5, 10, 3, -1, -2, -10]), start = step < 0 ? R(30, 60) : R(1, 20);
    const seq = [0, 1, 2, 3].map(i => start + i * step), ans = start + 4 * step;
    return { prompt: '수의 규칙을 찾아봐요. □ 에 알맞은 수는?', display: seq.join(', ') + ', □', ...numChoices(ans, [ans + step, ans - step, ans + 1, ans - 1]) };
  };
  G.grid = () => {
    const base = R(0, 8) * 10 + 1, col = R(0, 6);
    const rows = [0, 1, 2].map(r => [0, 1, 2, 3].map(c => base + r * 10 + col + c));
    const qr = R(0, 2), qc = R(0, 3), ans = rows[qr][qc];
    let html = '<table class="grid-table">';
    rows.forEach((row, r) => { html += '<tr>' + row.map((v, c) => r === qr && c === qc ? '<td class="q">?</td>' : `<td>${v}</td>`).join('') + '</tr>'; });
    html += '</table>';
    return { prompt: '수 배열표에서 ? 에 들어갈 수는?', html, ...numChoices(ans, [ans + 10, ans - 10, ans + 1, ans - 1]) };
  };
  G.count = () => {
    const names = Object.keys(SHAPES), target = pick(names);
    const items = []; const n = R(3, 9);
    for (let i = 0; i < n; i++) items.push(target);
    for (let i = 0; i < R(4, 8); i++) items.push(pick(names.filter(x => x !== target)));
    const cells = shuffle([...Array(24).keys()]).slice(0, items.length);
    let svg = '<svg viewBox="0 0 300 200"><rect width="300" height="200" rx="16" fill="#fff7ec"/>';
    items.forEach((s, i) => { const c = cells[i], x = 25 + (c % 6) * 50, y = 25 + Math.floor(c / 6) * 50; svg += SHAPES[s](x + R(-4, 4), y + R(-4, 4), pick(COLORS)); });
    svg += '</svg>';
    const p = person();
    return { prompt: `${p.가} 도형을 세고 있어요. ${target}는 모두 몇 개일까요?`, html: `<div class="svgbox">${svg}</div>`, ...numChoices(n, [n + 1, n - 1, items.length]) };
  };
  G.clock = () => {
    const h = R(1, 12), m = pick([0, 30]);
    const label = (hh, mm) => `${hh}시` + (mm ? ' 30분' : '');
    const ans = label(h, m);
    const wrong = new Set();
    const cand = [label(h, m ? 0 : 30), label(h % 12 + 1, m), label(h === 1 ? 12 : h - 1, m), label(m ? (h % 12 + 1) : h, m ? 0 : 30), label((h + 5) % 12 + 1, m)];
    for (const c of shuffle(cand)) { if (c !== ans) wrong.add(c); if (wrong.size === 2) break; }
    const p = person();
    return { prompt: m ? `${p.가} 시계를 봤어요. 몇 시 몇 분일까요?` : '시계가 가리키는 시각은 몇 시일까요?', html: `<div class="svgbox" style="width:220px">${clockSVG(h, m)}</div>`, choices: [ans, ...wrong], answer: 0 };
  };
  const WEIGHTS = [['코끼리', '🐘', '개미', '🐜'], ['수박', '🍉', '딸기', '🍓'], ['자동차', '🚗', '자전거', '🚲'], ['책가방', '🎒', '연필', '✏️'], ['고래', '🐋', '물고기', '🐟'], ['소', '🐄', '병아리', '🐥'], ['볼링공', '🎳', '풍선', '🎈'], ['돌', '🪨', '깃털', '🪶']];
  G.compare = () => {
    const kind = R(0, 2);
    if (kind === 0) {
      const a = R(10, 99); let b = R(10, 99); if (a === b) b++;
      const big = Math.random() < .5; const ans = big ? Math.max(a, b) : Math.min(a, b);
      return { prompt: big ? '두 수 중에서 더 큰 수는?' : '두 수 중에서 더 작은 수는?', choices: [String(ans), String(ans === a ? b : a)], answer: 0, big: true };
    }
    if (kind === 1) {
      const la = R(80, 280); let lb = R(80, 280); if (Math.abs(la - lb) < 30) lb = la > 180 ? la - 60 : la + 60;
      const svg = `<svg viewBox="0 0 300 110"><rect x="10" y="15" width="${la}" height="26" rx="13" fill="#ff6b6b"/><rect x="10" y="66" width="${lb}" height="26" rx="13" fill="#6aa9ff"/></svg>`;
      const longer = Math.random() < .5;
      const ans = (la > lb) === longer ? '빨간 막대' : '파란 막대';
      return { prompt: longer ? '어느 막대가 더 길까요?' : '어느 막대가 더 짧을까요?', html: `<div class="svgbox">${svg}</div>`, choices: [ans, ans === '빨간 막대' ? '파란 막대' : '빨간 막대'], answer: 0 };
    }
    const w = pick(WEIGHTS); const heavy = Math.random() < .5;
    return { prompt: heavy ? '더 무거운 것은 어느 것일까요?' : '더 가벼운 것은 어느 것일까요?', choices: heavy ? [w[1] + ' ' + w[0], w[3] + ' ' + w[2]] : [w[3] + ' ' + w[2], w[1] + ' ' + w[0]], answer: 0 };
  };

  // ---------- 돈 ----------
  function moneyHTML(list, coins) {
    return '<div class="money">' + list.map(v => {
      const c = coins && coins[v];
      const cls = v >= 1000 ? 'bill' : '';
      return c ? `<img class="${cls}" src="${c.url}" alt="${v}원" onerror="this.outerHTML='<span class=coin-fb>${v}원</span>'">` : `<span class="coin-fb">${v}원</span>`;
    }).join('') + '</div>';
  }
  G.coins = (ctx) => {
    const list = []; const n = R(2, 5);
    for (let i = 0; i < n; i++) list.push(pick([10, 50, 100]));
    list.sort((a, b) => b - a);
    const s = list.reduce((a, b) => a + b, 0);
    const p = person();
    return { prompt: `${p.가} 동전을 모았어요. 모두 얼마일까요?`, html: moneyHTML(list, ctx.coins), ...numChoices(s, [s + 10, s - 10, s + 50, s - 50, s + 100], 10), suffix: '원', credits: list.map(v => ctx.coins && ctx.coins[v]) };
  };
  G.moneyCount = (ctx) => {
    const lv = R(0, 2);
    const denoms = [[10, 50, 100], [50, 100, 500], [100, 500, 1000], [500, 1000, 5000]][lv + (Math.random() < .3 ? 1 : 0)];
    const list = []; const n = R(2, 5);
    for (let i = 0; i < n; i++) list.push(pick(denoms));
    list.sort((a, b) => b - a);
    const s = list.reduce((a, b) => a + b, 0), u = Math.min(...list);
    const p = person();
    return { prompt: pick([`${p.가} 저금통을 열었어요. 모두 얼마일까요?`, '돈을 세어 봐요. 모두 얼마일까요?', `${p.의} 지갑에 이만큼 있어요. 모두 얼마일까요?`]),
      html: moneyHTML(list, ctx.coins), ...numChoices(s, [s + u, s - u, s + Math.max(...list), s - Math.max(...list), s + u * 2].filter(x => x > 0), 10), suffix: '원' };
  };
  G.moneyWhich = (ctx) => {
    const v = pick([10, 50, 100, 500, 1000, 5000, 10000]);
    const opts = shuffle([10, 50, 100, 500, 1000, 5000, 10000].filter(x => x !== v)).slice(0, 2);
    return { prompt: '이 돈은 얼마일까요?', html: moneyHTML([v], ctx.coins).replace('<img ', '<img style="height:110px" '), choices: [v, ...opts].map(x => fmt(x) + '원'), answer: 0 };
  };
  G.moneyMake = () => {
    const kind = pick([[100, 500], [100, 1000], [10, 100], [50, 100], [500, 1000], [1000, 5000], [1000, 10000], [10, 50]]);
    const [u, total] = kind, ans = total / u;
    const p = person();
    return { prompt: `${p.가} ${fmt(total)}원을 만들려고 해요. ${fmt(u)}원짜리가 몇 개 있어야 할까요?`, ...numChoices(ans, [ans + 1, ans - 1, ans * 2, ans + 5], 1), suffix: '개' };
  };

  // ---------- 한자 ----------
  const HN = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
  const HM = ['한 일', '두 이', '석 삼', '넉 사', '다섯 오', '여섯 육', '일곱 칠', '여덟 팔', '아홉 구', '열 십'];
  G.hanjaCount = () => {
    const n = R(1, 10);
    const thing = pick(['🍎', '⭐', '🐥', '🌸', '🎈', '●']);
    if (Math.random() < 0.6) {
      const wrong = shuffle(HN.filter((_, i) => i !== n - 1 && Math.abs(i - (n - 1)) <= 3)).slice(0, 2);
      return { prompt: '몇 개일까요? 알맞은 숫자 한자를 골라요.', html: `<div class="dots">${thing.repeat(n)}</div>`, choices: [HN[n - 1], ...wrong], answer: 0, big: true, explain: `${HN[n - 1]}  ${HM[n - 1]}` };
    }
    const wrong = shuffle([...Array(10).keys()].filter(i => i !== n - 1)).slice(0, 2).map(i => String(i + 1));
    return { prompt: '이 한자는 숫자 몇일까요?', display: HN[n - 1], hanja: true, choices: [String(n), ...wrong], answer: 0, big: true, explain: `${HN[n - 1]}  ${HM[n - 1]}` };
  };

  // ---------- 수학 문장제 ----------
  function evalExpr(expr, v) { return Function('a', 'b', 'c', `return (${expr});`)(v.a, v.b, v.c); }
  function fillTemplate(t, vals) {
    // 값 뒤 조사(을/를, 이/가, 은/는, 와/과) 자동 맞춤
    let s = t;
    for (const [k, v] of Object.entries(vals)) s = s.split('{' + k + '}').join('\u0001' + v + '\u0002');
    s = s.replace(/\u0001([^\u0002]*)\u0002(을|를|이|가|은|는|와|과)/g, (m, w, j) => {
      const pair = { 을: '을를', 를: '을를', 이: '이가', 가: '이가', 은: '은는', 는: '은는', 와: '과와', 과: '과와' }[j];
      return w + (batchim(w) ? pair[0] : pair[1]);
    });
    return s.replace(/[\u0001\u0002]/g, '');
  }
  function wordProblem(item, ctx) {
    const rg = item.ranges || {};
    let v, ans, tries = 0;
    do {
      v = {}; for (const k of ['a', 'b', 'c']) v[k] = rg[k] ? R(rg[k][0], rg[k][1]) : 0;
      ans = evalExpr(item.ans, v); tries++;
    } while (tries < 200 && (!(Number.isInteger(ans) && ans >= 0 && ans <= 200) || (item.cond && !evalExpr(item.cond, v))));
    const p = person();
    let obj = null;
    if (item.objs) { const nm = pick(item.objs); obj = (ctx.objects || []).find(o => o.name === nm); }
    const vals = { a: v.a, b: v.b, c: v.c };
    for (const k of Object.keys(p)) vals['N' + k] = p[k];
    if (obj) { vals.o = obj.name; vals.u = obj.unit; }
    let text = fillTemplate(item.template, vals);
    let html = null, credits = [];
    if (obj && item.show) {
      const parts = item.show.split('+').map(x => evalExpr(x, v));
      if (parts.reduce((x, y) => x + y, 0) <= 20) {
        const one = obj.image && obj.image.url ? `<div class="obj"><img src="${obj.image.url}" alt="" onerror="this.outerHTML='${obj.emoji}'"></div>` : `<div class="obj">${obj.emoji}</div>`;
        html = '<div class="obj-grid">' + parts.map(n => one.repeat(n)).join('<span class="plus">+</span>') + '</div>';
        if (obj.image && obj.image.credit) credits.push(obj.image);
      }
    }
    const m = text.match(/몇 ?(자루|송이|켤레|조각|마리|개|권|장|명|대|번|살|쪽|컵|짝|칸|층|원|일|등)(?!째)/);
    const suf = m ? m[1] : '';
    const ch = numChoices(ans, [ans + 1, ans - 1, ans + 10, ans - 10, v.a + v.b, Math.abs(v.a - v.b)].filter(x => x !== ans));
    return { prompt: text, html, ...ch, suffix: suf, credits };
  }

  // ---------- 가게 상황 문제 ----------
  function shopProblem(item, ctx) {
    const goods = ctx.goods || [];
    const p = person();
    const [g1, g2, g3] = shuffle(goods);
    const tag = (g) => ({ ...(g.image || { fallbackEmoji: '🛍️' }), label: `${g.name} ${fmt(g.price)}원` });
    const show = (gs) => '<div class="obj-grid">' + gs.map(g => `<div style="text-align:center"><div class="obj" style="width:96px;height:96px;font-size:60px">${g.image && g.image.url ? `<img src="${g.image.url}" onerror="this.outerHTML='${g.image.fallbackEmoji}'">` : (g.image ? g.image.fallbackEmoji : '🛍️')}</div><div class="price-tag">${g.name} ${fmt(g.price)}원</div></div>`).join('') + '</div>';
    const vals = { N가: p.가, N는: p.는, N의: p.의, i1: g1.name, i2: g2.name, p1: fmt(g1.price) };
    const prep = (tpl, a, b) => tpl.replace('{i1}{와}', J(a.name, '과', '와')).replace('{i1}{를}', J(a.name, '을', '를'))
      .replace('{i2}{를}', J(b.name, '을', '를')).replace('{i2}{와}', J(b.name, '과', '와')).replace('{i1}', a.name).replace('{i2}', b.name);
    const t = prep(item.template, g1, g2);
    const fill = (s, extra) => fillTemplate(s, { ...vals, ...extra });
    const credits = [g1, g2].map(g => g.image).filter(x => x && x.credit);
    switch (item.kind) {
      case 'sum2': { const s = g1.price + g2.price; return { prompt: fill(t), html: show([g1, g2]), ...numChoices(s, [s + 100, s - 100, s + 1000, Math.abs(g1.price - g2.price)], 0), suffix: '원', credits }; }
      case 'double': { const s = g1.price * 2; return { prompt: fill(t), html: show([g1]), ...numChoices(s, [g1.price, s + 100, s - 100, s + g1.price]), suffix: '원', credits: credits.slice(0, 1) }; }
      case 'change': {
        const m = g1.price < 1000 ? 1000 : (g1.price < 5000 ? 5000 : 10000); const s = m - g1.price;
        return { prompt: fill(t, { m: fmt(m) }), html: show([g1]), ...numChoices(s, [s + 100, s - 100, g1.price, m + g1.price].filter(x => x > 0)), suffix: '원', credits: credits.slice(0, 1) };
      }
      case 'canbuy': {
        const m = pick([300, 500, 1000, 2000]);
        const ok = shuffle(goods.filter(g => g.price <= m)), no = shuffle(goods.filter(g => g.price > m));
        if (!ok.length || no.length < 2) return shopProblem({ ...item, kind: 'sum2', template: SHOP_FALLBACK }, ctx);
        const choices = [tag(ok[0]), tag(no[0]), tag(no[1])];
        return { prompt: fill(t, { m: fmt(m) }), type: 'imageChoice', choices, answer: 0, credits: [] };
      }
      case 'pricier': case 'cheaper': {
        let a = g1, b = goods.find(g => g.price !== g1.price && g !== g1) || g2;
        const tt = prep(item.template, a, b);
        const hi = a.price > b.price ? a : b, lo = hi === a ? b : a;
        const ans = item.kind === 'pricier' ? hi : lo;
        return { prompt: fill(tt), html: show([a, b]), choices: [ans.name, (ans === a ? b : a).name], answer: 0, credits };
      }
      case 'count100': { const price = pick([200, 300, 400, 500, 600, 700, 800, 900]); const s = price / 100; return { prompt: fill(t, { p1: fmt(price) }), html: moneyHTML([100], ctx.coins), ...numChoices(s, [s + 1, s - 1, price / 10], 1), suffix: '개' }; }
      case 'needmore': {
        const target = goods.filter(g => g.price >= 500); const g = pick(target);
        const have = Math.max(100, g.price - pick([100, 200, 300, 500].filter(x => x < g.price)));
        const s = g.price - have;
        return { prompt: fill(prep(item.template, g, g2), { have: fmt(have) }), html: show([g]), ...numChoices(s, [s + 100, s - 100, have, g.price]), suffix: '원', credits: g.image && g.image.credit ? [g.image] : [] };
      }
    }
    return null;
  }
  const SHOP_FALLBACK = '{N가} {i1}{와} {i2}{를} 샀어요. 모두 얼마일까요?';

  window.GEN = { G, wordProblem, shopProblem, shuffle, pick, R, batchim, J, person, fillTemplate };
})();
