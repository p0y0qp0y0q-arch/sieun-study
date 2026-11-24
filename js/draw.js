/* 그림 그리기 캔버스 */
(function () {
  const COLORS = ['#000000', '#ff3b30', '#ff9500', '#ffcc00', '#34c759', '#00c7be', '#007aff', '#5856d6', '#af52de', '#ff2d55', '#8e5a2b', '#ffb6c8', '#ffffff'];
  const cv = document.getElementById('canvas');
  const ctx = cv.getContext('2d');
  let color = COLORS[1], size = 10, eraser = false, drawing = false, last = null, history = [], opened = false;
  function resize() {
    const r = cv.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    const img = cv.width ? ctx.getImageData(0, 0, cv.width, cv.height) : null;
    cv.width = r.width * dpr; cv.height = r.height * dpr;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height);
    if (img) ctx.putImageData(img, 0, 0);
    ctx.scale(dpr, dpr);
  }
  const pal = document.getElementById('palette');
  COLORS.forEach((c, i) => {
    const b = document.createElement('button'); b.style.background = c; if (i === 1) b.classList.add('active');
    b.onclick = () => { color = c; eraser = false; document.getElementById('eraser').classList.remove('active'); pal.querySelectorAll('button').forEach(x => x.classList.remove('active')); b.classList.add('active'); };
    pal.appendChild(b);
  });
  document.querySelectorAll('[data-size]').forEach(b => b.onclick = () => { size = +b.dataset.size; document.querySelectorAll('[data-size]').forEach(x => x.classList.remove('active')); b.classList.add('active'); });
  document.getElementById('eraser').onclick = (e) => { eraser = !eraser; e.currentTarget.classList.toggle('active', eraser); };
  document.getElementById('clear').onclick = () => { if (confirm('그림을 모두 지울까요?')) { snapshot(); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height); ctx.restore(); } };
  document.getElementById('undo').onclick = () => { const h = history.pop(); if (h) ctx.putImageData(h, 0, 0); };
  document.getElementById('save').onclick = () => {
    const a = document.createElement('a'); const d = new Date();
    a.download = `시은이그림_${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}_${d.getHours()}${d.getMinutes()}.png`;
    a.href = cv.toDataURL('image/png'); a.click();
  };
  function snapshot() { history.push(ctx.getImageData(0, 0, cv.width, cv.height)); if (history.length > 20) history.shift(); }
  function pos(e) { const r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  cv.addEventListener('pointerdown', (e) => { drawing = true; snapshot(); last = pos(e); cv.setPointerCapture(e.pointerId); dot(last); });
  cv.addEventListener('pointermove', (e) => { if (!drawing) return; const p = pos(e); line(last, p); last = p; });
  ['pointerup', 'pointercancel'].forEach(t => cv.addEventListener(t, () => drawing = false));
  function stroke() { ctx.strokeStyle = eraser ? '#fff' : color; ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = eraser ? size * 2.5 : size; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; }
  function dot(p) { stroke(); ctx.beginPath(); ctx.arc(p.x, p.y, ctx.lineWidth / 2, 0, Math.PI * 2); ctx.fill(); }
  function line(a, b) { stroke(); ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
  window.DRAW = { open() { if (!opened) { opened = true; requestAnimationFrame(resize); } } };
  window.addEventListener('resize', () => opened && resize());
})();
