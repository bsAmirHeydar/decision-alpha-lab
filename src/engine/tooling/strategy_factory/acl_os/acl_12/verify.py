from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .events import verify_event_ledger
from .io import load_json
def verify_output(root:Path)->dict:
    files={'manifest':'output_manifest.json','receipt':'security_hardening_receipt.json','run':'run/security_hardening_run.json','matrix':'assessment/security_control_matrix.json','threats':'assessment/threat_assessment.json','risk':'risk/security_risk_register.json','evidence':'evidence/security_evidence_bundle.json','decision':'decision/security_readiness_decision.json','security':'security/security_boundary_report.json','events':'events/security_hardening_event_ledger.json','provenance':'lineage/security_hardening_provenance_graph.json','handoff':'handoff/acl13_handoff.json','secret':'scans/secret_scan_report.json','mql':'scans/mql5_forbidden_api_scan_report.json'}
    d={k:load_json(root/v) for k,v in files.items()}; errors=[]
    checks=[('receipt','receipt_digest'),('run','security_hardening_run_digest'),('matrix','assessment_digest'),('threats','assessment_digest'),('risk','register_digest'),('evidence','evidence_bundle_digest'),('decision','readiness_decision_digest'),('security','security_report_digest'),('events','ledger_digest'),('provenance','graph_digest'),('handoff','handoff_digest'),('secret','scan_digest'),('mql','scan_digest')]
    if not verify_output_manifest(root,d['manifest']): errors.append('OUTPUT_MANIFEST_INVALID')
    for k,f in checks:
        if not verify_embedded_digest(d[k],f): errors.append(f'{k.upper()}_DIGEST_INVALID')
    if not verify_event_ledger(d['events']): errors.append('EVENT_LEDGER_INVALID')
    if d['receipt'].get('output_manifest_digest')!=d['manifest'].get('manifest_digest'): errors.append('RECEIPT_MANIFEST_MISMATCH')
    if d['receipt'].get('acl13_handoff_digest')!=d['handoff'].get('handoff_digest'): errors.append('RECEIPT_HANDOFF_MISMATCH')
    if d['decision'].get('production_security_ready') is not False: errors.append('PRODUCTION_READINESS_ESCALATION')
    if d['run'].get('runtime_candidate_count')!=0: errors.append('RUNTIME_CANDIDATE_INVENTED')
    if not d['secret'].get('passed') or not d['mql'].get('passed'): errors.append('REFERENCE_SCAN_FAILED')
    if any(d['handoff'].get(k) for k in ['production_security_ready','runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed','production_key_access_allowed']): errors.append('HANDOFF_AUTHORITY_ESCALATION')
    return {'passed':not errors,'errors':errors,'security_hardening_run_id':d['run'].get('security_hardening_run_id')}
