from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_bytes,digest_object,verify_embedded_digest
from .errors import ContractError,IntegrityError
from .io import load_json,safe_relative
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS
from .schema_validation import validate_instance

REQUIRED={'handoff':'handoff/acl07_handoff.json','manifest':'output_manifest.json','receipt':'research_receipt.json','binding':'binding/acl05_binding.json','dag':'plan/research_dag.json','run':'execution/research_run.json','task_receipts':'execution/task_receipt_set.json','resource':'execution/resource_accounting.json','bundle':'results/research_result_bundle.json','result_index':'results/research_result_index.json','object_index':'store/object_index.json','events':'events/research_event_ledger.json','provenance':'lineage/research_provenance_graph.json'}
DIGEST_FIELDS={'handoff':'handoff_digest','binding':'binding_digest','dag':'dag_digest','run':'research_run_digest','task_receipts':'receipt_set_digest','resource':'accounting_digest','bundle':'result_bundle_digest','result_index':'index_digest','object_index':'object_index_digest','events':'ledger_digest','provenance':'graph_digest','receipt':'receipt_digest'}

def _sem(doc:dict,field:str,label:str):
    if not verify_embedded_digest(doc,field): raise IntegrityError(f'invalid {label} digest')


def _verify_acl06_event_chain(doc:dict[str,Any])->bool:
    prev=None
    events=doc.get('events',[])
    if doc.get('event_count')!=len(events): return False
    for seq,row in enumerate(events,1):
        if row.get('sequence')!=seq or row.get('previous_event_digest')!=prev: return False
        body={k:v for k,v in row.items() if k!='event_digest'}
        if row.get('event_digest')!=digest_object(body): return False
        prev=row['event_digest']
    return True

def load_acl06_bundle(root:Path)->dict[str,Any]:
    root=root.resolve()
    marker=root/'.acl06_generated_root'
    if not marker.is_file() or marker.is_symlink(): raise ContractError('ACL06 generated-root marker missing')
    docs={k:load_json(safe_relative(root,v)) for k,v in REQUIRED.items()}
    h=docs['handoff']; validate_instance('acl06_handoff_input',h)
    if h['handoff_type']!=HANDOFF_IN: raise ContractError('wrong handoff type')
    for k,f in DIGEST_FIELDS.items(): _sem(docs[k],f,k)
    if not verify_output_manifest(root,docs['manifest']): raise IntegrityError('ACL06 output manifest invalid')
    if docs['receipt']['output_manifest_digest']!=docs['manifest']['manifest_digest'] or docs['receipt']['acl07_handoff_digest']!=h['handoff_digest']: raise IntegrityError('ACL06 receipt binding invalid')
    if set(h['required_acl07_actions'])!=REQUIRED_UPSTREAM_ACTIONS or set(h['forbidden_acl07_actions'])!=FORBIDDEN_UPSTREAM_ACTIONS: raise ContractError('ACL06 action contract changed')
    if h['live_order_submission_allowed'] or h['capital_activation_allowed']: raise ContractError('ACL06 authority escalation')
    if docs['run'].get('state')!='COMPLETED' or docs['run'].get('live_order_submission_allowed') or docs['run'].get('capital_activation_allowed'): raise ContractError('ACL06 run not safely completed')
    if docs['task_receipts'].get('all_success') is not True or docs['task_receipts'].get('receipt_count')!=docs['dag'].get('task_count'): raise IntegrityError('task receipt coverage invalid')
    if docs['resource'].get('within_budget') is not True or docs['resource'].get('budget_expansion_allowed') is not False or docs['resource'].get('task_count_charged')!=docs['dag'].get('task_count'): raise IntegrityError('resource accounting invalid')
    if docs['provenance'].get('reaches_frozen_batch') is not True or docs['provenance'].get('candidate_behavior_mutated') is not False: raise IntegrityError('ACL06 provenance safety invalid')
    if not _verify_acl06_event_chain(docs['events']): raise IntegrityError('ACL06 event chain invalid')
    bindings={'research_run_digest':('run','research_run_digest'),'dag_digest':('dag','dag_digest'),'result_bundle_digest':('bundle','result_bundle_digest'),'task_receipt_set_digest':('task_receipts','receipt_set_digest'),'resource_accounting_digest':('resource','accounting_digest'),'object_index_digest':('object_index','object_index_digest'),'event_ledger_digest':('events','ledger_digest'),'provenance_graph_digest':('provenance','graph_digest')}
    for hf,(key,field) in bindings.items():
        if h[hf]!=docs[key][field]: raise IntegrityError(f'handoff binding mismatch: {hf}')
    bundle=docs['bundle']
    if bundle['descriptive_only'] is not True or bundle['validation_status']!='NOT_RUN' or bundle['alpha_claim_allowed'] is not False: raise ContractError('upstream results are not descriptive-only')
    candidates=[]
    for row in bundle['candidate_results']:
        p=safe_relative(root,f"results/candidates/{row['setup_id']}.json")
        doc=load_json(p); _sem(doc,'candidate_result_digest',row['setup_id'])
        if doc['candidate_result_digest']!=row['candidate_result_digest']: raise IntegrityError('candidate result file mismatch')
        candidates.append(doc)
    if len(candidates)!=bundle['candidate_count']: raise IntegrityError('candidate count mismatch')
    segment_results=[]
    for rec in docs['object_index']['objects']:
        p=safe_relative(root/'store',rec['store_path'])
        if not p.is_file() or p.is_symlink(): raise IntegrityError(f"missing run object {rec['logical_id']}")
        payload=p.read_bytes()
        if len(payload)!=rec['size_bytes'] or digest_bytes(payload)!=rec['blob_digest']: raise IntegrityError(f"run object mismatch {rec['logical_id']}")
        if rec['artifact_class']=='EVALUATE_CANDIDATE_SEGMENT':
            doc=json.loads(payload); _sem(doc,'segment_result_digest','segment result'); segment_results.append(doc)
    if len(segment_results)!=len(candidates)*3: raise IntegrityError('segment result count mismatch')
    by_setup={}
    for s in segment_results: by_setup.setdefault(s['setup_id'],{})[s['segment']]=s
    for c in candidates:
        if set(by_setup.get(c['setup_id'],{}))!={'TRAIN','VALIDATION','TEST'}: raise IntegrityError('candidate missing segment evidence')
    material={'handoff_digest':h['handoff_digest'],'run_id':h['run_id'],'bundle_digest':bundle['result_bundle_digest'],'candidate_digests':sorted(c['candidate_result_digest'] for c in candidates),'segment_digests':sorted(s['segment_result_digest'] for s in segment_results)}
    return {**docs,'candidates':sorted(candidates,key=lambda x:x['setup_id']),'segments_by_setup':by_setup,'bundle_digest':digest_object(material),'root':root}
