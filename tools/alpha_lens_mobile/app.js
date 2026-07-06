const PERSPECTIVES = [
  { key: 'hook_bullish', label: 'هوک صعودی', direction: 'bullish', mode: 'Hook' },
  { key: 'rally_bullish', label: 'رالی صعودی', direction: 'bullish', mode: 'Rally' },
  { key: 'hook_bearish', label: 'هوک نزولی', direction: 'bearish', mode: 'Hook' },
  { key: 'rally_bearish', label: 'رالی نزولی', direction: 'bearish', mode: 'Rally' },
];
const TIMEFRAMES = [
  { key: '1h', label: '1H / یک‌ساعته', role: 'Context / Parent' },
  { key: '10m', label: '10M / ده‌دقیقه', role: 'Child / Setup' },
  { key: '1m', label: '1M / یک‌دقیقه', role: 'Entry / Trigger' },
];
const STORAGE_KEY = 'alpha_lens_matrix_v1';
const SNAPSHOT_KEY = 'alpha_lens_snapshots_v1';

const $ = (id) => document.getElementById(id);
const matrix = $('matrix');
const template = $('cellTemplate');

function makeDefaultState() {
  const cells = {};
  for (const p of PERSPECTIVES) {
    for (const tf of TIMEFRAMES) {
      cells[`${p.key}__${tf.key}`] = {
        risk: '—', reward: '—', action: 'Empty', score: '', notes: ''
      };
    }
  }
  return {
    symbol: 'XAUUSD',
    session: '',
    globalContext: '',
    finalBias: 'نامشخص',
    finalAction: 'Watch',
    finalNotes: '',
    cells,
    updatedAt: new Date().toISOString(),
  };
}

let state = loadState();

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? { ...makeDefaultState(), ...JSON.parse(raw) } : makeDefaultState();
  } catch (_) {
    return makeDefaultState();
  }
}

