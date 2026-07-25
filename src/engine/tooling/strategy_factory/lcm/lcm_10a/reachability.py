from __future__ import annotations
from collections import defaultdict, deque
from .canonical import digest_object, stable_id
from .models import SourceAnalysis, FunctionRecord
from .patterns import BROKER_CAPABILITY_CODES

def build_reachability(analyses: list[SourceAnalysis], lcm01_entry_paths: set[str], meta_factory) -> list[dict]:
    functions=[f for a in analyses for f in a.functions]
    by_id={f.symbol_id:f for f in functions}; by_name=defaultdict(list); by_path=defaultdict(list)
    for f in functions:
        by_name[f.name.split('::')[-1]].append(f); by_path[f.path].append(f)
    entry_ids=set()
    for f in functions:
        if f.entry_point_types: entry_ids.add(f.symbol_id)
        elif f.path in lcm01_entry_paths and f.name in {'main','OnTick','OnTimer','OnStart','run','execute'}: entry_ids.add(f.symbol_id)
    reverse=defaultdict(set)
    ambiguities=[]
    for f in functions:
        for call in f.calls:
            candidates=[x for x in by_path[f.path] if x.name.split('::')[-1]==call]
            if not candidates: candidates=by_name.get(call,[])
            if len(candidates)==1: reverse[candidates[0].symbol_id].add(f.symbol_id)
            elif len(candidates)>1: ambiguities.append((f.symbol_id,call,tuple(x.symbol_id for x in candidates)))
    roots_by_symbol=defaultdict(set)
    for entry in sorted(entry_ids):
        q=deque([entry]); seen={entry}
        while q:
            current=q.popleft(); roots_by_symbol[current].add(entry)
            f=by_id[current]
            for call in f.calls:
                candidates=[x for x in by_path[f.path] if x.name.split('::')[-1]==call]
                if not candidates: candidates=by_name.get(call,[])
                if len(candidates)==1 and candidates[0].symbol_id not in seen:
                    seen.add(candidates[0].symbol_id); q.append(candidates[0].symbol_id)
    records=[]
    for a in analyses:
        for hit in a.capability_hits:
            if hit['pattern_code'] not in BROKER_CAPABILITY_CODES: continue
            sid=hit.get('symbol_id'); root_ids=sorted(roots_by_symbol.get(sid,set())) if sid else []
            if root_ids: state='REACHABLE_FROM_STATIC_ENTRY'
            elif a.path in lcm01_entry_paths: state='FILE_ENTRY_REACHABILITY_UNKNOWN'
            elif sid: state='STATIC_ENTRY_NOT_RESOLVED'
            else: state='TOP_LEVEL_OR_MACRO_UNKNOWN'
            roots=[{"symbol_id":rid,"path":by_id[rid].path,"qualified_name":by_id[rid].qualified_name,"entry_point_types":list(by_id[rid].entry_point_types)} for rid in root_ids]
            body={**meta_factory(a.sha256, status="PASS" if state == "REACHABLE_FROM_STATIC_ENTRY" else "UNKNOWN"),"reachability_id":stable_id('REACH',a.path,hit['line_number'],hit['pattern_code'],sid or 'NONE'),"capability_code":hit['pattern_code'],"authority_class":hit['authority_class'],"source_path":a.path,"source_sha256":a.sha256,"line_number":hit['line_number'],"symbol_id":sid,"symbol_name":hit.get('symbol_name'),"reachability_state":state,"entry_roots":roots,"mode_classes":a.mode_classes,"static_only":True,"runtime_observed":False}
            records.append({**body, "reachability_digest": digest_object(body)})
    return sorted(records,key=lambda x:(x['source_path'],x['line_number'],x['capability_code']))
