const PERSPECTIVES = [
  { key: 'hook_bullish', label: 'هوک\nصعودی', full: 'هوک صعودی', direction: 'bullish', mode: 'Hook' },
  { key: 'rally_bullish', label: 'رالی\nصعودی', full: 'رالی صعودی', direction: 'bullish', mode: 'Rally' },
  { key: 'hook_bearish', label: 'هوک\nنزولی', full: 'هوک نزولی', direction: 'bearish', mode: 'Hook' },
  { key: 'rally_bearish', label: 'رالی\nنزولی', full: 'رالی نزولی', direction: 'bearish', mode: 'Rally' },
];
const TIMEFRAMES = [
  { key: '1h', label: '1H', role: 'Context' },
  { key: '10m', label: '10M', role: 'Zone' },
  { key: '1m', label: '1M', role: 'Entry' },
];

const STORAGE_KEY = 'alpha_lens_matrix_minimal_v2';
const SNAPSHOT_KEY = 'alpha_lens_snapshots_minimal_v2';
const OLD_STORAGE_KEY = 'alpha_lens_matrix_v1';
const $ = (id) => document.getElementById(id);

let activeCellId = 'hook_bullish__1h';
let state = loadState();

function makeDefaultCells() {
  const cells = {};
  for (const p of PERSPECTIVES) {
    for (const tf of TIMEFRAMES) {
      cells[`${p.key}__${tf.key}`] = { risk: '—', reward: '—', action: 'Empty', score: '', notes: '' };
    }
  }
  return cells;
}

function makeDefaultState() {
  return {
    symbol: 'XAUUSD', session: '', globalContext: '',
    finalBias: 'نامشخص', finalAction: 'Watch', finalNotes: '',
    cells: makeDefaultCells(), updatedAt: new Date().toISOString(),
  };
}

function normalizeState(raw) {
  const base = makeDefaultState();
  const parsed = raw ? JSON.parse(raw) : {};
  return { ...base, ...parsed, cells: { ...base.cells, ...(parsed.cells || {}) } };
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY) || localStorage.getItem(OLD_STORAGE_KEY);
    return normalizeState(raw);
  } catch (_) { return makeDefaultState(); }
}

