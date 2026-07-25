from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .events import verify_event_ledger
from .io import load_json
def verify_output(root: Path) -> dict:
    files={'manifest':'output_manifest.json','receipt':'runtime_custody_receipt.json','run':'run/runtime_custody_run.json','assessment':'parity/runtime_parity_assessment.json','decision':'custody/runtime_custody_decision.json','generation':'runtime/runtime_generation_manifest.json','signing':'custody/signing_custody_plan.json','conformance':'parity/conformance_matrix.json','events':'events/runtime_custody_event_ledger.json','provenance':'lineage/runtime_custody_provenance_graph.json','security':'security/security_boundary_report.json','handoff':'handoff/acl12_handoff.json'}
    d={k:load_json(root/v) for k,v in files.items()}
    checks=[('receipt','receipt_digest'),('run','runtime_custody_run_digest'),('assessment','assessment_digest'),('decision','custody_decision_digest'),('generation','generation_manifest_digest'),('signing','signing_plan_digest'),('conformance','conformance_matrix_digest'),('events','ledger_digest'),('provenance','graph_digest'),('security','security_report_digest'),('handoff','handoff_digest')]
    errors=[]
    if not verify_output_manifest(root,d['manifest']): errors.append('OUTPUT_MANIFEST_INVALID')
    for k,f in checks:
        if not verify_embedded_digest(d[k],f): errors.append(f'{k.upper()}_DIGEST_INVALID')
    if not verify_event_ledger(d['events']): errors.append('EVENT_LEDGER_INVALID')
    if d['receipt'].get('output_manifest_digest')!=d['manifest'].get('manifest_digest'): errors.append('RECEIPT_MANIFEST_MISMATCH')
    if d['receipt'].get('acl12_handoff_digest')!=d['handoff'].get('handoff_digest'): errors.append('RECEIPT_HANDOFF_MISMATCH')
    if d['run'].get('runtime_candidate_count')!=0 or d['generation'].get('generation_count')!=0: errors.append('REFERENCE_NO_RUNTIME_PATH_VIOLATED')
    if any([d['handoff'].get('runtime_generation_allowed'),d['handoff'].get('runtime_activation_allowed'),d['handoff'].get('live_order_submission_allowed'),d['handoff'].get('capital_activation_allowed')]): errors.append('AUTHORITY_ESCALATION')
    return {'passed':not errors,'errors':errors,'runtime_custody_run_id':d['run'].get('runtime_custody_run_id')}
