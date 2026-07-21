from __future__ import annotations
import re
from pathlib import Path
from .canonical import file_digest, stable_id
from .constants import EXCLUDED_PARTS, TEST_PARTS, VISUAL_SOURCE_SUFFIXES
from .models import VisualSite
from .ownership import infer_owner, infer_source_event
from .patterns import CALL_TOKENS, REPORT_TOKENS, extract_balanced_call, nearest_function, split_arguments

class VisualSourceScanner:
    def __init__(self, repo_root: Path): self.repo_root=repo_root

    def source_files(self) -> list[Path]:
        result=[]
        for path in self.repo_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in VISUAL_SOURCE_SUFFIXES: continue
            rel=path.relative_to(self.repo_root)
            if any(part.lower() in EXCLUDED_PARTS for part in rel.parts): continue
            if rel.parts and rel.parts[0] in {"registry", "docs"}: continue
            result.append(path)
        return sorted(result, key=lambda p: p.relative_to(self.repo_root).as_posix().lower())

    def scan(self) -> tuple[list[VisualSite], list[dict], list[dict]]:
        sites=[]; source_rows=[]; delete_rows=[]
        for path in self.source_files():
            text=path.read_text(encoding="utf-8", errors="replace")
            if not any(token in text for token in (*CALL_TOKENS, *REPORT_TOKENS, "ObjectDelete", "ObjectsDeleteAll")): continue
            rel=path.relative_to(self.repo_root).as_posix(); digest=file_digest(path)
            lines=text.splitlines(); active=self._active_status(rel)
            source_rows.append({"source_path":rel,"source_digest":digest,"active_status":active,"visual_api_tokens":sorted({t for t in (*CALL_TOKENS,*REPORT_TOKENS,"ObjectDelete","ObjectsDeleteAll") if t in text})})
            for token in CALL_TOKENS:
                start=0
                while True:
                    idx=text.find(token+"(",start)
                    if idx<0: break
                    parsed=extract_balanced_call(text,idx)
                    if not parsed: break
                    raw,end=parsed; args=split_arguments(raw); line=text.count("\n",0,idx)+1
                    function=nearest_function(lines,max(0,line-1)); owner,subsystem=infer_owner(rel)
                    surface="CHART_OBJECT" if token=="ObjectCreate" else "INDICATOR_BUFFER"
                    if token=="ObjectCreate":
                        chart=args[0] if len(args)>0 else "UNKNOWN"; name=args[1] if len(args)>1 else "UNKNOWN"; obj=args[2] if len(args)>2 else "UNKNOWN_OBJECT_TYPE"
                    else:
                        chart="INDICATOR_WINDOW"; name=f"BUFFER_INDEX_{args[0] if args else 'UNKNOWN'}"; obj="INDICATOR_BUFFER"
                    event,event_status,event_evidence=infer_source_event(rel,surface); blockers=[]
                    if event_status=="BLOCKED": blockers.append(stable_id("VISBLOCK",rel,line,"SOURCE_EVENT"))
                    site=VisualSite(stable_id("VISOBJ",rel,line,token,obj,name),rel,digest,line,function,surface,obj,name,chart,tuple(args),active,owner,subsystem,event,event_status,event_evidence,tuple(blockers))
                    sites.append(site); start=end
            if path.suffix.lower()==".py":
                for line_no,line_text in enumerate(lines,1):
                    candidates=[token_name for token_name in REPORT_TOKENS if token_name in line_text]
                    lowered=line_text.lower()
                    if "write_text" in line_text and any(marker in lowered for marker in (".html", "report", "dashboard", "projection")):
                        candidates.append("write_text_report")
                    for token_name in candidates:
                        if not line_text.lstrip().startswith(("def ","#")):
                            owner,subsystem=infer_owner(rel); event,status,evidence=infer_source_event(rel,"REPORT_PROJECTION")
                            name=line_text.strip()[:180]
                            sites.append(VisualSite(stable_id("VISOBJ",rel,line_no,"REPORT",token_name,name),rel,digest,line_no,nearest_function(lines,line_no-1),"REPORT_PROJECTION",token_name.upper(),name,"REPORT_OUTPUT",(line_text.strip(),),active,owner,subsystem,event,status,evidence,tuple()))
            for token_name in ("ObjectsDeleteAll","ObjectDelete"):
                start=0
                while True:
                    idx=text.find(token_name+"(",start)
                    if idx<0: break
                    parsed=extract_balanced_call(text,idx)
                    if not parsed: break
                    raw,end=parsed; args=split_arguments(raw); line=text.count("\n",0,idx)+1
                    delete_rows.append({"delete_site_id":stable_id("VISDEL",rel,line,token_name,raw),"source_path":rel,"source_digest":digest,"line":line,"function_name":nearest_function(lines,max(0,line-1)),"api":token_name,"arguments":args,"scope_classification":self._delete_scope(token_name,args),"active_status":active})
                    start=end
        unique={s.visual_object_id:s for s in sites}
        return list(sorted(unique.values(),key=lambda x:(x.source_path.lower(),x.line,x.visual_object_id))),source_rows,delete_rows

    @staticmethod
    def _active_status(path: str) -> str:
        lower=path.lower(); parts={x.lower() for x in Path(path).parts}
        if any(x in lower for x in ("selftest","tests/","/test_","migration/fixtures")) or parts & TEST_PARTS: return "TEST_OR_FIXTURE"
        if any(x in lower for x in ("archive/","deprecated/","legacy_snapshot")): return "ARCHIVE_ONLY"
        return "ACTIVE_OR_REFERENCED"

    @staticmethod
    def _delete_scope(api: str,args: list[str]) -> str:
        if api=="ObjectDelete": return "INDIVIDUAL_OBJECT"
        if len(args)<2: return "BROAD_CHART_DELETE_BLOCKING"
        prefix=args[1].strip()
        if prefix in {"",'""',"NULL","0"}: return "BROAD_CHART_DELETE_BLOCKING"
        return "PREFIX_SCOPED_DELETE_REVIEW_REQUIRED"
