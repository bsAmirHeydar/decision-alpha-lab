from __future__ import annotations
import re
from pathlib import Path
from .canonical import digest_object

PATTERNS={
 'order_api':r'\b(OrderSend|CTrade|PositionOpen|PositionModify|PositionClose|\bBuy\s*\(|\bSell\s*\()',
 'drawing_api':r'\b(ObjectCreate|ObjectSet|ObjectDelete|ObjectsDeleteAll|PlotIndexSet|SetIndexBuffer)',
 'timeframe_api':r'\b(CopyRates|CopyBuffer|iBarShift|iTime|iOpen|iHigh|iLow|iClose|PERIOD_[A-Z0-9]+|timeframe)',
 'session_api':r'\b(RTH|PREMARKET|AFTERMARKET|SESSION|DST|NEW_YORK|NewYork|TimeGMT|TimeTradeServer)',
 'file_io':r'\b(FileOpen|FileRead|FileWrite|open\s*\(|read_text|write_text|read_csv|to_csv)',
 'network_api':r'\b(WebRequest|requests\.|urllib\.|httpx\.|socket\.)',
 'timer_api':r'\b(EventSetTimer|EventSetMillisecondTimer|OnTimer|Timer)',
 'global_state':r'\b(GlobalVariable|static\s+|global\s+|singleton|cache)',
 'current_bar':r'\b(shift\s*==\s*0|\[\s*0\s*\]|current_bar|bar0|rates\[0\])',
 'closed_bar':r'\b(shift\s*==\s*1|\[\s*1\s*\]|closed_bar|previous_bar|rates\[1\])',
 'randomness':r'\b(MathRand|random\.|randint|uuid4|secrets\.)',
 'wall_clock':r'\b(TimeCurrent|datetime\.now|utcnow|time\.time)',
 'dynamic_exec':r'\b(eval\s*\(|exec\s*\(|shell\s*=\s*True|subprocess\.)',
}
CALLBACKS=['OnInit','OnDeinit','OnTick','OnTimer','OnCalculate','OnChartEvent','OnTradeTransaction','main']

def profile(repo_root: Path, identity: dict):
    rel=identity['source_artifact_path'];p=repo_root/rel
    data=p.read_bytes() if p.is_file() else b''
    text='';binary=False
    try: text=data.decode('utf-8')
    except UnicodeDecodeError:
        try: text=data.decode('utf-8-sig')
        except UnicodeDecodeError: binary=True
    flags={k:bool(re.search(v,text,re.I|re.M)) if not binary else False for k,v in PATTERNS.items()}
    callbacks=[x for x in CALLBACKS if re.search(r'\b'+re.escape(x)+r'\s*\(',text)] if not binary else []
    includes=len(re.findall(r'(?m)^\s*(?:#include|from\s+\S+\s+import|import\s+)',text)) if not binary else 0
    funcs=len(re.findall(r'(?m)^\s*(?:def\s+\w+\s*\(|(?:bool|void|int|long|double|string|datetime|ENUM_\w+|[A-Z]\w+)\s+\w+\s*\()',text)) if not binary else 0
    risk=0
    weights={'order_api':100,'network_api':90,'dynamic_exec':80,'file_io':35,'global_state':30,'timer_api':25,'current_bar':20,'session_api':20,'timeframe_api':15,'drawing_api':10,'randomness':25,'wall_clock':15}
    for k,v in flags.items(): risk+=weights.get(k,0) if v else 0
    risk=min(risk,100)
    obj={'schema_version':'1.0.0','identity_id':identity['identity_id'],'source_artifact_path':rel,
         'source_artifact_sha256':identity['source_artifact_sha256'],'file_exists':p.is_file(),
         'binary_or_unreadable':binary,'size_bytes':len(data),'line_count':text.count('\n')+1 if text else 0,
         'include_or_import_count':includes,'function_count_estimate':funcs,'callbacks':callbacks,
         'capabilities':flags,'characterization_risk_score':risk,'static_profile_is_behavioral_proof':False,
         'profile_digest':None}
    obj['profile_digest']=digest_object(obj,'profile_digest');return obj
