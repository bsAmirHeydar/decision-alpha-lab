const VERSION = 'studio10';
const PERSPECTIVES = [
  { key:'hook_bullish', label:'هوک صعودی', dir:'bull' },
  { key:'rally_bullish', label:'رالی صعودی', dir:'bull' },
  { key:'hook_bearish', label:'هوک نزولی', dir:'bear' },
  { key:'rally_bearish', label:'رالی نزولی', dir:'bear' },
];
const TFS = [
  {key:'1h', label:'۱س', long:'۱ ساعته', role:'کانتکست / زون مادر'},
  {key:'10m', label:'۱۰د', long:'۱۰ دقیقه', role:'زون میانی / قابل معامله'},
  {key:'1m', label:'۱د', long:'۱ دقیقه', role:'ورود دقیق / کاهش ریسک'},
];
const OPTIONS = {
  view: [
    ['Bullish','صعودی'],
    ['Bearish','نزولی'],
    ['Dual','دوطرفه'],
    ['Neutral','خنثی'],
  ],
  risk: [
    ['—','—'],
    ['Low','کم'],
    ['Medium','متوسط'],
    ['High','زیاد'],
  ],
  reward: [
    ['—','—'],
    ['Low','کم'],
    ['Medium','متوسط'],
    ['High','زیاد'],
    ['Open','باز'],
  ],
  action: [
    ['Empty','خالی'],
    ['Watch','رصد'],
    ['Wait for Child','زیرزون'],
    ['Limit Ready','لیمیت'],
    ['Manage','مدیریت'],
    ['No Trade','رد'],
  ]
};
const STORAGE_KEY='alpha_lens_studio10_state';
const SNAP_KEY='alpha_lens_studio10_snaps';
const OLD_KEYS=['alpha_lens_studio9_state','alpha_lens_studio8_state','alpha_lens_studio7_state','alpha_lens_studio6_state','alpha_lens_studio5_state'];
const $=id=>document.getElementById(id);
let active='hook_bullish__1h';
let activeTf='1h';
let touchStartX=null;
let state=loadState();

