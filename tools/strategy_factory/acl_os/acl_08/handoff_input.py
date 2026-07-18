from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_object,verify_embedded_digest
from .errors import ContractError,IntegrityError
from .io import load_json,safe_relative
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS
from .schema_validation import validate_instance
REQUIRED={'handoff':'handoff/acl08_handoff.json','manifest':'output_manifest.json','receipt':'validation_receipt.json','binding':'binding/acl06_binding.json','validation':'validation/validation_run.json','decisions':'decisions/validation_decision_bundle.json','matrix':'gates/gate_matrix.json','events':'events/validation_event_ledger.json','provenance':'lineage/validation_provenance_graph.json','registry':'policy/gate_registry_snapshot.json','policy':'policy/validation_policy_snapshot.json','diagnostic':'reports/diagnostic_isolation_report.json','security':'reports/security_boundary_report.json','integrity':'reports/integrity_report.json'}
DIGEST_FIELDS={'handoff':'handoff_digest','receipt':'receipt_digest','binding':'binding_digest','validation':'validation_run_digest','decisions':'decision_bundle_digest','matrix':'gate_matrix_digest','events':'ledger_digest','provenance':'graph_digest','registry':'registry_digest','policy':'policy_digest','diagnostic':'report_digest','security':'report_digest','integrity':'report_digest'}
def _sem(doc:dict,field:str,label:str):
    if not verify_embedded_digest(doc,field): raise IntegrityError(f'invalid {label} digest')
def _verify_events(doc:dict)->bool:
    prev='GENESIS'; rows=doc.get('events',[])
    if doc.get('event_count')!=len(rows): return False
    for i,row in enumerate(rows,1):
        if row.get('sequence')!=i or row.get('previous_event_digest')!=prev: return False
        if row.get('event_digest')!=digest_object({k:v for k,v in row.items() if k!='event_digest'}): return False
        prev=row['event_digest']
    return doc.get('terminal_event_digest')==prev and doc.get('ledger_digest')==digest_object({k:v for k,v in doc.items() if k!='ledger_digest'})
def load_acl07_bundle(root:Path)->dict[str,Any]:
    root=root.resolve(); marker=root/'.acl07_generated_root'
    if not marker.is_file() or marker.is_symlink(): raise ContractError('ACL07 generated-root marker missing')
    docs={k:load_json(safe_relative(root,v)) for k,v in REQUIRED.items()}
    h=docs['handoff']; validate_instance('acl07_handoff_input',h)
    if h['handoff_type']!=HANDOFF_IN: raise ContractError('wrong ACL07 handoff type')
    for k,f in DIGEST_FIELDS.items(): _sem(docs[k],f,k)
    if not verify_output_manifest(root,docs['manifest']): raise IntegrityError('ACL07 output manifest invalid')
    if docs['receipt']['output_manifest_digest']!=docs['manifest']['manifest_digest'] or docs['receipt']['acl08_handoff_digest']!=h['handoff_digest']: raise IntegrityError('ACL07 receipt binding invalid')
    if set(h['required_acl08_actions'])!=REQUIRED_UPSTREAM_ACTIONS or set(h['forbidden_acl08_actions'])!=FORBIDDEN_UPSTREAM_ACTIONS: raise ContractError('ACL07 action contract changed')
    if h['alpha_claim_allowed'] or h['live_order_submission_allowed'] or h['capital_activation_allowed']: raise ContractError('ACL07 authority escalation')
    if docs['validation'].get('state')!='COMPLETED_NON_PROMOTIONAL': raise ContractError('ACL07 validation not safely completed')
    if any(docs['decisions'].get(k) is not False for k in ['alpha_claim_allowed','promotion_allowed','live_order_submission_allowed','capital_activation_allowed']): raise ContractError('ACL07 decision bundle authority changed')
    if docs['provenance'].get('research_results_mutated') is not False or docs['provenance'].get('diagnostic_lane_promoted') is not False or docs['provenance'].get('execution_authority_granted') is not False: raise IntegrityError('ACL07 provenance safety invalid')
    if not _verify_events(docs['events']): raise IntegrityError('ACL07 event chain invalid')
    bindings={'validation_run_digest':('validation','validation_run_digest'),'decision_bundle_digest':('decisions','decision_bundle_digest'),'gate_matrix_digest':('matrix','gate_matrix_digest'),'event_ledger_digest':('events','ledger_digest'),'provenance_graph_digest':('provenance','graph_digest')}
    for hf,(key,field) in bindings.items():
        if h[hf]!=docs[key][field]: raise IntegrityError(f'handoff binding mismatch: {hf}')
    decision_files=[]; gates_by_setup={}
    for row in docs['decisions']['decisions']:
        dp=load_json(safe_relative(root,f"decisions/candidates/{row['setup_id']}.json")); _sem(dp,'decision_digest',row['setup_id'])
        if dp['decision_digest']!=row['decision_digest'] or dp!=row: raise IntegrityError('candidate decision file mismatch')
        gp=load_json(safe_relative(root,f"gates/candidates/{row['setup_id']}.json")); _sem(gp,'candidate_gate_digest',row['setup_id'])
        if gp['setup_id']!=row['setup_id'] or gp['candidate_id']!=row['candidate_id']: raise IntegrityError('candidate gate identity mismatch')
        mapped={g['gate_id']:g['gate_result_digest'] for g in gp['gates']}
        if mapped!=row['gate_result_digests']: raise IntegrityError('candidate gate digest mapping mismatch')
        for g in gp['gates']: _sem(g,'gate_result_digest',g['gate_id'])
        decision_files.append(dp); gates_by_setup[row['setup_id']]=gp
    if len(decision_files)!=docs['decisions']['candidate_count'] or len(gates_by_setup)!=docs['matrix']['candidate_count']: raise IntegrityError('ACL07 candidate coverage mismatch')
    if sorted(x['candidate_gate_digest'] for x in gates_by_setup.values())!=sorted(docs['matrix']['candidate_gate_digests']): raise IntegrityError('ACL07 gate matrix coverage mismatch')
    material={'handoff_digest':h['handoff_digest'],'validation_id':h['validation_id'],'decision_bundle_digest':docs['decisions']['decision_bundle_digest'],'gate_matrix_digest':docs['matrix']['gate_matrix_digest'],'decision_digests':sorted(x['decision_digest'] for x in decision_files),'candidate_gate_digests':sorted(x['candidate_gate_digest'] for x in gates_by_setup.values())}
    return {**docs,'candidate_decisions':sorted(decision_files,key=lambda x:x['setup_id']),'gates_by_setup':gates_by_setup,'bundle_digest':digest_object(material),'root':root}
