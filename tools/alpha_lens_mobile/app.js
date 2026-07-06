const VERSION = 'ultra4';
const PERSPECTIVES = [
  { key:'hook_bullish', label:'هوک\nصعودی', full:'هوک صعودی', dir:'bull', mode:'Hook' },
  { key:'rally_bullish', label:'رالی\nصعودی', full:'رالی صعودی', dir:'bull', mode:'Rally' },
  { key:'hook_bearish', label:'هوک\nنزولی', full:'هوک نزولی', dir:'bear', mode:'Hook' },
  { key:'rally_bearish', label:'رالی\nنزولی', full:'رالی نزولی', dir:'bear', mode:'Rally' },
];
const TFS = [
  {key:'1h', label:'1H', role:'Context'},
  {key:'10m', label:'10M', role:'Zone'},
  {key:'1m', label:'1M', role:'Entry'},
];
const STORAGE_KEY='alpha_lens_ultra4_state';
const SNAP_KEY='alpha_lens_ultra4_snaps';
const OLD_KEYS=['alpha_lens_matrix_minimal_v2','alpha_lens_matrix_v1'];
const $=id=>document.getElementById(id);
let active='hook_bullish__1h';
let state=loadState();
function defaultCells(){const cells={};for(const p of PERSPECTIVES){for(const t of TFS){cells[`${p.key}__${t.key}`]={risk:'—',reward:'—',action:'Empty',score:'',notes:''}}}return cells}
function baseState(){return{symbol:'XAUUSD',session:'',finalBias:'نامشخص',globalContext:'',finalAction:'Watch',finalNotes:'',cells:defaultCells(),updatedAt:new Date().toISOString()}}
function normalize(raw){const b=baseState();let p={};try{p=raw?JSON.parse(raw):{}}catch(e){}return{...b,...p,cells:{...b.cells,...(p.cells||{})}}}
function loadState(){let raw=localStorage.getItem(STORAGE_KEY);if(!raw){for(const k of OLD_KEYS){raw=localStorage.getItem(k);if(raw)break}}return normalize(raw)}
function save(){state.updatedAt=new Date().toISOString();localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}
function meta(id){const [pk,tk]=id.split('__');return{p:PERSPECTIVES.find(x=>x.key===pk),t:TFS.find(x=>x.key===tk)}}
function short(v){if(!v||v==='Empty')return '—';return {'Medium':'M','Low':'L','High':'H','Open':'O','Wait for Child':'Wait','Limit Ready':'Limit','No Trade':'No'}[v]||v}
function actionClass(a){if(a==='Limit Ready')return 'limit';if(a==='No Trade')return 'no';if(a==='Wait for Child')return 'wait';if(a==='Manage')return 'manage';return ''}
function renderMatrix(){const body=$('matrixBody');body.innerHTML='';for(const p of PERSPECTIVES){const tr=document.createElement('tr');const name=document.createElement('td');name.className=`row-name ${p.dir}`;name.innerHTML=p.label.replace('\n','<br>');tr.appendChild(name);for(const t of TFS){const id=`${p.key}__${t.key}`;const c=state.cells[id]||{};const td=document.createElement('td');const btn=document.createElement('button');btn.type='button';btn.className=`cell ${p.dir} ${id===active?'active':''} ${actionClass(c.action)}`;btn.innerHTML=`<span class="score">${c.score||'—'}</span><span class="line">R:${short(c.risk)} · W:${short(c.reward)}</span><span class="act">${short(c.action)}</span>`;btn.onclick=()=>{active=id;renderMatrix();renderEditor()};td.appendChild(btn);tr.appendChild(td)}body.appendChild(tr)}}
function renderEditor(){const {p,t}=meta(active);const c=state.cells[active]||{};$('activeTitle').textContent=`${p.full} · ${t.label}`;$('activeRole').textContent=t.role;$('riskInput').value=c.risk||'—';$('rewardInput').value=c.reward||'—';$('actionInput').value=c.action||'Empty';$('scoreInput').value=c.score||'';$('notesInput').value=c.notes||''}
function bind(){['symbolInput','sessionInput','finalBias','globalContext','finalAction','finalNotes'].forEach(id=>{$(id).value=state[id.replace('Input','')]||state[id]||''});$('symbolInput').value=state.symbol;$('sessionInput').value=state.session;$('globalContext').value=state.globalContext;$('finalBias').value=state.finalBias;$('finalAction').value=state.finalAction;$('finalNotes').value=state.finalNotes;const map={symbolInput:'symbol',sessionInput:'session',globalContext:'globalContext',finalBias:'finalBias',finalAction:'finalAction',finalNotes:'finalNotes'};Object.entries(map).forEach(([id,key])=>$(id).addEventListener('input',e=>{state[key]=e.target.value;save()}));['riskInput','rewardInput','actionInput','scoreInput','notesInput'].forEach(id=>$(id).addEventListener('input',()=>{state.cells[active]={risk:$('riskInput').value,reward:$('rewardInput').value,action:$('actionInput').value,score:$('scoreInput').value,notes:$('notesInput').value};save();renderMatrix()}));$('resetBtn').onclick=()=>{if(confirm('همه داده‌های صفحه پاک شود؟')){state=baseState();save();bindValues();renderMatrix();renderEditor()}};$('exportBtn').onclick=()=>download(`alpha-lens-${new Date().toISOString().slice(0,10)}.json`,state);$('saveSnapshotBtn').onclick=saveSnapshot;$('clearSnapshotsBtn').onclick=()=>{if(confirm('همه snapshotها حذف شوند؟')){localStorage.setItem(SNAP_KEY,'[]');renderSnaps()}};$('importInput').addEventListener('change',importJson)}
function bindValues(){$('symbolInput').value=state.symbol;$('sessionInput').value=state.session;$('globalContext').value=state.globalContext;$('finalBias').value=state.finalBias;$('finalAction').value=state.finalAction;$('finalNotes').value=state.finalNotes}
function download(name,data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();URL.revokeObjectURL(url)}
function snaps(){try{return JSON.parse(localStorage.getItem(SNAP_KEY)||'[]')}catch(e){return[]}}
function renderSnaps(){const list=$('snapshotsList');const items=snaps().sort((a,b)=>(b.createdAt||'').localeCompare(a.createdAt||''));if(!items.length){list.innerHTML='<div style="padding-top:8px">هنوز snapshot نداری.</div>';return}list.innerHTML='';for(const it of items){const div=document.createElement('div');div.className='snapshot';div.innerHTML=`<strong>${it.state?.symbol||'Symbol'} · ${it.state?.finalBias||'Bias'} · ${it.state?.finalAction||'Action'}</strong><small>${new Date(it.createdAt).toLocaleString('fa-IR')}</small><div class="snap-row"><button data-load="${it.id}">Load</button><button data-export="${it.id}">Export</button><button data-del="${it.id}">Delete</button></div>`;list.appendChild(div)}list.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>{const it=snaps().find(x=>x.id===b.dataset.load);if(it){state=normalize(JSON.stringify(it.state));save();bindValues();renderMatrix();renderEditor()}});list.querySelectorAll('[data-export]').forEach(b=>b.onclick=()=>{const it=snaps().find(x=>x.id===b.dataset.export);if(it)download(`alpha-lens-snap-${it.id}.json`,it)});list.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{localStorage.setItem(SNAP_KEY,JSON.stringify(snaps().filter(x=>x.id!==b.dataset.del)));renderSnaps()})}
function saveSnapshot(){const items=snaps();items.push({id:Date.now().toString(36),createdAt:new Date().toISOString(),version:VERSION,state});localStorage.setItem(SNAP_KEY,JSON.stringify(items));renderSnaps()}
function importJson(e){const file=e.target.files?.[0];if(!file)return;const r=new FileReader();r.onload=()=>{state=normalize(r.result);save();bindValues();renderMatrix();renderEditor()};r.readAsText(file);e.target.value=''}
function registerSW(){if('serviceWorker'in navigator){navigator.serviceWorker.register('./sw.js?v=ultra4').catch(()=>{})}}
bind();bindValues();renderMatrix();renderEditor();renderSnaps();registerSW();