function nowIso(){ return new Date().toISOString(); }
function formatTime(d=new Date()){
  return d.toLocaleString('fa-IR',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});
}
function defaultCells(){
  const cells={};
  for(const p of PERSPECTIVES){
    for(const t of TFS){
      cells[`${p.key}__${t.key}`]={view:'Neutral',risk:'—',reward:'—',action:'Empty',score:'',notes:''};
    }
  }
  return cells;
}
function baseState(){
  return {symbol:'XAUUSD',session:'',finalBias:'نامشخص',globalContext:'',finalAction:'Watch',finalNotes:'',registeredAt:nowIso(),theme:'light',cells:defaultCells(),updatedAt:nowIso()};
}
function normalize(raw){
  const b=baseState(); let p={};
  try{ p=raw?JSON.parse(raw):{}; }catch(e){}
  const merged={...b,...p,cells:{...b.cells,...(p.cells||{})}};
  Object.keys(merged.cells).forEach(k=>{
    const cell = merged.cells[k] || {};
    merged.cells[k]={view:'Neutral',risk:'—',reward:'—',action:'Empty',score:'',notes:'',...cell};
  });
  if(!merged.registeredAt) merged.registeredAt = nowIso();
  return merged;
}
function loadState(){
  let raw=localStorage.getItem(STORAGE_KEY);
  if(!raw){ for(const k of OLD_KEYS){ raw=localStorage.getItem(k); if(raw) break; } }
  return normalize(raw);
}
function stamp(){ state.registeredAt=nowIso(); state.updatedAt=state.registeredAt; }
function save(){ stamp(); localStorage.setItem(STORAGE_KEY,JSON.stringify(state)); updateClock(); }
function meta(id){
  const [pk,tk]=id.split('__');
  return {p:PERSPECTIVES.find(x=>x.key===pk),t:TFS.find(x=>x.key===tk)};
}
function activePerspectiveKey(){ return active.split('__')[0]; }
function setActiveTf(tfKey){ activeTf=tfKey; active=`${activePerspectiveKey()}__${tfKey}`; renderAll(); }
function labelFor(group,value){ return (OPTIONS[group].find(x=>x[0]===value)||[])[1] || '—'; }
function riskShort(v){ return labelFor('risk',v); }
function rewardShort(v){ return labelFor('reward',v); }
function viewLabel(v){ return labelFor('view',v); }
function viewClass(v){
  if(v==='Bullish') return 'bull';
  if(v==='Bearish') return 'bear';
  if(v==='Dual') return 'dual';
  return 'neutral';
}
function actionShort(v){ return labelFor('action',v); }
function actionClass(a){
  if(a==='Limit Ready') return 'limit';
  if(a==='No Trade') return 'no';
  if(a==='Wait for Child') return 'wait';
  if(a==='Manage') return 'manage';
  if(a==='Watch') return 'watch';
  return 'empty';
}
function accentForCell(c,p){
  if(c?.view === 'Bullish') return 'bull';
  if(c?.view === 'Bearish') return 'bear';
  if(c?.view === 'Dual') return 'dual';
  if(p?.dir === 'bull') return 'bull';
  if(p?.dir === 'bear') return 'bear';
  return 'neutral';
}
function applyTheme(){
  const theme = state.theme === 'dark' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', theme);
  const btn=$('themeBtn');
  if(btn) btn.textContent = theme === 'dark' ? '☀' : '☾';
  const meta=document.querySelector('meta[name="theme-color"]');
  if(meta) meta.setAttribute('content', theme === 'dark' ? '#0e1114' : '#f5f1e8');
}
function applyAccent(){
  const {p}=meta(active);
  const c=state.cells[active] || {};
  document.documentElement.setAttribute('data-accent', accentForCell(c,p));
}
function updateClock(){
  const el=$('recordedAtInput');
  if(el) el.value = `زمان ثبت: ${formatTime(new Date())}`;
}
function renderTabs(){
  const el=$('tfTabs'); el.innerHTML='';
  TFS.forEach(tf=>{
    const b=document.createElement('button');
    b.type='button';
    b.className=`tf-tab ${activeTf===tf.key?'active':''}`;
    b.textContent=tf.label;
    b.title=tf.long;
    b.onclick=()=>setActiveTf(tf.key);
    el.appendChild(b);
  });
}
function renderSlides(){
  const wrap=$('slides'); wrap.innerHTML='';
  const tf=TFS.find(x=>x.key===activeTf) || TFS[0];
  const slide=document.createElement('section');
  slide.className='slide';
  slide.dataset.tf=tf.key;
  slide.innerHTML=`<div class="slide-head"><span class="slide-title">${tf.long}</span><span class="slide-sub">${tf.role}</span></div>`;
  const grid=document.createElement('div');
  grid.className='slide-grid';
  PERSPECTIVES.forEach(p=>{
    const id=`${p.key}__${tf.key}`;
    const c=state.cells[id]||{};
    const btn=document.createElement('button');
    btn.type='button';
    btn.className=`cell-card ${p.dir==='bull'?'bullish-lens':'bearish-lens'} ${id===active?'active':''}`;
    btn.innerHTML=`<div class="lens-name ${p.dir}">${p.label}</div><div class="cell-stack"><div class="topline"><span class="bias-chip ${viewClass(c.view)}">${viewLabel(c.view)}</span><span class="score">${c.score||'—'}</span></div><div class="meta-line">ریسک ${riskShort(c.risk)} · ریوارد ${rewardShort(c.reward)}</div><div class="act-line ${actionClass(c.action)}">${actionShort(c.action)}</div></div>`;
    btn.onclick=()=>{ active=id; activeTf=tf.key; renderAll(); };
    grid.appendChild(btn);
  });
  slide.appendChild(grid);
  wrap.appendChild(slide);
}
function renderSegmented(){
  const groups = [
    ['viewControl','view'],
    ['riskControl','risk'],
    ['rewardControl','reward'],
    ['actionControl','action'],
  ];
  const c=state.cells[active]||{};
  for(const [id,field] of groups){
    const el=$(id); el.innerHTML='';
    for(const [value,label] of OPTIONS[field]){
      const btn=document.createElement('button');
      btn.type='button';
      btn.className=`seg-btn ${(c[field]||defaultValue(field))===value?'active':''}`;
      btn.textContent=label;
      btn.onclick=()=>{
        state.cells[active]={view:'Neutral',risk:'—',reward:'—',action:'Empty',score:'',notes:'',...(state.cells[active]||{}),[field]:value};
        save();
        renderAll();
      };
      el.appendChild(btn);
    }
  }
}
function defaultValue(field){ return field==='view'?'Neutral':field==='action'?'Empty':'—'; }
function renderEditor(){
  const {p,t}=meta(active);
  const c=state.cells[active]||{};
  $('activeTitle').textContent=`${p.label} · ${t.long}`;
  $('activeRole').textContent=t.role;
  $('scoreInput').value=c.score||'';
  $('notesInput').value=c.notes||'';
  renderSegmented();
  applyAccent();
}
function bindValues(){
  $('symbolInput').value=state.symbol;
  $('sessionInput').value=state.session;
  $('globalContext').value=state.globalContext;
  $('finalBias').value=state.finalBias;
  $('finalAction').value=state.finalAction;
  $('finalNotes').value=state.finalNotes;
  updateClock();
}
function bind(){
  bindValues();
  const map={symbolInput:'symbol',sessionInput:'session',globalContext:'globalContext',finalBias:'finalBias',finalAction:'finalAction',finalNotes:'finalNotes'};
  Object.entries(map).forEach(([id,key])=>$(id).addEventListener('input',e=>{ state[key]=e.target.value; save(); }));
  ['scoreInput','notesInput'].forEach(id=>$(id).addEventListener('input',()=>{
    state.cells[active]={view:'Neutral',risk:'—',reward:'—',action:'Empty',score:'',notes:'',...(state.cells[active]||{}),score:$('scoreInput').value,notes:$('notesInput').value};
    save();
    renderSlides();
    renderTabs();
  }));
  $('themeBtn').onclick=()=>{ state.theme = state.theme === 'dark' ? 'light' : 'dark'; save(); applyTheme(); };
  $('resetBtn').onclick=()=>{
    if(confirm('همه داده‌های صفحه پاک شود؟')){
      state=baseState(); active='hook_bullish__1h'; activeTf='1h';
      save(); applyTheme(); renderAll();
    }
  };
  $('exportBtn').onclick=()=>{ save(); download(`alpha-lens-${new Date().toISOString().slice(0,10)}.json`,state); };
  $('saveSnapshotBtn').onclick=saveSnapshot;
  $('clearSnapshotsBtn').onclick=()=>{ if(confirm('همه اسنپ‌ها حذف شوند؟')){ localStorage.setItem(SNAP_KEY,'[]'); renderSnaps(); } };
  $('importInput').addEventListener('change',importJson);
  const slides=$('slides');
  slides.addEventListener('touchstart',e=>{ touchStartX=e.changedTouches[0].clientX; },{passive:true});
  slides.addEventListener('touchend',e=>{
    if(touchStartX===null) return;
    const dx=e.changedTouches[0].clientX - touchStartX;
    touchStartX=null;
    if(Math.abs(dx)<46) return;
    if(dx<0) goTf(1); else goTf(-1);
  },{passive:true});
}
function goTf(delta){
  const idx=TFS.findIndex(t=>t.key===activeTf);
  const next=Math.max(0,Math.min(TFS.length-1,idx+delta));
  if(next!==idx) setActiveTf(TFS[next].key);
}
function download(name,data){
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url; a.download=name; a.click();
  URL.revokeObjectURL(url);
}
function snaps(){ try{return JSON.parse(localStorage.getItem(SNAP_KEY)||'[]')}catch(e){return[]} }
function renderSnaps(){
  const list=$('snapshotsList');
  const items=snaps().sort((a,b)=>(b.createdAt||'').localeCompare(a.createdAt||''));
  if(!items.length){ list.innerHTML='<div style="padding-top:8px;color:var(--muted)">هنوز اسنپی ذخیره نشده.</div>'; return; }
  list.innerHTML='';
  for(const it of items){
    const div=document.createElement('div');
    div.className='snapshot';
    div.innerHTML=`<strong>${it.state?.symbol||'نماد'} · ${it.state?.finalBias||'سوگیری'} · ${labelFinalAction(it.state?.finalAction)}</strong><small>${new Date(it.createdAt).toLocaleString('fa-IR')}</small><div class="snap-row"><button data-load="${it.id}">بارگذاری</button><button data-export="${it.id}">خروجی</button><button data-del="${it.id}">حذف</button></div>`;
    list.appendChild(div);
  }
  list.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>{
    const it=snaps().find(x=>x.id===b.dataset.load);
    if(it){ state=normalize(JSON.stringify(it.state)); active='hook_bullish__1h'; activeTf='1h'; save(); applyTheme(); renderAll(); }
  });
  list.querySelectorAll('[data-export]').forEach(b=>b.onclick=()=>{
    const it=snaps().find(x=>x.id===b.dataset.export);
    if(it) download(`alpha-lens-snap-${it.id}.json`,it);
  });
  list.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{
    localStorage.setItem(SNAP_KEY,JSON.stringify(snaps().filter(x=>x.id!==b.dataset.del)));
    renderSnaps();
  });
}
function labelFinalAction(v){
  return ({'Watch':'رصد','Wait for Child':'نیاز به زیرزون','Limit Ready':'آماده لیمیت','Manage':'مدیریت','No Trade':'بدون معامله'})[v] || '—';
}
function saveSnapshot(){
  stamp();
  const snapshotState=JSON.parse(JSON.stringify(state));
  const items=snaps();
  items.push({id:Date.now().toString(36),createdAt:state.registeredAt,version:VERSION,state:snapshotState});
  localStorage.setItem(SNAP_KEY,JSON.stringify(items));
  save();
  renderSnaps();
}
function importJson(e){
  const file=e.target.files?.[0]; if(!file) return;
  const r=new FileReader();
  r.onload=()=>{
    state=normalize(r.result); active='hook_bullish__1h'; activeTf='1h';
    save(); applyTheme(); renderAll();
  };
  r.readAsText(file); e.target.value='';
}
function registerSW(){ if('serviceWorker' in navigator){ navigator.serviceWorker.register('./sw.js?v=studio10').catch(()=>{}); } }
function renderAll(){
  bindValues();
  renderTabs();
  renderSlides();
  renderEditor();
  renderSnaps();
}

bind(); applyTheme(); renderAll(); updateClock(); setInterval(updateClock,1000); registerSW();
