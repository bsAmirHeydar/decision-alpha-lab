from __future__ import annotations
import re
from pathlib import Path, PurePosixPath
from .canonical import sha256_bytes

INC_RE=re.compile(r'^\s*#include\s*([<"])([^>"]+)[>"]',re.M)
CAPS={
 'ORDER_API':re.compile(r'\b(OrderSend|OrderSendAsync|CTrade|PositionOpen|PositionModify|PositionClose|Buy\s*\(|Sell\s*\()'),
 'DRAWING_API':re.compile(r'\b(ObjectCreate|ObjectSetInteger|ObjectSetDouble|ObjectSetString|ObjectDelete|ObjectsDeleteAll|ChartRedraw)\b'),
 'FILE_IO':re.compile(r'\b(FileOpen|FileRead|FileWrite|FileClose|FolderCreate|FileDelete|FileMove)\b'),
 'NETWORK_API':re.compile(r'\bWebRequest\b'),
 'TIMER_API':re.compile(r'\b(EventSetTimer|EventSetMillisecondTimer|EventKillTimer|OnTimer)\b'),
 'GLOBAL_VARIABLE_API':re.compile(r'\b(GlobalVariableSet|GlobalVariableGet|GlobalVariableDel|GlobalVariablesDeleteAll)\b'),
 'TIMEFRAME_ACCESS':re.compile(r'\b(PERIOD_[A-Z0-9_]+|iBarShift|CopyRates|CopyTime|iTime|iOpen|iHigh|iLow|iClose)\b'),
 'SESSION_OR_DST_TERMS':re.compile(r'\b(RTH|PREMARKET|PRE_MARKET|AFTERMARKET|AFTER_MARKET|NEW_YORK|DST|SESSION)\b',re.I),
 'CHART_CALLBACK':re.compile(r'\b(OnChartEvent|ChartID|ChartSetInteger|ChartGetInteger)\b'),
 'MULTI_SYMBOL_ACCESS':re.compile(r'\b(SymbolSelect|CopyTicks|CopyTicksRange|MarketBookAdd|MarketBookGet)\b'),
 'INDICATOR_BUFFER':re.compile(r'\b(SetIndexBuffer|CopyBuffer|IndicatorRelease)\b'),
 'PERSISTENT_STATE':re.compile(r'\b(FileOpen|GlobalVariableSet|GlobalVariableGet)\b'),
}

def _resolve_include(source: str, raw: str, quote: str, known: set[str]) -> tuple[str,str,list[str]]:
    raw=raw.replace('\\','/').lstrip('/')
    candidates=[]
    src_parent=PurePosixPath(source).parent
    if quote=='"': candidates.append((src_parent/PurePosixPath(raw)).as_posix())
    candidates += [raw, f'mql5/Include/{raw}', f'mql5/{raw}']
    unique=[]
    for c in candidates:
        while c.startswith('./'): c=c[2:]
        if c not in unique: unique.append(c)
    hits=[c for c in unique if c in known]
    if len(hits)==1: return 'RESOLVED_INTERNAL',hits[0],unique
    if len(hits)>1: return 'AMBIGUOUS_INTERNAL','',hits
    if quote=='<' or raw.startswith(('Trade/','Arrays/','Files/','Math/','Indicators/','Controls/','Expert/')):
        return 'EXTERNAL_PLATFORM_LIBRARY','',unique
    return 'UNRESOLVED','',unique

def scan(repo_root: Path, paths: list[str], known: set[str]) -> tuple[list[dict],list[dict],list[dict]]:
    edges=[]; caps=[]; entries=[]
    for source in paths:
        p=repo_root/source
        data=p.read_bytes(); text=data.decode('utf-8',errors='replace')
        if source.lower().endswith('.mq5'):
            entries.append({'path':source,'entry_point_type':'MQL5_COMPILE_UNIT','evidence':'FILE_EXTENSION_MQ5','authority_inferred':False})
        for m in INC_RE.finditer(text):
            status,resolved,candidates=_resolve_include(source,m.group(2).strip(),m.group(1),known)
            line=text.count('\n',0,m.start())+1
            edges.append({'source_path':source,'edge_type':'MQL5_INCLUDE','raw_target':m.group(2).strip(),'line_number':line,'resolution_status':status,'resolved_path':resolved,'resolution_candidates':candidates,'semantic_reachability_claimed':False})
        lines=text.splitlines()
        for kind,rx in CAPS.items():
            for m in rx.finditer(text):
                line=text.count('\n',0,m.start())+1
                token=m.group(1) if m.lastindex else m.group(0)
                caps.append({'path':source,'language':'MQL5','capability_kind':kind,'matched_token':token[:120],'line_number':line,'line_digest':sha256_bytes((lines[line-1] if line<=len(lines) else '').strip().encode('utf-8')),'risk_indicator_only':True,'live_authority_inferred':False})
    edges.sort(key=lambda x:(x['source_path'],x['line_number'],x['raw_target']))
    caps.sort(key=lambda x:(x['path'],x['line_number'],x['capability_kind'],x['matched_token']))
    return edges,caps,entries
