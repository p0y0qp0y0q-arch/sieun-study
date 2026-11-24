/* 그림 그리기 캔버스: 연필 · 페인트통(채우기) · 지우개 · 되돌리기 · 저장 */
(function () {
  const COLORS = ['#000000', '#ff3b30', '#ff9500', '#ffcc00', '#34c759', '#00c7be', '#007aff', '#5856d6', '#af52de', '#ff2d55', '#8e5a2b', '#ffb6c8', '#ffffff'];
  const cv = document.getElementById('canvas');
  const ctx = cv.getContext('2d', { willReadFrequently: true });
  let sized = false, color = COLORS[1], size = 10, mode = 'pen', drawing = false, last = null, history = [], opened = false, dpr = 1;
  function resize() {
    const r = cv.getBoundingClientRect(); dpr = window.devicePixelRatio || 1;
    const old = sized ? ctx.getImageData(0, 0, cv.width, cv.height) : null;
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height);
    if (old) ctx.putImageData(old, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    sized = true;
  }
  const pal = document.getElementById('palette');
  COLORS.forEach((c, i) => {
    const b = document.createElement('button'); b.style.background = c; b.setAttribute('aria-label', c); if (i === 1) b.classList.add('active');
    b.onclick = () => { color = c; if (mode === 'eraser') setMode('pen'); pal.querySelectorAll('button').forEach(x => x.classList.remove('active')); b.classList.add('active'); };
    pal.appendChild(b);
  });
  function setMode(m) { mode = m; document.querySelectorAll('[data-mode]').forEach(x => x.classList.toggle('active', x.dataset.mode === m)); }
  document.querySelectorAll('[data-mode]').forEach(b => b.onclick = () => setMode(b.dataset.mode));
  document.querySelectorAll('[data-size]').forEach(b => b.onclick = () => { size = +b.dataset.size; if (mode === 'fill') setMode('pen'); document.querySelectorAll('[data-size]').forEach(x => x.classList.remove('active')); b.classList.add('active'); });
  document.getElementById('clear').onclick = () => { if (confirm('그림을 모두 지울까요?')) { snapshot(); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height); ctx.restore(); } };
  document.getElementById('undo').onclick = () => { const h = history.pop(); if (h) ctx.putImageData(h, 0, 0); };
  document.getElementById('save').onclick = () => {
    const a = document.createElement('a'); const d = new Date();
    a.download = `시은이그림_${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}_${d.getHours()}${String(d.getMinutes()).padStart(2, '0')}.png`;
    a.href = cv.toDataURL('image/png'); a.click();
  };
  function snapshot() { history.push(ctx.getImageData(0, 0, cv.width, cv.height)); if (history.length > 20) history.shift(); }
  function pos(e) { const r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }

  // 페인트통: 누른 곳과 같은 색으로 이어진 영역을 채운다 (선 가장자리 번짐은 허용 오차로 처리)
  function hex(c) { const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function fill(p) {
    const W = cv.width, H = cv.height;
    const sx = Math.floor(p.x * dpr), sy = Math.floor(p.y * dpr);
    if (sx < 0 || sy < 0 || sx >= W || sy >= H) return;
    const img = ctx.getImageData(0, 0, W, H), d = img.data;
    const i0 = (sy * W + sx) * 4, tr = d[i0], tg = d[i0 + 1], tb = d[i0 + 2];
    const [fr, fg, fb] = hex(color);
    if (Math.abs(tr - fr) + Math.abs(tg - fg) + Math.abs(tb - fb) < 10) return;
    const TOL = 90;
    const same = (i) => Math.abs(d[i] - tr) + Math.abs(d[i + 1] - tg) + Math.abs(d[i + 2] - tb) <= TOL;
    const seen = new Uint8Array(W * H);
    const stack = [sx, sy];
    while (stack.length) {
      const y = stack.pop(), x0 = stack.pop();
      let x = x0;
      while (x >= 0 && !seen[y * W + x] && same((y * W + x) * 4)) x--;
      x++;
      let up = false, down = false;
      for (; x < W; x++) {
        const k = y * W + x;
        if (seen[k] || !same(k * 4)) break;
        seen[k] = 1; const i = k * 4; d[i] = fr; d[i + 1] = fg; d[i + 2] = fb; d[i + 3] = 255;
        if (y > 0) { const ku = k - W; const ok = !seen[ku] && same(ku * 4); if (ok && !up) { stack.push(x, y - 1); up = true; } else if (!ok) up = false; }
        if (y < H - 1) { const kd = k + W; const ok = !seen[kd] && same(kd * 4); if (ok && !down) { stack.push(x, y + 1); down = true; } else if (!ok) down = false; }
      }
    }
    // 가장자리 한 칸 더 칠해서 선 옆 하얀 테두리 없애기
    const grow = new Uint8Array(seen);
    for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
      const k = y * W + x; if (seen[k]) continue;
      if (seen[k - 1] || seen[k + 1] || seen[k - W] || seen[k + W]) {
        const i = k * 4; const lum = d[i] + d[i + 1] + d[i + 2];
        if (lum > 300) { d[i] = fr; d[i + 1] = fg; d[i + 2] = fb; grow[k] = 1; }
      }
    }
    ctx.putImageData(img, 0, 0);
  }

  cv.addEventListener('pointerdown', (e) => {
    snapshot();
    const p = pos(e);
    if (mode === 'fill') { fill(p); return; }
    drawing = true; last = p; cv.setPointerCapture(e.pointerId); dot(last);
  });
  cv.addEventListener('pointermove', (e) => { if (!drawing) return; const p = pos(e); line(last, p); last = p; });
  ['pointerup', 'pointercancel'].forEach(t => cv.addEventListener(t, () => drawing = false));
  function stroke() { const er = mode === 'eraser'; ctx.strokeStyle = er ? '#fff' : color; ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = er ? size * 2.5 : size; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; }
  function dot(p) { stroke(); ctx.beginPath(); ctx.arc(p.x, p.y, ctx.lineWidth / 2, 0, Math.PI * 2); ctx.fill(); }
  function line(a, b) { stroke(); ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
  window.DRAW = { open() { if (!opened) { opened = true; requestAnimationFrame(resize); } } };
  window.addEventListener('resize', () => opened && resize());
})();
