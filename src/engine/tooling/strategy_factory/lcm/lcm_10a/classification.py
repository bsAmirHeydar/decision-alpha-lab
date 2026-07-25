from __future__ import annotations
import re
from collections import defaultdict
from .canonical import digest_object, stable_id
from .models import SourceAnalysis
from .patterns import ORDER_MUTATION_CODES

def owner_for(path: str, classifications: dict[str,dict]) -> dict:
    row=classifications.get(path)
    if row:
        return {"code_owner_role":row.get("code_owner_role"),"semantic_owner_role":row.get("semantic_owner_role"),"owner_resolution_status":row.get("owner_resolution_status"),"ownership_is_human_approved":bool(row.get("ownership_is_human_approved")),"security_sensitive":bool(row.get("security_sensitive")),"security_reviewer_role":row.get("security_reviewer_role")}
    if path.startswith('mql5/'): return {"code_owner_role":"CODE_OWNER_MQL5_LEGACY","semantic_owner_role":"DOMAIN_OWNER_EXECUTION","owner_resolution_status":"ROLE_INFERRED_CLASSIFICATION_RECORD_MISSING","ownership_is_human_approved":False,"security_sensitive":True,"security_reviewer_role":"SECURITY_REVIEWER"}
    return {"code_owner_role":"CODE_OWNER_UNRESOLVED","semantic_owner_role":"DOMAIN_OWNER_UNRESOLVED","owner_resolution_status":"UNKNOWN","ownership_is_human_approved":False,"security_sensitive":False,"security_reviewer_role":None}

def treatment_atoms(analyses: list[SourceAnalysis], classifications: dict[str,dict], meta_factory) -> list[dict]:
    groups=defaultdict(list)
    for a in analyses:
        for hit in a.treatment_hits: groups[(a.path,hit.get('symbol_id'),hit['pattern_code'])].append((a,hit))
    out=[]
    for (path,sid,code),items in sorted(groups.items(), key=lambda item:(item[0][0], item[0][1] or "", item[0][2])):
        a=items[0][0]; evidence=[{k:h[k] for k in ('line_number','line_digest','excerpt')} for _,h in items]
        own=owner_for(path,classifications)
        body={**meta_factory(a.sha256),"treatment_atom_id":stable_id('TREATATOM',path,sid or 'TOP',code),"atom_type":code,"source_path":path,"source_sha256":a.sha256,"language":a.language,"symbol_id":sid,"symbol_name":items[0][1].get('symbol_name'),"mode_classes":a.mode_classes,"evidence_locations":evidence,"evidence_count":len(evidence),"owner":own,"semantic_status":"OBSERVED_STATIC_NOT_NORMALIZED","executable_rule_extracted":False,"source_move_performed":False,"source_delete_performed":False}
        out.append({**body,"atom_digest":digest_object(body)})
    return out

def execution_capabilities(analyses: list[SourceAnalysis], classifications: dict[str,dict], reachability: list[dict], meta_factory) -> list[dict]:
    reach_by_key={(r['source_path'],r['line_number'],r['capability_code']):r for r in reachability}
    groups=defaultdict(list)
    for a in analyses:
        for hit in a.capability_hits: groups[(a.path,hit.get('symbol_id'),hit['pattern_code'],hit['authority_class'])].append((a,hit))
    out=[]
    for (path,sid,code,authority),items in sorted(groups.items(), key=lambda item:(item[0][0], item[0][1] or "", item[0][2], item[0][3] or "")):
        a=items[0][0]; evidence=[]; states=[]
        for _,h in items:
            evidence.append({k:h[k] for k in ('line_number','line_digest','excerpt')})
            r=reach_by_key.get((path,h['line_number'],code))
            if r: states.append(r['reachability_state'])
        own=owner_for(path,classifications); symbol=(items[0][1].get('symbol_name') or '')
        hidden=bool(authority in {'SUBMIT_ORDER','MODIFY_POSITION','MODIFY_ORDER','CANCEL_ORDER','CLOSE_POSITION'} and symbol and not re.search(r'(trade|order|broker|execute|route|submit|open|close|modify|cancel)',symbol,re.I))
        body={**meta_factory(a.sha256),"capability_id":stable_id('EXECCAP',path,sid or 'TOP',code,authority),"capability_code":code,"authority_class":authority,"severity":items[0][1]['severity'],"source_path":path,"source_sha256":a.sha256,"language":a.language,"symbol_id":sid,"symbol_name":items[0][1].get('symbol_name'),"mode_classes":a.mode_classes,"evidence_locations":evidence,"evidence_count":len(evidence),"reachability_states":sorted(set(states)) or ['NOT_APPLICABLE_OR_UNKNOWN'],"owner":own,"hidden_authority_indicator":hidden,"authority_status":"OBSERVED_NOT_AUTHORIZED","live_order_authorized":False,"runtime_authorized":False,"capital_authorized":False,"source_move_performed":False,"source_delete_performed":False}
        out.append({**body,"capability_digest":digest_object(body)})
    return out

