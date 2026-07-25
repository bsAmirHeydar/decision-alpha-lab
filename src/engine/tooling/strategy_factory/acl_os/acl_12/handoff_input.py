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
def load_acl11_bundle(root:Path)->dict[str,Any]:
    req((root/'.acl11_generated_root').is_file(),'ACL11_MARKER_MISSING')
    paths={'manifest':'output_manifest.json','receipt':'runtime_custody_receipt.json','handoff':'handoff/acl12_handoff.json','run':'run/runtime_custody_run.json','decision':'custody/runtime_custody_decision.json','assessment':'parity/runtime_parity_assessment.json','generation':'runtime/runtime_generation_manifest.json','signing':'custody/signing_custody_plan.json','tcb':'security/runtime_trusted_computing_base.json','security':'security/security_boundary_report.json','events':'events/runtime_custody_event_ledger.json','provenance':'lineage/runtime_custody_provenance_graph.json','integrity':'reports/integrity_report.json'}
    d={k:load_json(root/v) for k,v in paths.items()}
    req(verify_output_manifest(root,d['manifest']),'ACL11_MANIFEST_INVALID')
    checks=[('receipt','receipt_digest'),('handoff','handoff_digest'),('run','runtime_custody_run_digest'),('decision','custody_decision_digest'),('assessment','assessment_digest'),('generation','generation_manifest_digest'),('signing','signing_plan_digest'),('tcb','tcb_digest'),('security','security_report_digest'),('events','ledger_digest'),('provenance','graph_digest'),('integrity','integrity_report_digest')]
    for key,field in checks: req(verify_embedded_digest(d[key],field),f'ACL11_{key.upper()}_DIGEST_INVALID')
    h=d['handoff']
    req(h.get('handoff_type')==HANDOFF_IN,'ACL11_HANDOFF_TYPE_INVALID')
    req(set(h.get('required_acl12_actions',[]))==REQUIRED_UPSTREAM_ACTIONS,'ACL11_REQUIRED_ACTIONS_INVALID')
    req(set(h.get('forbidden_acl12_actions',[]))==FORBIDDEN_UPSTREAM_ACTIONS,'ACL11_FORBIDDEN_ACTIONS_INVALID')
    req(h.get('runtime_candidate_count')==0,'ACL11_RUNTIME_CANDIDATE_COUNT_NOT_ZERO')
    req(d['run'].get('state')=='COMPLETED_NO_RUNTIME_GENERATION','ACL11_RUN_STATE_INVALID')
    req(d['decision'].get('decision')=='NON_EXECUTABLE_NO_RUNTIME_CANDIDATES','ACL11_CUSTODY_DECISION_INVALID')
    req(d['generation'].get('generation_count')==0 and d['generation'].get('generation_materialized') is False,'ACL11_GENERATION_MATERIALIZED')
    req(d['signing'].get('key_material_present') is False and d['signing'].get('signature_created') is False,'ACL11_SIGNING_ESCALATION')
    req(d['tcb'].get('production_tcb_verified') is False,'ACL11_PRODUCTION_TCB_CLAIMED')
    req(d['security'].get('passed') is True and d['integrity'].get('passed') is True,'ACL11_SECURITY_OR_INTEGRITY_FAILED')
    req(d['receipt'].get('output_manifest_digest')==d['manifest'].get('manifest_digest'),'ACL11_RECEIPT_MANIFEST_MISMATCH')
    req(d['receipt'].get('acl12_handoff_digest')==h.get('handoff_digest'),'ACL11_RECEIPT_HANDOFF_MISMATCH')
    req(h.get('custody_decision_digest')==d['decision'].get('custody_decision_digest'),'ACL11_DECISION_BINDING_MISMATCH')
    req(h.get('parity_assessment_digest')==d['assessment'].get('assessment_digest'),'ACL11_ASSESSMENT_BINDING_MISMATCH')
    req(h.get('security_report_digest')==d['security'].get('security_report_digest'),'ACL11_SECURITY_BINDING_MISMATCH')
    req(not any(h.get(k) for k in ['runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']),'ACL11_AUTHORITY_ESCALATION')
    req(d['provenance'].get('runtime_candidate_invented') is False and d['provenance'].get('runtime_generation_materialized') is False,'ACL11_PROVENANCE_ESCALATION')
    body={'schema_version':'1.0.0','runtime_custody_run_id':h['runtime_custody_run_id'],'promotion_run_id':h['promotion_run_id'],'acl11_handoff_digest':h['handoff_digest'],'runtime_custody_run_digest':d['run']['runtime_custody_run_digest'],'custody_decision_digest':d['decision']['custody_decision_digest'],'parity_assessment_digest':d['assessment']['assessment_digest'],'runtime_generation_manifest_digest':d['generation']['generation_manifest_digest'],'signing_plan_digest':d['signing']['signing_plan_digest'],'tcb_digest':d['tcb']['tcb_digest'],'runtime_candidate_count':0,'event_ledger_digest':d['events']['ledger_digest'],'provenance_graph_digest':d['provenance']['graph_digest']}
    d['binding']=with_digest(body,'binding_digest'); d['root']=root
    return d
