/* 자동 동기화: Firebase Realtime Database (부모님 Google 계정의 무료 저장소)
   - 같은 '가족 코드'를 넣은 폰끼리 기록(별·푼 문제·복습·오답노트)을 자동으로 합쳐요.
   - 기록은 families/<가족코드>/rec 에 JSON 글자 하나로 저장해요.
   - 지우기(오답노트 지우기·기록 지우기)는 '새 판(epoch)'으로 올려서 다른 폰도 그대로 따라가요. */
(function () {
  'use strict';
  const CFG = window.FIREBASE_CONFIG;
  const CODE_KEY = 'sieun-family-code';
  const SDK = 'https://www.gstatic.com/firebasejs/10.12.5/';
  const A = () => window.APP;
  let db = null, ref = null, ready = false, status = '꺼짐', timer = null, lastSync = null, listening = false;

  const getCode = () => { try { return localStorage.getItem(CODE_KEY) || ''; } catch (e) { return ''; } };
  const setCodeLS = (c) => { try { c ? localStorage.setItem(CODE_KEY, c) : localStorage.removeItem(CODE_KEY); } catch (e) {} };
  const norm = (c) => String(c || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  const pretty = (c) => c.replace(/(.{4})(?=.)/g, '$1-');
  function newCode() {
    const al = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'; const r = new Uint32Array(12); crypto.getRandomValues(r);
    return Array.from(r, x => al[x % al.length]).join('');
  }
  const newEpoch = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 6);

  // 이 폰의 기록만 뽑기 / 받은 기록으로 바꾸기
  function rec() { const S = A().state, o = {}; A().REC_KEYS.forEach(k => o[k] = S[k]); return JSON.parse(JSON.stringify(o)); }
  function adopt(r) { const S = A().state; A().REC_KEYS.forEach(k => S[k] = r[k] != null ? r[k] : (k === 'stars' ? 0 : {})); S.syncEpoch = r.epoch; }
  const parse = (v) => { try { return v ? JSON.parse(v) : null; } catch (e) { return null; } };

  function loadScript(src) { return new Promise((ok, no) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = no; document.head.appendChild(s); }); }
  async function start() {
    const code = getCode();
    if (!CFG || !code) { status = !CFG ? '설정 전' : '꺼짐'; return; }
    try {
      status = '연결 중…'; paint();
      if (!window.firebase) { await loadScript(SDK + 'firebase-app-compat.js'); await loadScript(SDK + 'firebase-auth-compat.js'); await loadScript(SDK + 'firebase-database-compat.js'); }
      if (!firebase.apps.length) firebase.initializeApp(CFG);
      await firebase.auth().signInAnonymously();
      db = firebase.database(); ref = db.ref('families/' + code + '/rec');
      ready = true;
      await push();
      if (!listening) { listening = true; ref.on('value', onRemote, (e) => { status = '오류: ' + e.code; paint(); }); }
      status = '켜짐';
    } catch (e) { console.error(e); status = '연결 실패 (' + (e.code || e.message || e) + ')'; ready = false; }
    paint();
  }

  // 다른 폰이 올린 기록이 바뀌었을 때
  function onRemote(snap) {
    const r = parse(snap.val()); if (!r) return;
    const S = A().state;
    const before = JSON.stringify(rec());
    if (S.syncEpoch && r.epoch && r.epoch !== S.syncEpoch) adopt(r);  // 다른 폰에서 지우기를 했음 → 그대로 따라감
    else { A().mergeInto(S, r); S.syncEpoch = r.epoch || S.syncEpoch; }
    lastSync = new Date();
    if (JSON.stringify(rec()) !== before) { A().save(true); A().refresh(); }
    // 이 폰에만 있는 기록이 남아 있으면 다시 올림
    const merged = rec(); A().mergeInto(merged, r);
    if (JSON.stringify(merged) !== JSON.stringify((({ epoch, ...x }) => x)(r))) schedule(500);
    paint();
  }

  // 이 폰 기록을 서버 기록과 합쳐서 올리기 (동시에 두 폰이 올려도 안전하게 transaction)
  async function push() {
    if (!ready) return;
    const S = A().state, local = rec();
    let adopted = null;
    const res = await ref.transaction((cur) => {
      adopted = null;
      const r = parse(cur);
      if (!r || !r.epoch) return JSON.stringify({ ...local, epoch: S.syncEpoch || newEpoch() });
      if (S.syncEpoch && r.epoch !== S.syncEpoch) { adopted = r; return; }  // 서버가 새 판 → 이 폰이 따라감 (쓰지 않음)
      const m = JSON.parse(JSON.stringify(r)); A().mergeInto(m, local); m.epoch = r.epoch;
      const out = JSON.stringify(m);
      return out === cur ? undefined : out;
    }, undefined, false);
    const r = parse(res.snapshot.val());
    if (r) { if (adopted || (S.syncEpoch && r.epoch !== S.syncEpoch)) adopt(r); else { A().mergeInto(S, r); S.syncEpoch = r.epoch; } A().save(true); A().refresh(); }
    lastSync = new Date(); paint();
  }
  function schedule(ms) { clearTimeout(timer); timer = setTimeout(() => push().catch(e => { console.error(e); status = '올리기 실패'; paint(); }), ms); }

  // 지운 것까지 모든 폰에 그대로: 새 판으로 덮어쓰기
  async function authoritative() {
    if (!ready) return;
    const S = A().state; S.syncEpoch = newEpoch(); A().save(true);
    await ref.set(JSON.stringify({ ...rec(), epoch: S.syncEpoch }));
    lastSync = new Date(); paint();
  }

  // ---------- 부모님 메뉴 화면 ----------
  let box = null;
  function paint() {
    if (!box || !document.body.contains(box)) return;
    const code = getCode();
    if (!CFG) { box.innerHTML = '<p class="sync-note">아직 Firebase 저장소가 연결되지 않았어요. (설정이 끝나면 여기에서 켤 수 있어요)</p>'; return; }
    if (!code) {
      box.innerHTML = `<p class="sync-note">처음 켜는 폰에서는 <b>새 가족 코드 만들기</b>, 다른 폰에서는 그 코드를 <b>입력</b>하세요. 같은 코드를 넣은 폰끼리 기록이 자동으로 합쳐져요.</p>
        <button id="syncNew">✨ 새 가족 코드 만들기</button>
        <div class="sync-join"><input id="syncIn" placeholder="가족 코드 입력 (예: ABCD-EFGH-JKMN)" autocapitalize="characters"><button id="syncJoin">연결</button></div>`;
      box.querySelector('#syncNew').onclick = () => { setCodeLS(newCode()); start(); paint(); };
      box.querySelector('#syncJoin').onclick = () => {
        const c = norm(box.querySelector('#syncIn').value);
        if (c.length < 12) return alert('가족 코드를 끝까지 정확히 넣어 주세요.');
        setCodeLS(c); start(); paint();
      };
      return;
    }
    const t = lastSync ? `${lastSync.getHours()}:${String(lastSync.getMinutes()).padStart(2, '0')}` : '-';
    box.innerHTML = `<p class="sync-state">상태: <b>${status}</b> · 마지막 동기화 ${t}</p>
      <p class="sync-code">가족 코드 <b>${pretty(code)}</b></p>
      <p class="sync-note">다른 폰의 부모님 메뉴에서 이 코드를 입력하면 같은 기록을 써요. 코드를 아는 사람만 기록을 볼 수 있으니 가족끼리만 나눠 주세요.</p>
      <button id="syncNow">🔄 지금 동기화</button><button id="syncCopy">📋 코드 복사</button><button id="syncOff">연결 끊기</button>`;
    box.querySelector('#syncNow').onclick = () => (ready ? push() : start());
    box.querySelector('#syncCopy').onclick = async () => { try { await navigator.clipboard.writeText(pretty(code)); alert('가족 코드를 복사했어요.'); } catch (e) { prompt('가족 코드', pretty(code)); } };
    box.querySelector('#syncOff').onclick = () => {
      if (!confirm('이 폰의 자동 동기화를 끌까요? (이 폰 기록은 그대로 남아요)')) return;
      if (ref) ref.off(); listening = false; ready = false; setCodeLS(''); status = '꺼짐'; paint();
    };
  }
  function renderBox(el) { box = el; paint(); }

  window.SYNC = { dirty: () => ready && schedule(2000), authoritative: () => authoritative().catch(console.error), renderBox, get status() { return status; } };
  // 앱을 다시 볼 때마다 한 번 맞추기
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && ready) schedule(300); });
  if (CFG && getCode()) start();
})();