def risk_assumptions(analyses: list[SourceAnalysis], classifications: dict[str,dict], meta_factory) -> list[dict]:
    groups=defaultdict(list)
    for a in analyses:
        for hit in a.risk_hits: groups[(a.path,hit.get('symbol_id'),hit['pattern_code'])].append((a,hit))
    out=[]
    for (path,sid,code),items in sorted(groups.items(), key=lambda item:(item[0][0], item[0][1] or "", item[0][2])):
        a=items[0][0]; evidence=[{k:h[k] for k in ('line_number','line_digest','excerpt')} for _,h in items]
        own=owner_for(path,classifications)
        body={**meta_factory(a.sha256),"risk_assumption_id":stable_id('RISKASM',path,sid or 'TOP',code),"assumption_type":code,"source_path":path,"source_sha256":a.sha256,"language":a.language,"symbol_id":sid,"symbol_name":items[0][1].get('symbol_name'),"mode_classes":a.mode_classes,"evidence_locations":evidence,"evidence_count":len(evidence),"owner":own,"assumption_value":"STATIC_EXPRESSION_NOT_EVALUATED","symbol_specificity":"UNKNOWN","normalization_status":"NOT_NORMALIZED","behavior_change_performed":False}
        out.append({**body,"assumption_digest":digest_object(body)})
    return out

def authority_map(capabilities: list[dict], meta_factory) -> list[dict]:
    groups=defaultdict(list)
    for c in capabilities: groups[(c['source_path'],c.get('symbol_id'),c['authority_class'])].append(c)
    out=[]
    for (path,sid,authority),rows in sorted(groups.items(), key=lambda item:(item[0][0], item[0][1] or "", item[0][2] or "")):
        owner=rows[0]['owner']; codes=sorted({r['capability_code'] for r in rows}); hidden=any(r['hidden_authority_indicator'] for r in rows)
        blockers=[]
        if not owner['ownership_is_human_approved']: blockers.append('HUMAN_OWNER_APPROVAL_MISSING')
        if hidden: blockers.append('HIDDEN_AUTHORITY_WRAPPER')
        if authority in {'SUBMIT_ORDER','MODIFY_POSITION','MODIFY_ORDER','CANCEL_ORDER','CLOSE_POSITION'}: blockers.append('ORDER_CAPABLE_SOURCE_REQUIRES_LCM10B_BOUNDARY')
        body={**meta_factory(*(r['source_sha256'] for r in rows)),"authority_boundary_id":stable_id('AUTHBOUND',path,sid or 'TOP',authority),"source_path":path,"symbol_id":sid,"symbol_name":rows[0].get('symbol_name'),"authority_class":authority,"capability_ids":[r['capability_id'] for r in rows],"capability_codes":codes,"owner":owner,"hidden_authority_indicator":hidden,"blocker_codes":sorted(set(blockers)),"boundary_status":"BLOCKED_PENDING_LCM10B" if blockers else "OBSERVED_REFERENCE_ONLY","request_intent_authority":False,"submission_authority":False,"modify_authority":False,"cancel_authority":False,"reconcile_authority":False,"close_authority":False,"runtime_authority":False,"live_order_authority":False,"capital_authority":False}
        out.append({**body,"boundary_digest":digest_object(body)})
    return out
