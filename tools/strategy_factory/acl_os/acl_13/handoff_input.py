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
def load_acl12_bundle(root:Path)->dict[str,Any]:
    req((root/'.acl12_generated_root').is_file(),'ACL12_MARKER_MISSING')
    paths={'manifest':'output_manifest.json','receipt':'security_hardening_receipt.json','handoff':'handoff/acl13_handoff.json','run':'run/security_hardening_run.json','decision':'decision/security_readiness_decision.json','matrix':'assessment/security_control_matrix.json','evidence':'evidence/security_evidence_bundle.json','risk':'risk/security_risk_register.json','events':'events/security_hardening_event_ledger.json','provenance':'lineage/security_hardening_provenance_graph.json','security':'security/security_boundary_report.json','integrity':'reports/integrity_report.json'}
    d={k:load_json(root/v) for k,v in paths.items()}
    req(verify_output_manifest(root,d['manifest']),'ACL12_MANIFEST_INVALID')
    checks=[('receipt','receipt_digest'),('handoff','handoff_digest'),('run','security_hardening_run_digest'),('decision','readiness_decision_digest'),('matrix','assessment_digest'),('evidence','evidence_bundle_digest'),('risk','register_digest'),('events','ledger_digest'),('provenance','graph_digest'),('security','security_report_digest'),('integrity','integrity_report_digest')]
    for k,f in checks: req(verify_embedded_digest(d[k],f),f'ACL12_{k.upper()}_DIGEST_INVALID')
    h=d['handoff']
    req(h.get('handoff_type')==HANDOFF_IN,'ACL12_HANDOFF_TYPE_INVALID')
    req(REQUIRED_UPSTREAM_ACTIONS.issubset(set(h.get('required_acl13_actions',[]))),'ACL12_REQUIRED_ACTIONS_MISSING')
    req(FORBIDDEN_UPSTREAM_ACTIONS.issubset(set(h.get('forbidden_acl13_actions',[]))),'ACL12_FORBIDDEN_ACTIONS_MISSING')
    req(d['receipt'].get('output_manifest_digest')==d['manifest'].get('manifest_digest'),'ACL12_RECEIPT_MANIFEST_MISMATCH')
    req(d['receipt'].get('acl13_handoff_digest')==h.get('handoff_digest'),'ACL12_RECEIPT_HANDOFF_MISMATCH')
    req(h.get('security_readiness_decision_digest')==d['decision'].get('readiness_decision_digest'),'ACL12_DECISION_BINDING_MISMATCH')
    req(h.get('security_control_matrix_digest')==d['matrix'].get('assessment_digest'),'ACL12_MATRIX_BINDING_MISMATCH')
    req(h.get('security_evidence_bundle_digest')==d['evidence'].get('evidence_bundle_digest'),'ACL12_EVIDENCE_BINDING_MISMATCH')
    req(h.get('security_risk_register_digest')==d['risk'].get('register_digest'),'ACL12_RISK_BINDING_MISMATCH')
    req(d['decision'].get('decision')=='REFERENCE_SECURITY_HARDENED_PRODUCTION_NOT_READY','ACL12_READINESS_REINTERPRETATION_DENIED')
    req(d['decision'].get('production_security_ready') is False,'ACL12_PRODUCTION_READINESS_ESCALATION')
    req(d['run'].get('runtime_candidate_count')==0,'ACL12_RUNTIME_CANDIDATE_INVENTION')
    req(not any(h.get(k) for k in ['production_security_ready','runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed','production_key_access_allowed']),'ACL12_AUTHORITY_ESCALATION')
    req(d['security'].get('passed') is True and d['integrity'].get('passed') is True,'ACL12_SECURITY_OR_INTEGRITY_FAILED')
    body={'schema_version':'1.0.0','security_hardening_run_id':h['security_hardening_run_id'],'runtime_custody_run_id':h['runtime_custody_run_id'],'acl12_handoff_digest':h['handoff_digest'],'security_readiness_decision_digest':d['decision']['readiness_decision_digest'],'security_control_matrix_digest':d['matrix']['assessment_digest'],'security_evidence_bundle_digest':d['evidence']['evidence_bundle_digest'],'security_risk_register_digest':d['risk']['register_digest'],'production_security_ready':False,'runtime_candidate_count':0,'open_production_risk_count':d['risk'].get('open_production_risk_count',0),'event_ledger_digest':d['events']['ledger_digest'],'provenance_graph_digest':d['provenance']['graph_digest']}
    d['binding']=with_digest(body,'binding_digest'); d['root']=root
    return d