function saveState() {
  state.updatedAt = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function cellMeta(id) {
  const [pKey, tfKey] = id.split('__');
  const p = PERSPECTIVES.find(x => x.key === pKey);
  const tf = TIMEFRAMES.find(x => x.key === tfKey);
  return { p, tf };
}

function shortValue(value, fallback = '—') {
  if (!value || value === 'Empty') return fallback;
  if (value === 'Wait for Child') return 'Wait';
  if (value === 'Limit Ready') return 'Limit';
  if (value === 'No Trade') return 'No';
  if (value === 'Medium') return 'Med';
  return value;
}

function bindTopInputs() {
  $('symbolInput').value = state.symbol || '';
  $('sessionInput').value = state.session || '';
  $('globalContext').value = state.globalContext || '';
  $('finalBias').value = state.finalBias || 'نامشخص';
  $('finalAction').value = state.finalAction || 'Watch';
  $('finalNotes').value = state.finalNotes || '';

  $('symbolInput').addEventListener('input', e => { state.symbol = e.target.value; saveState(); });
  $('sessionInput').addEventListener('input', e => { state.session = e.target.value; saveState(); });
  $('globalContext').addEventListener('input', e => { state.globalContext = e.target.value; saveState(); });
  $('finalBias').addEventListener('input', e => { state.finalBias = e.target.value; saveState(); });
  $('finalAction').addEventListener('input', e => { state.finalAction = e.target.value; saveState(); });
  $('finalNotes').addEventListener('input', e => { state.finalNotes = e.target.value; saveState(); });
}

function buildMatrix() {
  const matrix = $('matrix');
  matrix.innerHTML = '';
  for (const p of PERSPECTIVES) {
    const row = document.createElement('div');
    row.className = 'lens-row';
    const rowLabel = document.createElement('div');
    rowLabel.className = `row-label ${p.direction}`;
    rowLabel.innerHTML = p.label.replace('\n', '<br>');
    row.appendChild(rowLabel);

    for (const tf of TIMEFRAMES) {
      const id = `${p.key}__${tf.key}`;
      const cell = state.cells[id] || { risk: '—', reward: '—', action: 'Empty', score: '', notes: '' };
      const btn = document.createElement('button');
      btn.className = `cell-tile ${id === activeCellId ? 'active' : ''}`;
      btn.type = 'button';
      btn.dataset.id = id;
      btn.dataset.direction = p.direction;
      btn.dataset.action = cell.action || 'Empty';
      btn.innerHTML = `
        <span class="dot"></span>
        <span class="score">${cell.score || '—'}</span>
        <span class="mini">R:${shortValue(cell.risk)} · W:${shortValue(cell.reward)}</span>
        <span class="mini">${shortValue(cell.action, 'Empty')}</span>
      `;
      btn.addEventListener('click', () => {
        activeCellId = id;
        buildMatrix();
        renderEditor();
      });
      row.appendChild(btn);
    }
    matrix.appendChild(row);
  }
}

function renderEditor() {
  const { p, tf } = cellMeta(activeCellId);
  const cell = state.cells[activeCellId] || { risk: '—', reward: '—', action: 'Empty', score: '', notes: '' };
  $('activeTitle').textContent = `${p.full} · ${tf.label}`;
  $('activeRole').textContent = tf.role;
  $('riskInput').value = cell.risk || '—';
  $('rewardInput').value = cell.reward || '—';
  $('actionInput').value = cell.action || 'Empty';
  $('scoreInput').value = cell.score || '';
  $('notesInput').value = cell.notes || '';
}

function wireEditor() {
  ['riskInput', 'rewardInput', 'actionInput', 'scoreInput', 'notesInput'].forEach(id => {
    $(id).addEventListener('input', () => {
      state.cells[activeCellId] = {
        risk: $('riskInput').value,
        reward: $('rewardInput').value,
        action: $('actionInput').value,
        score: $('scoreInput').value,
        notes: $('notesInput').value,
      };
      saveState();
      buildMatrix();
    });
  });
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
  if (!items.length) { list.innerHTML = '<div class="micro">هنوز چیزی ذخیره نشده.</div>'; return; }
  list.innerHTML = '';
  for (const item of items) {
    const div = document.createElement('article');
    div.className = 'snapshot-item';
    const title = `${item.state?.symbol || 'Symbol'} · ${item.state?.finalBias || 'Bias'} · ${item.state?.finalAction || 'Watch'}`;
    const meta = new Date(item.createdAt).toLocaleString('fa-IR');
    div.innerHTML = `
      <div class="snapshot-title">${title}</div>
      <div class="snapshot-meta">${meta}</div>
      <div class="snapshot-actions">
        <button type="button" data-load="${item.id}">Load</button>
        <button type="button" data-export="${item.id}">Export</button>
        <button type="button" data-delete="${item.id}">Delete</button>
      </div>`;
    list.appendChild(div);
  }
  list.querySelectorAll('[data-load]').forEach(btn => btn.addEventListener('click', () => {
    const found = getSnapshots().find(x => x.id === btn.dataset.load);
    if (!found?.state) return;
    state = normalizeState(JSON.stringify(found.state));
    saveState();
    bindCurrentValuesOnly();
    buildMatrix(); renderEditor();
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

function bindCurrentValuesOnly() {
  $('symbolInput').value = state.symbol || '';
  $('sessionInput').value = state.session || '';
  $('globalContext').value = state.globalContext || '';
  $('finalBias').value = state.finalBias || 'نامشخص';
  $('finalAction').value = state.finalAction || 'Watch';
  $('finalNotes').value = state.finalNotes || '';
}

function wireActions() {
  $('saveSnapshotBtn').addEventListener('click', () => {
    const items = getSnapshots();
    items.push({ id: `${Date.now()}`, createdAt: new Date().toISOString(), state: JSON.parse(JSON.stringify(state)) });
    saveSnapshots(items);
    renderSnapshots();
  });
  $('exportBtn').addEventListener('click', () => {
    downloadJson(`alpha-lens-minimal-${Date.now()}.json`, { exportedAt: new Date().toISOString(), state, snapshots: getSnapshots() });
  });
  $('importInput').addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const obj = JSON.parse(await file.text());
      state = normalizeState(JSON.stringify(obj.state || obj));
      if (Array.isArray(obj.snapshots)) saveSnapshots(obj.snapshots);
      saveState(); bindCurrentValuesOnly(); buildMatrix(); renderEditor(); renderSnapshots();
    } catch (_) { alert('JSON معتبر نیست.'); }
    finally { event.target.value = ''; }
  });
  $('clearSnapshotsBtn').addEventListener('click', () => {
    if (confirm('همه Snapshotها حذف شوند؟')) { saveSnapshots([]); renderSnapshots(); }
  });
  $('resetBtn').addEventListener('click', () => {
    if (confirm('فرم فعلی ریست شود؟')) {
      state = makeDefaultState(); saveState(); bindCurrentValuesOnly(); buildMatrix(); renderEditor();
    }
  });
}

async function registerSW() {
  if ('serviceWorker' in navigator) {
    try { await navigator.serviceWorker.register('./sw.js'); }
    catch (err) { console.warn('Service worker registration failed', err); }
  }
}

bindTopInputs();
buildMatrix();
renderEditor();
wireEditor();
wireActions();
renderSnapshots();
saveState();
registerSW();