function saveState() {
  state.updatedAt = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function setInputsFromState() {
  $('symbolInput').value = state.symbol || '';
  $('sessionInput').value = state.session || '';
  $('globalContext').value = state.globalContext || '';
  $('finalBias').value = state.finalBias || 'نامشخص';
  $('finalAction').value = state.finalAction || 'Watch';
  $('finalNotes').value = state.finalNotes || '';
}

function buildMatrix() {
  matrix.innerHTML = '';
  for (const p of PERSPECTIVES) {
    for (const tf of TIMEFRAMES) {
      const id = `${p.key}__${tf.key}`;
      if (!state.cells[id]) state.cells[id] = { risk: '—', reward: '—', action: 'Empty', score: '', notes: '' };
      const node = template.content.cloneNode(true);
      const card = node.querySelector('.cell-card');
      card.dataset.id = id;
      card.dataset.direction = p.direction;
      card.dataset.action = state.cells[id].action || 'Empty';
      node.querySelector('.cell-title').textContent = `${p.label} × ${tf.label} — ${tf.role}`;
      const risk = node.querySelector('.risk');
      const reward = node.querySelector('.reward');
      const action = node.querySelector('.action');
      const score = node.querySelector('.score');
      const notes = node.querySelector('.notes');
      risk.value = state.cells[id].risk || '—';
      reward.value = state.cells[id].reward || '—';
      action.value = state.cells[id].action || 'Empty';
      score.value = state.cells[id].score || '';
      notes.value = state.cells[id].notes || '';
      [risk, reward, action, score, notes].forEach(input => {
        input.addEventListener('input', () => {
          state.cells[id] = {
            risk: risk.value,
            reward: reward.value,
            action: action.value,
            score: score.value,
            notes: notes.value,
          };
          card.dataset.action = action.value;
          saveState();
        });
      });
      matrix.appendChild(node);
    }
  }
}

function wireTopInputs() {
  $('symbolInput').addEventListener('input', e => { state.symbol = e.target.value; saveState(); });
  $('sessionInput').addEventListener('input', e => { state.session = e.target.value; saveState(); });
  $('globalContext').addEventListener('input', e => { state.globalContext = e.target.value; saveState(); });
  $('finalBias').addEventListener('input', e => { state.finalBias = e.target.value; saveState(); });
  $('finalAction').addEventListener('input', e => { state.finalAction = e.target.value; saveState(); });
  $('finalNotes').addEventListener('input', e => { state.finalNotes = e.target.value; saveState(); });
}

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function getSnapshots() {
  try { return JSON.parse(localStorage.getItem(SNAPSHOT_KEY) || '[]'); }
  catch (_) { return []; }
}
function saveSnapshots(items) { localStorage.setItem(SNAPSHOT_KEY, JSON.stringify(items)); }

function renderSnapshots() {
  const list = $('snapshotsList');
  const items = getSnapshots().sort((a,b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
  list.innerHTML = '';
  if (!items.length) {
    list.innerHTML = '<p class="subtitle">هنوز Snapshot ذخیره نشده.</p>';
    return;
  }
  for (const item of items) {
    const div = document.createElement('article');
    div.className = 'snapshot-item';
    const title = `${item.state?.symbol || 'Symbol'} — ${item.state?.finalBias || 'نامشخص'} — ${item.state?.finalAction || 'Watch'}`;
    const date = new Date(item.createdAt).toLocaleString('fa-IR');
    div.innerHTML = `
      <header>
        <h3>${title}</h3>
        <span>${date}</span>
      </header>
      <p>${item.state?.finalNotes || item.state?.globalContext || 'بدون توضیح'}</p>
      <div class="snapshot-actions">
        <button type="button" data-load="${item.id}" class="ghost">Load</button>
        <button type="button" data-export="${item.id}" class="ghost">Export</button>
        <button type="button" data-delete="${item.id}" class="ghost danger">Delete</button>
      </div>
    `;
    list.appendChild(div);
  }
  list.querySelectorAll('[data-load]').forEach(btn => btn.addEventListener('click', () => {
    const found = getSnapshots().find(x => x.id === btn.dataset.load);
    if (found?.state) {
      state = found.state;
      saveState();
      setInputsFromState();
      buildMatrix();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }));
  list.querySelectorAll('[data-export]').forEach(btn => btn.addEventListener('click', () => {
    const found = getSnapshots().find(x => x.id === btn.dataset.export);
    if (found) downloadJson(`alpha-lens-${found.id}.json`, found);
  }));
  list.querySelectorAll('[data-delete]').forEach(btn => btn.addEventListener('click', () => {
    saveSnapshots(getSnapshots().filter(x => x.id !== btn.dataset.delete));
    renderSnapshots();
  }));
}

function wireActions() {
  $('saveSnapshotBtn').addEventListener('click', () => {
    const items = getSnapshots();
    const snapshot = {
      id: `${Date.now()}`,
      createdAt: new Date().toISOString(),
      state: JSON.parse(JSON.stringify(state)),
    };
    items.push(snapshot);
    saveSnapshots(items);
    renderSnapshots();
  });
  $('exportBtn').addEventListener('click', () => {
    downloadJson(`alpha-lens-current-${Date.now()}.json`, { exportedAt: new Date().toISOString(), state, snapshots: getSnapshots() });
  });
  $('importInput').addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const obj = JSON.parse(await file.text());
      if (obj.state) state = { ...makeDefaultState(), ...obj.state };
      if (Array.isArray(obj.snapshots)) saveSnapshots(obj.snapshots);
      saveState();
      setInputsFromState();
      buildMatrix();
      renderSnapshots();
    } catch (err) {
      alert('فایل JSON معتبر نیست.');
    } finally {
      event.target.value = '';
    }
  });
  $('clearSnapshotsBtn').addEventListener('click', () => {
    if (confirm('همه Snapshotها حذف شوند؟')) {
      saveSnapshots([]);
      renderSnapshots();
    }
  });
  $('resetBtn').addEventListener('click', () => {
    if (confirm('فرم فعلی ریست شود؟ Snapshotها حذف نمی‌شوند.')) {
      state = makeDefaultState();
      saveState();
      setInputsFromState();
      buildMatrix();
    }
  });
}

async function registerSW() {
  if ('serviceWorker' in navigator) {
    try { await navigator.serviceWorker.register('./sw.js'); }
    catch (err) { console.warn('Service worker registration failed', err); }
  }
}

setInputsFromState();
buildMatrix();
wireTopInputs();
wireActions();
renderSnapshots();
saveState();
registerSW();
