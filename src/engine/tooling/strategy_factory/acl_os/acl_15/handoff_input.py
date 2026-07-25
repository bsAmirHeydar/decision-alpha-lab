from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest,with_digest
from .errors import IntegrityError
from .io import load_json
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS
def req(v:bool,code:str)->None:
    if not v: raise IntegrityError(code)
def load_acl14_bundle(root:Path)->dict[str,Any]:
    req((root/'.acl14_generated_root').is_file(),'ACL14_MARKER_MISSING')
    paths={'manifest':'output_manifest.json','receipt':'first_real_context_pilot_receipt.json','handoff':'handoff/acl15_handoff.json','run':'run/pilot_run.json','decision':'decision/pilot_readiness_decision.json','contract':'contract/first_real_context_pilot_contract.json','execution':'execution/pilot_execution_manifest.json','readiness':'assessment/pilot_readiness_matrix.json','events':'events/pilot_event_ledger.json','provenance':'lineage/pilot_provenance_graph.json'}
    d={k:load_json(root/v) for k,v in paths.items()}
    req(verify_output_manifest(root,d['manifest']),'ACL14_MANIFEST_INVALID')
    checks={'receipt':'receipt_digest','handoff':'handoff_digest','run':'pilot_run_digest','decision':'pilot_readiness_decision_digest','contract':'pilot_contract_digest','execution':'pilot_execution_manifest_digest','readiness':'readiness_matrix_digest','events':'ledger_digest','provenance':'graph_digest'}
    for k,f in checks.items(): req(verify_embedded_digest(d[k],f),f'ACL14_{k.upper()}_DIGEST_INVALID')
    h=d['handoff']
    req(h.get('handoff_type')==HANDOFF_IN,'ACL14_HANDOFF_TYPE_INVALID')
    req(set(h.get('required_acl15_actions',[]))==REQUIRED_UPSTREAM_ACTIONS,'ACL14_REQUIRED_ACTIONS_INVALID')
    req(set(h.get('forbidden_acl15_actions',[]))==FORBIDDEN_UPSTREAM_ACTIONS,'ACL14_FORBIDDEN_ACTIONS_INVALID')
    req(d['receipt'].get('output_manifest_digest')==d['manifest'].get('manifest_digest'),'ACL14_RECEIPT_MANIFEST_MISMATCH')
    req(d['receipt'].get('acl15_handoff_digest')==h.get('handoff_digest'),'ACL14_RECEIPT_HANDOFF_MISMATCH')
    req(h.get('pilot_contract_digest')==d['contract'].get('pilot_contract_digest'),'ACL14_HANDOFF_CONTRACT_MISMATCH')
    req(h.get('pilot_readiness_decision_digest')==d['decision'].get('pilot_readiness_decision_digest'),'ACL14_HANDOFF_DECISION_MISMATCH')
    req(h.get('pilot_execution_manifest_digest')==d['execution'].get('pilot_execution_manifest_digest'),'ACL14_HANDOFF_EXECUTION_MISMATCH')
    req(h.get('readiness_matrix_digest')==d['readiness'].get('readiness_matrix_digest'),'ACL14_HANDOFF_READINESS_MISMATCH')
    req(h.get('event_ledger_digest')==d['events'].get('ledger_digest'),'ACL14_HANDOFF_EVENT_MISMATCH')
    req(h.get('provenance_graph_digest')==d['provenance'].get('graph_digest'),'ACL14_HANDOFF_PROVENANCE_MISMATCH')
    req(h.get('pilot_execution_materialized') is False,'ACL14_EXECUTION_ESCALATION')
    req(h.get('prospective_evidence_present') is False,'ACL14_PROSPECTIVE_EVIDENCE_ESCALATION')
    req(d['execution'].get('execution_count')==0 and d['execution'].get('prospective_observation_rows')==0,'ACL14_EXECUTION_NOT_EMPTY')
    for field in ['validation_claim_allowed','alpha_claim_allowed','production_security_ready','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']:
        req(h.get(field) is False,f'ACL14_{field.upper()}_ESCALATION')
    binding=with_digest({'schema_version':'1.0.0','pilot_run_id':d['run']['pilot_run_id'],'pilot_contract_id':d['contract']['pilot_contract_id'],'acl14_handoff_digest':h['handoff_digest'],'acl14_manifest_digest':d['manifest']['manifest_digest'],'pilot_contract_digest':d['contract']['pilot_contract_digest'],'pilot_readiness_decision_digest':d['decision']['pilot_readiness_decision_digest'],'pilot_execution_manifest_digest':d['execution']['pilot_execution_manifest_digest'],'readiness_matrix_digest':d['readiness']['readiness_matrix_digest'],'pilot_readiness_state':h['pilot_readiness_decision'],'pilot_ready_non_capital':False,'pilot_execution_materialized':False,'prospective_evidence_present':False,'reference_design_only':True},'acl14_binding_digest')
    return {**d,'binding':binding}
