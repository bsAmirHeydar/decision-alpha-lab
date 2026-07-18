from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .events import verify_event_ledger
from .io import load_json
def verify_output(root:Path)->dict:
    files={'manifest':'output_manifest.json','receipt':'fleet_closure_receipt.json','run':'run/fleet_closure_run.json','binding':'binding/acl14_binding.json','authority':'authority/authority_report.json','fleet':'contract/fleet_registration_contract.json','ownership':'contract/lifecycle_ownership_contract.json','retention':'contract/retention_contract.json','surveillance':'contract/surveillance_contract.json','migration':'contract/migration_contract.json','reopen':'contract/reopen_policy.json','closure_policy':'contract/closure_policy.json','package_status':'status/fleet_package_status.json','retention_status':'status/retention_status.json','surveillance_status':'status/surveillance_status.json','evidence':'evidence/pilot_evidence_inventory.json','operations':'operations/fleet_operations_manifest.json','execution':'execution/runtime_and_order_manifest.json','decision':'decision/non_capital_closure_decision.json','report':'report/fleet_closure_report.json','executive':'report/executive_brief.json','residual':'report/residual_risk_report.json','security':'security/security_boundary_report.json','events':'events/fleet_event_ledger.json','provenance':'lineage/fleet_provenance_graph.json','handoff':'handoff/lifecycle_closure_handoff.json','integrity':'reports/integrity_report.json'}
    try: d={k:load_json(root/v) for k,v in files.items()}
    except Exception as e: return {'passed':False,'errors':[str(e)]}
    fields={'receipt':'receipt_digest','run':'fleet_closure_run_digest','binding':'acl14_binding_digest','authority':'authority_report_digest','fleet':'fleet_registration_digest','ownership':'ownership_contract_digest','retention':'retention_contract_digest','surveillance':'surveillance_contract_digest','migration':'migration_contract_digest','reopen':'reopen_policy_digest','closure_policy':'closure_policy_digest','package_status':'package_status_digest','retention_status':'retention_status_digest','surveillance_status':'surveillance_status_digest','evidence':'evidence_inventory_digest','operations':'fleet_operations_manifest_digest','execution':'execution_manifest_digest','decision':'closure_decision_digest','report':'fleet_closure_report_digest','executive':'executive_brief_digest','residual':'residual_risk_report_digest','security':'security_report_digest','events':'ledger_digest','provenance':'graph_digest','handoff':'handoff_digest','integrity':'integrity_report_digest'}
    errors=[]
    if not verify_output_manifest(root,d['manifest']): errors.append('OUTPUT_MANIFEST_INVALID')
    for k,f in fields.items():
        if not verify_embedded_digest(d[k],f): errors.append(f'{k.upper()}_DIGEST_INVALID')
    if not verify_event_ledger(d['events']): errors.append('EVENT_LEDGER_INVALID')
    if d['receipt'].get('output_manifest_digest')!=d['manifest'].get('manifest_digest'): errors.append('RECEIPT_MANIFEST_MISMATCH')
    if d['receipt'].get('lifecycle_closure_handoff_digest')!=d['handoff'].get('handoff_digest'): errors.append('RECEIPT_HANDOFF_MISMATCH')
    if d['decision'].get('state')!='REFERENCE_LIFECYCLE_CLOSED_NON_CAPITAL': errors.append('CLOSURE_STATE_INVALID')
    if d['execution'].get('pilot_execution_count')!=0 or d['execution'].get('runtime_generation_count')!=0 or d['execution'].get('live_order_count')!=0 or d['execution'].get('capital_activation_count')!=0: errors.append('EXECUTION_AUTHORITY_ESCALATION')
    if d['evidence'].get('prospective_evidence_present') is not False or d['evidence'].get('pilot_outcomes_present') is not False: errors.append('EVIDENCE_INVENTION')
    if any(d['handoff'].get(k) for k in ['pilot_execution_materialized','prospective_evidence_present','validation_claim_allowed','promotion_allowed','runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']): errors.append('HANDOFF_AUTHORITY_ESCALATION')
    if d['run'].get('state')!='COMPLETED_REFERENCE_FLEET_CLOSURE_NON_CAPITAL': errors.append('RUN_STATE_INVALID')
    return {'passed':not errors,'errors':errors,'fleet_closure_run_id':d['run'].get('fleet_closure_run_id'),'fleet_id':d['fleet'].get('fleet_id'),'state':d['decision'].get('state')}
