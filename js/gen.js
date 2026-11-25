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
    for (let i = 0; i < 60; i++) {
      const a = i * 6 * Math.PI / 180, big = i % 5 === 0, r1 = big ? 80 : 84;
      ticks += `<line x1="${100 + r1 * Math.sin(a)}" y1="${100 - r1 * Math.cos(a)}" x2="${100 + 89 * Math.sin(a)}" y2="${100 - 89 * Math.cos(a)}" stroke="${big ? '#3b2f2f' : '#b9a9a0'}" stroke-width="${big ? 2.5 : 1.2}"/>`;
    }
    for (let i = 1; i <= 12; i++) {
      const a = (i * 30 - 90) * Math.PI / 180;
      ticks += `<text x="${100 + 66 * Math.cos(a)}" y="${100 + 66 * Math.sin(a) + 8}" font-size="22" font-weight="700" font-family="sans-serif" text-anchor="middle" fill="#3b2f2f">${i}</text>`;
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><circle cx="100" cy="100" r="94" fill="#fff" stroke="#ff8fab" stroke-width="8"/>${ticks}
      <line x1="100" y1="100" x2="${100 + 40 * Math.sin(ha * Math.PI / 180)}" y2="${100 - 40 * Math.cos(ha * Math.PI / 180)}" stroke="#3b2f2f" stroke-width="10" stroke-linecap="round"/>
      <line x1="100" y1="100" x2="${100 + 60 * Math.sin(ma * Math.PI / 180)}" y2="${100 - 60 * Math.cos(ma * Math.PI / 180)}" stroke="#e2577e" stroke-width="5" stroke-linecap="round"/>
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
    return { prompt: `${target}는 모두 몇 개일까요?`, html: `<div class="svgbox">${svg}</div>`, ...numChoices(n, [n + 1, n - 1, items.length]) };
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


  // ---------- 창의 수학 (팩토 1단계 수준) ----------
  // 수 피라미드: 아래 두 수를 더해 위에 써요
  G.pyramid = () => {
    const a = R(1, 6), b = R(1, 6), c = R(1, 6), ab = a + b, bc = b + c, top = ab + bc;
    const hideTop = Math.random() < .5;
    const cell = (v, q) => `<span class="pyr${q ? ' q' : ''}">${q ? '?' : v}</span>`;
    let ans, html;
    if (hideTop) { ans = top; html = `<div class="pyramid"><div>${cell(top, 1)}</div><div>${cell(ab)}${cell(bc)}</div><div>${cell(a)}${cell(b)}${cell(c)}</div></div>`; }
    else { ans = b; html = `<div class="pyramid"><div>${cell(top)}</div><div>${cell(ab)}${cell(bc)}</div><div>${cell(a)}${cell(b, 1)}${cell(c)}</div></div>`; }
    return { prompt: '바로 아래 두 수를 더하면 위의 수가 돼요. ? 에 알맞은 수는?', html, ...numChoices(ans, [ans + 1, ans - 1, ans + 2, top - ab]),
      explain: `${a} + ${b} = ${ab}, ${b} + ${c} = ${bc}, ${ab} + ${bc} = ${top}` };
  };
  // 그림 식: 같은 그림은 같은 수
  const PICS = [['🍎', '🍌'], ['🐶', '🐱'], ['⭐', '🌙'], ['🚗', '🚲'], ['🍩', '🍪']];
  G.picEq = () => {
    const [x, y] = pick(PICS), vx = R(2, 8), vy = R(1, 9);
    const k = pick([2, 3]);
    const line1 = Array(k).fill(x).join(' + ') + ` = ${vx * k}`;
    const line2 = `${x} + ${y} = ${vx + vy}`;
    return { prompt: `같은 그림은 같은 수예요. ${y}는 얼마일까요?`, html: `<div class="eqs"><div>${line1}</div><div>${line2}</div><div>${y} = ?</div></div>`,
      ...numChoices(vy, [vx, vx + vy, vy + 1, vy - 1], 0), explain: `${x} 하나는 ${vx * k} ÷ ${k} = ${vx}. 그래서 ${y}는 ${vx + vy} − ${vx} = ${vy}` };
  };
  // 저울: 무게 바꾸기
  G.balance = () => {
    const sets = [['🍉', '🍎', '🍓'], ['🐘', '🐶', '🐭'], ['📦', '📕', '✏️']];
    const [A, B, C] = pick(sets), ab = pick([2, 3]), bc = pick([2, 3, 4]), na = pick([1, 2]);
    const ans = na * ab * bc;
    return { prompt: `저울이 평평해요. ${A} 1개는 ${B} ${ab}개와 무게가 같고, ${B} 1개는 ${C} ${bc}개와 무게가 같아요. ${A} ${na}개는 ${C} 몇 개와 무게가 같을까요?`,
      html: `<div class="eqs"><div>${A} = ${B.repeat(ab)}</div><div>${B} = ${C.repeat(bc)}</div><div>${A.repeat(na)} = ${C} ?개</div></div>`,
      ...numChoices(ans, [ab + bc, ab * bc + 1, na * (ab + bc), ans + bc]), suffix: '개' };
  };
  // 거꾸로 생각하기
  G.backward = () => {
    const x = R(3, 15), a = R(2, 9), b = R(1, Math.min(9, x + a - 1)), r = x + a - b;
    return { prompt: `어떤 수에 ${J(String(a), '을', '를')} 더하고 ${J(String(b), '을', '를')} 뺐더니 ${J(String(r), '이', '가')} 되었어요. 어떤 수는 얼마일까요?`,
      ...numChoices(x, [r + a - b, r - a, r + b, x + 1]), explain: `거꾸로 생각해요: ${r} + ${b} − ${a} = ${x}` };
  };
  // 수 카드로 두 자리 수 만들기
  G.cards = () => {
    let ds; do { ds = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]).slice(0, 3); } while (ds.filter(d => d === 0).length > 1);
    const nums = []; for (const a of ds) for (const b of ds) if (a !== b && a !== 0) nums.push(a * 10 + b);
    const kind = pick(['max', 'min', 'max', 'min', 'count']);
    const html = `<div class="cards">${ds.map(d => `<span class="ncard">${d}</span>`).join('')}</div>`;
    if (kind === 'count') { const n = nums.length; return { prompt: '수 카드 2장을 골라 만들 수 있는 두 자리 수는 모두 몇 개일까요?', html, ...numChoices(n, [3, 9, 6, 4].filter(v => v !== n)), suffix: '개' }; }
    const ans = kind === 'max' ? Math.max(...nums) : Math.min(...nums);
    const other = nums.filter(v => v !== ans);
    const rev = Number(String(ans).split('').reverse().join(''));
    return { prompt: `수 카드 2장으로 만들 수 있는 가장 ${kind === 'max' ? '큰' : '작은'} 두 자리 수는?`, html,
      ...numChoices(ans, [rev >= 10 ? rev : null, ...shuffle(other)].filter(v => v != null && v !== ans)) };
  };
  // 줄 서기: 앞에서 몇째, 뒤에서 몇째
  G.lineup = () => {
    const f = R(3, 8), b = R(2, 7), n = f + b - 1, p = person();
    if (Math.random() < .5) return { prompt: `${p.가} 줄을 섰어요. 앞에서 ${f}번째, 뒤에서 ${b}번째예요. 줄을 선 사람은 모두 몇 명일까요?`, html: `<div class="dots" style="font-size:26px">🧍🧍🙋‍♀️🧍🧍</div>`,
      ...numChoices(n, [f + b, f + b + 1, n - 1]), suffix: '명', explain: `${f} + ${b} − 1 = ${n}명 (${p.가} 두 번 세어졌어요)` };
    return { prompt: `${n}명이 한 줄로 섰어요. ${p.는} 앞에서 ${f}번째예요. 뒤에서는 몇 번째일까요?`, html: `<div class="dots" style="font-size:26px">🧍🧍🙋‍♀️🧍🧍</div>`,
      ...numChoices(b, [n - f, b + 1, n - f + 2]), suffix: '번째', explain: `${n} − ${f} + 1 = ${b}번째` };
  };
  // 나무 심기 (간격)
  G.trees = () => {
    const gap = pick([2, 3, 5]), k = R(3, 6), len = gap * k;
    if (Math.random() < .5) return { prompt: `길이가 ${len}m인 길의 처음부터 끝까지 ${gap}m마다 나무를 심어요. 처음과 끝에도 심으면 나무는 모두 몇 그루일까요?`,
      html: `<div class="dots" style="font-size:24px">🌳—🌳—🌳—🌳</div>`, ...numChoices(k + 1, [k, k + 2, len]), suffix: '그루', explain: `간격이 ${k}개면 나무는 ${k} + 1 = ${k + 1}그루예요.` };
    const n = R(4, 8);
    return { prompt: `깃발 ${n}개를 한 줄로 꽂았어요. 깃발과 깃발 사이는 모두 몇 군데일까요?`, html: `<div class="dots" style="font-size:24px">🚩 🚩 🚩 🚩</div>`,
      ...numChoices(n - 1, [n, n + 1, n - 2]), suffix: '군데', explain: `깃발이 ${n}개면 사이는 ${n} − 1 = ${n - 1}군데예요.` };
  };
  // 다리 수 세기
  G.legs = () => {
    const c = R(1, 5), d = R(1, 5);
    if (Math.random() < .55) return { prompt: `닭 ${c}마리와 강아지 ${d}마리가 있어요. 다리는 모두 몇 개일까요?`, html: `<div class="dots" style="font-size:30px">${'🐔'.repeat(c)} ${'🐶'.repeat(d)}</div>`,
      ...numChoices(2 * c + 4 * d, [2 * (c + d), 4 * (c + d), c + d, 2 * c + 4 * d + 2]), suffix: '개' };
    const heads = c + d, legs = 2 * c + 4 * d;
    return { prompt: `닭과 강아지가 모두 ${heads}마리 있어요. 다리를 세어 보니 ${legs}개예요. 강아지는 몇 마리일까요?`, html: '<div class="dots" style="font-size:30px">🐔 🐶 ❓</div>',
      ...numChoices(d, [c, d + 1, d - 1]), suffix: '마리', explain: `모두 닭이라면 다리는 ${heads * 2}개. 남는 다리 ${legs - heads * 2}개를 2개씩 나누면 강아지 ${d}마리!` };
  };
  // 같은 수 □
  G.sameBox = () => {
    const x = R(2, 9), k = R(1, 9), kind = pick([2, 3]);
    const s = x * kind + k;
    return { prompt: '□ 에는 모두 같은 수가 들어가요. □ 는 얼마일까요?', display: `${Array(kind).fill('□').join(' + ')} + ${k} = ${s}`, ...numChoices(x, [s - k, x + 1, x - 1, Math.floor((s) / kind)]) };
  };
  // 규칙이 바뀌는 수 (늘어나는 간격)
  G.growPattern = () => {
    const a = R(1, 5), d0 = R(1, 3); const seq = [a]; let d = d0;
    for (let i = 0; i < 4; i++) { seq.push(seq[seq.length - 1] + d); d++; }
    const ans = seq.pop();
    return { prompt: '수가 늘어나는 규칙을 찾아봐요. □ 에 알맞은 수는?', display: seq.join(', ') + ', □',
      ...numChoices(ans, [ans - 1, ans + 1, seq[3] + (seq[3] - seq[2])]), explain: `${d0}, ${d0 + 1}, ${d0 + 2}, ${d0 + 3}씩 커져요.` };
  };
  // 두 가지가 함께 바뀌는 규칙
  G.pattern2 = () => {
    const shapes = ['●', '▲', '■'], cols = ['#ff6b6b', '#4c9aff', '#f6b100'];
    const ls = R(2, 3), lc = ls === 2 ? 3 : 2;
    const len = 7;
    const item = (i) => ({ s: shapes[i % ls], c: cols[i % lc] });
    const span = (o) => `<span style="color:${o.c}">${o.s}</span>`;
    const seq = []; for (let i = 0; i < len; i++) seq.push(item(i));
    const ans = item(len);
    const wrong = [{ s: ans.s, c: cols[(cols.indexOf(ans.c) + 1) % lc] }, { s: shapes[(shapes.indexOf(ans.s) + 1) % ls], c: ans.c }];
    const lab = (o) => ({ 'ff6b6b': '빨간 ', '4c9aff': '파란 ', 'f6b100': '노란 ' }[o.c.slice(1)] + ({ '●': '동그라미', '▲': '세모', '■': '네모' }[o.s]));
    return { prompt: '모양과 색깔이 함께 바뀌어요. ? 에 올 것은?', html: `<div class="dots" style="font-size:38px">${seq.map(span).join(' ')} ❓</div>`,
      choices: [lab(ans), ...wrong.map(lab)], answer: 0 };
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

  // ---------- 시간 (시계·달력) ----------
  const tl = (h, m) => `${h}시` + (m ? ` ${m}분` : '');          // 3시 / 3시 30분
  const hAdd = (h, k) => ((h - 1 + k) % 12 + 12) % 12 + 1;
  const clockBox = (h, m) => `<div class="svgbox clock">${clockSVG(h, m)}</div>`;
  const clockImg = (h, m) => ({ url: 'data:image/svg+xml;utf8,' + encodeURIComponent(clockSVG(h, m)), fallbackEmoji: '🕒' });
  // 시와 분을 모두 봐야 맞힐 수 있는 3지선다: [정답, 시는 같고 분이 다름, 분은 같고 시가 다름]
  function timeChoices(h, m, mins) {
    const otherM = shuffle(mins.filter(x => x !== m))[0];
    const hourErr = m >= 30 ? hAdd(h, 1) : pick([hAdd(h, 1), hAdd(h, -1)]); // 짧은바늘이 다음 숫자 쪽에 있을 때 헷갈림
    return { choices: [tl(h, m), tl(h, otherM), tl(hourErr, m)], answer: 0 };
  }
  G.tHour = () => {
    const h = R(1, 12);
    const wrong = shuffle([...new Set([hAdd(h, 1), hAdd(h, -1), h === 12 ? 6 : 12])].filter(x => x !== h)).slice(0, 2);
    return { prompt: '시계가 가리키는 시각은 몇 시일까요?', html: clockBox(h, 0), choices: [tl(h, 0), ...wrong.map(x => tl(x, 0))], answer: 0,
      explain: `짧은바늘이 ${h}, 긴바늘이 12를 가리키면 ${h}시예요.` };
  };
  G.tHalf = () => {
    const h = R(1, 12);
    return { prompt: '시계가 가리키는 시각은 몇 시 몇 분일까요?', html: clockBox(h, 30), ...timeChoices(h, 30, [0, 30, 15, 45]),
      explain: `긴바늘이 6을 가리키면 30분이에요. 짧은바늘은 ${J(String(h), '과', '와')} ${hAdd(h, 1)} 사이에 있으니까 ${h}시 30분!` };
  };
  G.tQuarter = () => {
    const h = R(1, 12), m = pick([15, 45]);
    return { prompt: '시계가 가리키는 시각은 몇 시 몇 분일까요?', html: clockBox(h, m), ...timeChoices(h, m, [0, 15, 30, 45]),
      explain: `긴바늘이 ${J(String(m / 5), '을', '를')} 가리키면 ${m}분이에요.` };
  };
  G.t5 = () => {
    const h = R(1, 12), m = 5 * R(1, 11);
    const r = timeChoices(h, m, [m / 5, 5 * R(1, 11), m + 5 > 55 ? m - 5 : m + 5].filter(x => x !== m && x > 0 && x < 60));
    return { prompt: '시계가 가리키는 시각은 몇 시 몇 분일까요?', html: clockBox(h, m), ...r,
      explain: `긴바늘이 가리키는 숫자에 5를 곱하면 분이에요. ${m / 5} × 5 = ${m}, 그래서 ${tl(h, m)}!` };
  };
  G.tFind = () => {
    const h = R(1, 12), m = pick([0, 0, 30, 30, 15, 45]);
    const swapH = m === 0 ? 12 : m / 5, swapM = (h % 12) * 5;   // 긴바늘·짧은바늘을 바꿔 본 시계
    let others = [[swapH, swapM], [hAdd(h, 1), m]];
    if (swapH === h && swapM === m) others[0] = [hAdd(h, -1), m];
    return { type: 'imageChoice', clocks: true, prompt: `${J(tl(h, m), '을', '를')} 가리키는 시계를 골라요.`, choices: [clockImg(h, m), ...others.map(([a, b]) => clockImg(a, b))], answer: 0,
      explain: '짧은바늘은 시, 긴바늘은 분을 가리켜요.' };
  };
  G.tDigital = () => {
    const h = R(1, 12), m = pick([0, 30, 15, 45, 5 * R(1, 11)]);
    const others = [[hAdd(h, 1), m], [h, (m + 30) % 60]];
    return { type: 'imageChoice', clocks: true, prompt: '디지털 시계와 같은 시각을 가리키는 시계를 골라요.', display: `${h}:${String(m).padStart(2, '0')}`, displayClass: 'digital',
      speak: `디지털 시계와 같은 시각을 가리키는 시계를 골라요. ${tl(h, m)}`,
      choices: [clockImg(h, m), ...others.map(([a, b]) => clockImg(a, b))], answer: 0 };
  };
  // 직접 고르기: 시 버튼 + 분 버튼
  function clockInput(steps) {
    const h = R(1, 12), m = pick(steps);
    return { type: 'clockInput', prompt: '시계를 보고 몇 시 몇 분인지 직접 골라요.', html: clockBox(h, m), h, m,
      minutes: steps.length > 4 ? [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55] : steps.length > 2 ? [0, 15, 30, 45] : [0, 30],
      choices: [tl(h, m)], answer: 0 };
  }
  G.tInputHalf = () => clockInput([0, 30]);
  G.tInputQuarter = () => clockInput([0, 15, 30, 45]);
  G.tInput5 = () => clockInput([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]);
  G.tLater = () => {
    const h = R(1, 11), m = pick([0, 30]);
    if (Math.random() < 0.6) {
      const k = R(1, 3), a = hAdd(h, k);
      return { prompt: `지금 시계를 보세요. ${k}시간 뒤는 몇 시일까요?`, html: clockBox(h, m), choices: [tl(a, m), tl(hAdd(h, -k), m), tl(hAdd(a, 1), m)], answer: 0,
        explain: `${tl(h, m)}에서 ${k}시간 뒤는 ${tl(a, m)}예요.` };
    }
    const after = m === 0 ? tl(h, 30) : tl(hAdd(h, 1), 0);
    const w = m === 0 ? [tl(h + 1, 0), tl(h, 0)] : [tl(h, 0), tl(hAdd(h, 1), 30)];
    return { prompt: '지금 시계를 보세요. 30분 뒤는 몇 시 몇 분일까요?', html: clockBox(h, m), choices: [after, ...w], answer: 0,
      explain: '긴바늘이 한 바퀴의 반을 돌면 30분이 지나요.' };
  };
  // 달력
  const WD = ['일', '월', '화', '수', '목', '금', '토'];
  function calHTML(y, mo, mark) {
    const first = new Date(y, mo - 1, 1).getDay(), days = new Date(y, mo, 0).getDate();
    let h = `<div class="cal"><div class="cal-title">${y}년 ${mo}월</div><table><tr>${WD.map((w, i) => `<th class="${i === 0 ? 'sun' : i === 6 ? 'sat' : ''}">${w}</th>`).join('')}</tr><tr>`;
    for (let i = 0; i < first; i++) h += '<td></td>';
    for (let d = 1; d <= days; d++) {
      const wd = (first + d - 1) % 7;
      h += `<td class="${wd === 0 ? 'sun' : wd === 6 ? 'sat' : ''}${mark && mark.includes(d) ? ' mark' : ''}">${d}</td>`;
      if (wd === 6 && d < days) h += '</tr><tr>';
    }
    return h + '</tr></table></div>';
  }
  const ym = () => ({ y: pick([2026, 2027]), mo: R(1, 12) });
  G.calDay = () => {
    const { y, mo } = ym(), days = new Date(y, mo, 0).getDate(), d = R(1, days), wd = new Date(y, mo - 1, d).getDay();
    return { prompt: `달력을 보세요. ${mo}월 ${d}일은 무슨 요일일까요?`, html: calHTML(y, mo),
      choices: [WD[wd] + '요일', WD[(wd + 1) % 7] + '요일', WD[(wd + 6) % 7] + '요일'], answer: 0 };
  };
  G.calCount = () => {
    const { y, mo } = ym(), wd = R(0, 6), first = new Date(y, mo - 1, 1).getDay(), days = new Date(y, mo, 0).getDate();
    let n = 0; for (let d = 1; d <= days; d++) if ((first + d - 1) % 7 === wd) n++;
    return { prompt: `달력을 보세요. ${mo}월에 ${WD[wd]}요일은 모두 몇 번 있나요?`, html: calHTML(y, mo), choices: [`${n}번`, `${n === 4 ? 5 : 4}번`, `${n === 4 ? 3 : 6}번`], answer: 0 };
  };
  G.calAfter = () => {
    const { y, mo } = ym(), days = new Date(y, mo, 0).getDate();
    const kind = pick(['week', 'week', 'days', 'before']);
    if (kind === 'week') {
      const d = R(1, days - 7);
      return { prompt: `오늘은 ${mo}월 ${d}일이에요. 일주일 뒤는 며칠일까요?`, html: calHTML(y, mo, [d]), choices: [`${d + 7}일`, `${d + 1}일`, `${d + 6}일`], answer: 0,
        explain: '일주일은 7일이에요. 달력에서 바로 아래 칸이 일주일 뒤예요.' };
    }
    if (kind === 'before') {
      const d = R(9, days);
      return { prompt: `오늘은 ${mo}월 ${d}일이에요. 일주일 전은 며칠일까요?`, html: calHTML(y, mo, [d]), choices: [`${d - 7}일`, `${d - 1}일`, `${d + 7 <= days ? d + 7 : d - 6}일`], answer: 0,
        explain: '일주일 전은 달력에서 바로 위 칸이에요.' };
    }
    const d = R(1, days - 5), k = R(2, 5);
    return { prompt: `오늘은 ${mo}월 ${d}일이에요. ${k}일 뒤는 며칠일까요?`, html: calHTML(y, mo, [d]), ...numChoices(d + k, [d + k + 1, d + k - 1, d + k + 7]), suffix: '일' };
  };
  G.dayNext = () => {
    const w = R(0, 6), kind = pick(['내일', '어제', '모레']);
    const off = { 내일: 1, 어제: -1, 모레: 2 }[kind], a = (w + off + 7) % 7;
    const set = new Set([a]); for (const x of shuffle([(w + 7 - off) % 7, w, (a + 1) % 7, (a + 6) % 7])) { if (set.size >= 3) break; set.add(x); }
    return { prompt: `오늘이 ${WD[w]}요일이면 ${J(kind, '은', '는')} 무슨 요일일까요?`, choices: [...set].map(x => WD[x] + '요일'), answer: 0,
      explain: '일, 월, 화, 수, 목, 금, 토 순서로 돌아요.' };
  };
  G.monthNext = () => {
    const m = R(1, 12), k = pick([1, 1, 2, 3]), a = (m - 1 + k) % 12 + 1;
    const set = new Set([a]); for (const x of shuffle([(m + 10) % 12 + 1, (a % 12) + 1, m, ((a + 10) % 12) + 1])) { if (set.size >= 3) break; set.add(x); }
    return { prompt: k === 1 ? `${m}월 다음 달은 몇 월일까요?` : `${m}월에서 ${k}달 뒤는 몇 월일까요?`, choices: [...set].map(x => x + '월'), answer: 0,
      explain: '12월 다음에는 다시 1월이 와요.' };
  };

  const SHOP_FALLBACK = '{N가} {i1}{와} {i2}{를} 샀어요. 모두 얼마일까요?';

  window.GEN = { G, wordProblem, shopProblem, shuffle, pick, R, batchim, J, person, fillTemplate };
})();
