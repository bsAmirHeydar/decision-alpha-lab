from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .events import verify_event_ledger
from .io import load_json
def verify_output(root:Path)->dict:
    files={'manifest':'output_manifest.json','receipt':'first_real_context_pilot_receipt.json','run':'run/pilot_run.json','request':'input/pilot_request.json','input_validation':'input/pilot_input_validation_report.json','contract':'contract/first_real_context_pilot_contract.json','owner':'contract/context_owner_approval_bundle.json','mapping':'contract/data_mapping_contract.json','availability':'contract/availability_semantics_contract.json','evaluation':'contract/evaluation_freeze_contract.json','search':'contract/search_space_freeze.json','support':'contract/support_target_contract.json','stop':'contract/stop_condition_contract.json','failure':'contract/failure_condition_contract.json','boundary':'contract/non_capital_boundary_contract.json','readiness':'assessment/pilot_readiness_matrix.json','decision':'decision/pilot_readiness_decision.json','execution':'execution/pilot_execution_manifest.json','report':'report/pilot_design_report.json','executive':'report/executive_brief.json','security':'security/security_boundary_report.json','events':'events/pilot_event_ledger.json','provenance':'lineage/pilot_provenance_graph.json','handoff':'handoff/acl15_handoff.json','integrity':'reports/integrity_report.json'}
    d={k:load_json(root/v) for k,v in files.items()}; errors=[]
    checks=[('receipt','receipt_digest'),('run','pilot_run_digest'),('request','pilot_request_digest'),('input_validation','input_validation_digest'),('contract','pilot_contract_digest'),('owner','owner_approval_bundle_digest'),('mapping','data_mapping_contract_digest'),('availability','availability_contract_digest'),('evaluation','evaluation_freeze_digest'),('search','search_space_freeze_digest'),('support','support_contract_digest'),('stop','stop_contract_digest'),('failure','failure_contract_digest'),('boundary','non_capital_boundary_digest'),('readiness','readiness_matrix_digest'),('decision','pilot_readiness_decision_digest'),('execution','pilot_execution_manifest_digest'),('report','pilot_design_report_digest'),('executive','executive_brief_digest'),('security','security_report_digest'),('events','ledger_digest'),('provenance','graph_digest'),('handoff','handoff_digest'),('integrity','integrity_report_digest')]
    if not verify_output_manifest(root,d['manifest']): errors.append('OUTPUT_MANIFEST_INVALID')
    for k,f in checks:
        if not verify_embedded_digest(d[k],f): errors.append(f'{k.upper()}_DIGEST_INVALID')
    if not verify_event_ledger(d['events']): errors.append('EVENT_LEDGER_INVALID')
    if d['receipt'].get('output_manifest_digest')!=d['manifest'].get('manifest_digest'): errors.append('RECEIPT_MANIFEST_MISMATCH')
    if d['receipt'].get('acl15_handoff_digest')!=d['handoff'].get('handoff_digest'): errors.append('RECEIPT_HANDOFF_MISMATCH')
    if d['request'].get('synthetic_or_reference_reuse_as_real') is not False: errors.append('SYNTHETIC_REUSE_ESCALATION')
    if d['execution'].get('pilot_execution_materialized') is not False or d['execution'].get('execution_count')!=0: errors.append('PILOT_EXECUTION_MATERIALIZED')
    if any(d['handoff'].get(k) for k in ['pilot_execution_materialized','prospective_evidence_present','validation_claim_allowed','alpha_claim_allowed','production_security_ready','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']): errors.append('HANDOFF_AUTHORITY_ESCALATION')
    if d['run'].get('state')!='COMPLETED_PILOT_CONTRACT_AND_READINESS_ASSESSMENT': errors.append('RUN_STATE_INVALID')
    if d['decision'].get('state') not in {'PILOT_CONTRACT_AUTHORED_REAL_EVIDENCE_REQUIRED','PILOT_READY_NON_CAPITAL_NOT_EXECUTED'}: errors.append('DECISION_STATE_INVALID')
    return {'passed':not errors,'errors':errors,'pilot_run_id':d['run'].get('pilot_run_id'),'pilot_contract_id':d['contract'].get('pilot_contract_id'),'state':d['decision'].get('state')}
