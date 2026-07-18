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
def load_acl13_bundle(root:Path)->dict[str,Any]:
    req((root/'.acl13_generated_root').is_file(),'ACL13_MARKER_MISSING')
    paths={'manifest':'output_manifest.json','receipt':'one_hour_assessment_receipt.json','handoff':'handoff/acl14_handoff.json','run':'run/one_hour_assessment_run.json','decision':'decision/one_hour_assessment_result.json','report':'report/one_hour_assessment_report.json','evidence':'evidence/one_hour_evidence_bundle.json','events':'events/one_hour_assessment_event_ledger.json','provenance':'lineage/one_hour_assessment_provenance_graph.json'}
    d={k:load_json(root/v) for k,v in paths.items()}
    req(verify_output_manifest(root,d['manifest']),'ACL13_MANIFEST_INVALID')
    for k,f in [('receipt','receipt_digest'),('handoff','handoff_digest'),('run','assessment_run_digest'),('decision','assessment_result_digest'),('report','report_digest'),('evidence','evidence_bundle_digest'),('events','ledger_digest'),('provenance','graph_digest')]: req(verify_embedded_digest(d[k],f),f'ACL13_{k.upper()}_DIGEST_INVALID')
    req(d['handoff'].get('handoff_type')==HANDOFF_IN,'ACL13_HANDOFF_TYPE_INVALID')
    req(set(d['handoff'].get('required_acl14_actions',[]))==REQUIRED_UPSTREAM_ACTIONS,'ACL13_REQUIRED_ACTIONS_INVALID')
    req(set(d['handoff'].get('forbidden_acl14_actions',[]))==FORBIDDEN_UPSTREAM_ACTIONS,'ACL13_FORBIDDEN_ACTIONS_INVALID')
    req(d['receipt'].get('output_manifest_digest')==d['manifest'].get('manifest_digest'),'ACL13_RECEIPT_MANIFEST_MISMATCH')
    req(d['receipt'].get('acl14_handoff_digest')==d['handoff'].get('handoff_digest'),'ACL13_RECEIPT_HANDOFF_MISMATCH')
    req(d['handoff'].get('assessment_result_digest')==d['decision'].get('assessment_result_digest'),'ACL13_HANDOFF_DECISION_MISMATCH')
    req(d['handoff'].get('report_digest')==d['report'].get('report_digest'),'ACL13_HANDOFF_REPORT_MISMATCH')
    req(d['handoff'].get('evidence_bundle_digest')==d['evidence'].get('evidence_bundle_digest'),'ACL13_HANDOFF_EVIDENCE_MISMATCH')
    req(d['handoff'].get('event_ledger_digest')==d['events'].get('ledger_digest'),'ACL13_HANDOFF_EVENT_MISMATCH')
    req(d['handoff'].get('provenance_graph_digest')==d['provenance'].get('graph_digest'),'ACL13_HANDOFF_PROVENANCE_MISMATCH')
    req(d['handoff'].get('first_real_context_pilot_design_allowed') is True,'ACL13_PILOT_DESIGN_NOT_ALLOWED')
    req(d['handoff'].get('first_real_context_pilot_execution_allowed') is False,'ACL13_PILOT_EXECUTION_ESCALATION')
    for field in ['validation_claim_allowed','alpha_claim_allowed','production_security_ready','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']:
        req(d['handoff'].get(field) is False,f'ACL13_{field.upper()}_ESCALATION')
    body={'schema_version':'1.0.0','assessment_run_id':d['run']['assessment_run_id'],'report_id':d['report']['report_id'],'context_id':d['decision']['context_id'],'context_version':d['decision']['context_version'],'assessment_result':d['decision']['decision'],'assessment_result_digest':d['decision']['assessment_result_digest'],'report_digest':d['report']['report_digest'],'evidence_bundle_digest':d['evidence']['evidence_bundle_digest'],'acl13_handoff_digest':d['handoff']['handoff_digest'],'acl13_manifest_digest':d['manifest']['manifest_digest'],'pilot_design_allowed':True,'pilot_execution_allowed':False,'synthetic_reference_data':True,'validation_claim_allowed':False,'alpha_claim_allowed':False,'production_security_ready':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
    return {'binding':with_digest(body,'binding_digest'),**d}
