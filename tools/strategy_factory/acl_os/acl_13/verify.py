from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .events import verify_event_ledger
from .io import load_json
def verify_output(root:Path)->dict:
    files={'manifest':'output_manifest.json','receipt':'one_hour_assessment_receipt.json','run':'run/one_hour_assessment_run.json','request':'input/assessment_request.json','slice':'slice/fast_data_slice.json','support':'diagnostics/support_diagnostics.json','baseline':'baselines/constrained_random_baseline.json','catalog':'discovery/setup_family_catalog.json','value':'value/context_value_decomposition.json','uncertainty':'uncertainty/uncertainty_and_limitations.json','evidence':'evidence/one_hour_evidence_bundle.json','decision':'decision/one_hour_assessment_result.json','report':'report/one_hour_assessment_report.json','executive':'report/executive_summary.json','security':'security/security_boundary_report.json','events':'events/one_hour_assessment_event_ledger.json','provenance':'lineage/one_hour_assessment_provenance_graph.json','handoff':'handoff/acl14_handoff.json','integrity':'reports/integrity_report.json'}
    d={k:load_json(root/v) for k,v in files.items()}; errors=[]
    checks=[('receipt','receipt_digest'),('run','assessment_run_digest'),('request','assessment_request_digest'),('slice','slice_digest'),('support','support_diagnostics_digest'),('baseline','baseline_report_digest'),('catalog','catalog_digest'),('value','value_decomposition_digest'),('uncertainty','uncertainty_report_digest'),('evidence','evidence_bundle_digest'),('decision','assessment_result_digest'),('report','report_digest'),('executive','executive_summary_digest'),('security','security_report_digest'),('events','ledger_digest'),('provenance','graph_digest'),('handoff','handoff_digest'),('integrity','integrity_report_digest')]
    if not verify_output_manifest(root,d['manifest']): errors.append('OUTPUT_MANIFEST_INVALID')
    for k,f in checks:
        if not verify_embedded_digest(d[k],f): errors.append(f'{k.upper()}_DIGEST_INVALID')
    if not verify_event_ledger(d['events']): errors.append('EVENT_LEDGER_INVALID')
    if d['receipt'].get('output_manifest_digest')!=d['manifest'].get('manifest_digest'): errors.append('RECEIPT_MANIFEST_MISMATCH')
    if d['receipt'].get('acl14_handoff_digest')!=d['handoff'].get('handoff_digest'): errors.append('RECEIPT_HANDOFF_MISMATCH')
    if not d['request'].get('synthetic_reference_data'): errors.append('REFERENCE_FIXTURE_DISCLOSURE_MISSING')
    if d['decision'].get('validation_claim_allowed') is not False or d['decision'].get('alpha_claim_allowed') is not False: errors.append('TRIAGE_CLAIM_ESCALATION')
    if any(d['handoff'].get(k) for k in ['first_real_context_pilot_execution_allowed','validation_claim_allowed','alpha_claim_allowed','production_security_ready','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']): errors.append('HANDOFF_AUTHORITY_ESCALATION')
    if d['run'].get('state')!='COMPLETED_BOUNDED_RESEARCH_TRIAGE': errors.append('RUN_STATE_INVALID')
    return {'passed':not errors,'errors':errors,'assessment_run_id':d['run'].get('assessment_run_id'),'report_id':d['report'].get('report_id')}
