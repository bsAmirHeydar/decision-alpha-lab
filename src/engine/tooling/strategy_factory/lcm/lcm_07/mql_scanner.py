from __future__ import annotations
import csv,hashlib,re
from pathlib import Path
from .canonical import sha256_bytes
from .errors import ScanError

FUNC_RE=re.compile(r"(?m)^[ \t]*(?:(?:static|inline|virtual|const)\s+)*(?P<ret>void|bool|int|long|double|float|string|datetime|color|uchar|uint|ulong|short|ushort|char|ENUM_[A-Z0-9_]+|[A-Za-z_][A-Za-z0-9_:<>]*)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\((?P<args>[^;{}]*)\)\s*(?:const\s*)?\{")
COMMENT_RE=re.compile(r"//.*?$|/\*.*?\*/",re.M|re.S)
KEYWORDS={"if","for","while","switch","catch"}
API_PATTERNS={
 "order_api":r"\b(OrderSend|CTrade|Buy\s*\(|Sell\s*\(|Position(?:Open|Modify|Close)|trade\.)",
 "file_write_api":r"\b(FileWrite|FileDelete|FileMove|FileFlush)\b",
 "file_read_api":r"\b(FileOpen|FileRead|FileIsExist)\b",
 "network_api":r"\b(WebRequest|Socket)",
 "object_mutation_api":r"\b(ObjectCreate|ObjectDelete|ObjectsDeleteAll|ObjectSet(?:Integer|Double|String)?)\b",
 "global_variable_api":r"\b(GlobalVariable(?:Set|Del|Temp|SetOnCondition))\b",
 "current_bar_access":r"\[[ ]*0[ ]*\]|\b(?:iClose|iOpen|iHigh|iLow|iTime)\s*\([^;\n]*,[ ]*0[ ]*\)",
 "session_or_dst":r"\b(NewYork|NY|DST|Session|RTH|PreMarket|AfterHours)\b",
 "timeframe_api":r"\b(PERIOD_[A-Z0-9_]+|ENUM_TIMEFRAMES|PeriodSeconds|iBarShift|CopyRates)\b",
}

def _protected(repo):
    roots=sorted((repo/"registry/history/lcm/classifications").glob("CLASSIFICATION_*/protection/protected_platform_assets.csv"))
    out=set()
    if roots:
        with roots[-1].open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f): out.add(r["artifact_path"])
    return out

def _extract(text):
    for m in FUNC_RE.finditer(text):
        if m.group("name") in KEYWORDS: continue
        start=m.end()-1; depth=0; i=start; quote=None; escape=False
        while i<len(text):
            c=text[i]
            if quote:
                if escape: escape=False
                elif c=="\\": escape=True
                elif c==quote: quote=None
            else:
                if c in ('"',"'"): quote=c
                elif c=="{": depth+=1
                elif c=="}":
                    depth-=1
                    if depth==0:
                        body=text[start:i+1]
                        line_start=text.count("\n",0,m.start())+1; line_end=text.count("\n",0,i+1)+1
                        yield m.group("ret"),m.group("name"),m.group("args").strip(),body,line_start,line_end
                        break
            i+=1

def _arg_types(args):
    if not args.strip(): return []
    parts=[];cur="";depth=0
    for c in args:
        if c in "(<[":depth+=1
        elif c in ")>]":depth=max(0,depth-1)
        if c=="," and depth==0:parts.append(cur.strip());cur=""
        else:cur+=c
    if cur.strip():parts.append(cur.strip())
    types=[]
    for p in parts:
        p=re.sub(r"\s*=.*$","",p).strip(); toks=p.split()
        types.append(" ".join(toks[:-1]) if len(toks)>1 else p)
    return types

def scan(repo:Path):
    protected=_protected(repo); records=[]; excluded=[]
    files=sorted(list((repo/"mql5").rglob("*.mqh"))+list((repo/"mql5").rglob("*.mq5")))
    for p in files:
        rel=p.relative_to(repo).as_posix()
        if rel in protected or any(x in rel for x in ("/ACL_OS/","/StrategyFactory/SAED/","/DecisionAlphaLab/StrategyFactory/SAED/")):
            excluded.append({"artifact_path":rel,"reason":"PROTECTED_PLATFORM_EXCLUDED"}); continue
        try:text=p.read_text(encoding="utf-8",errors="ignore")
        except OSError as e: raise ScanError(f"cannot read {rel}") from e
        file_sha=sha256_bytes(p.read_bytes())
        for ret,name,args,body,ls,le in _extract(text):
            clean=COMMENT_RE.sub("",body); normalized=re.sub(r"\s+","",clean)
            if len(normalized)<80 or len(normalized)>12000: continue
            flags={k:bool(re.search(v,body,re.I|re.M)) for k,v in API_PATTERNS.items()}
            records.append({"artifact_path":rel,"artifact_sha256":file_sha,"function_name":name,"return_type":ret,"parameter_text":args,"parameter_types":_arg_types(args),"parameter_arity":len(_arg_types(args)),"line_start":ls,"line_end":le,"body_length":len(body),"normalized_length":len(normalized),"normalized_body_sha256":"sha256:"+hashlib.sha256(normalized.encode()).hexdigest(),"flags":flags})
    return records,excluded
