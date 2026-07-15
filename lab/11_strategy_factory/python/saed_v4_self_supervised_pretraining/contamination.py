from __future__ import annotations
from collections import defaultdict
from .canonical import content_hash, stable_id
from .errors import ContaminationError, LeakageError
from .validation import scan_forbidden

CANARY_PREFIX='CANARY::'

def audit_contamination(records:list[dict],split_manifest:dict,token_streams:list[dict],canaries:list[str])->dict:
    issues=[]
    split_by_record={x['record_id']:x['split'] for x in split_manifest['assignments']}
    roots=defaultdict(set);hash_splits=defaultdict(set);contexts=defaultdict(set)
    for r in records:
        split=split_by_record.get(r['record_id'])
        if split is None: issues.append({"code":"MISSING_SPLIT","record_id":r['record_id']});continue
        roots[r['root_context_id']].add(split);contexts[r['context_id']].add(split)
        for h in r['source_hashes']: hash_splits[h].add(split)
        try: scan_forbidden(r)
        except LeakageError as e: issues.append({"code":"FORBIDDEN_INPUT","record_id":r['record_id'],"detail":str(e)})
    for root,splits in roots.items():
        if len(splits)>1: issues.append({"code":"ROOT_CROSS_SPLIT","root_context_id":root,"splits":sorted(splits)})
    for ctx,splits in contexts.items():
        if len(splits)>1: issues.append({"code":"CONTEXT_CROSS_SPLIT","context_id":ctx,"splits":sorted(splits)})
    for h,splits in hash_splits.items():
        if len(splits)>1: issues.append({"code":"SOURCE_HASH_CROSS_SPLIT","source_hash":h,"splits":sorted(splits)})
    token_set={t for s in token_streams for t in s['tokens']}
    canary_hits=sorted(set(canaries)&token_set)
    if canary_hits: issues.append({"code":"CANARY_MEMBERSHIP","tokens":canary_hits})
    payload={"phase":"SAED_V4_11","passed":not issues,"issues":issues,"issue_count":len(issues),"checks":{"identity_disjoint":True,"source_hash_disjoint":True,"forbidden_input_scan":True,"membership_canaries":True,"future_suffix_forbidden":True},"canary_count":len(canaries),"canary_hits":canary_hits}
    payload['audit_id']=stable_id('contaminationaudit',payload);payload['audit_hash']=content_hash(payload);return payload

def assert_clean(audit:dict)->None:
    if not audit.get('passed'): raise ContaminationError(f"contamination audit failed: {audit.get('issues')}")

def membership_audit(checkpoint:dict,canaries:list[str])->dict:
    vocab=set(checkpoint['vocabulary']);hits=sorted(vocab&set(canaries))
    payload={"phase":"SAED_V4_11","checkpoint_hash":checkpoint['checkpoint_hash'],"canary_count":len(canaries),"hits":hits,"passed":not hits,"method":"exact_vocabulary_membership_canary"}
    payload['audit_id']=stable_id('membershipaudit',payload);payload['audit_hash']=content_hash(payload);return payload
