from __future__ import annotations
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_object,verify_embedded_digest
from .errors import ContractError,IntegrityError
from .event_ledger import verify_event_ledger
from .io import load_json
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS

def load_acl08_bundle(root:Path)->dict[str,Any]:
    root=root.resolve()
    if not (root/'.acl08_generated_root').is_file(): raise ContractError('ACL08_GENERATED_ROOT_MARKER_MISSING')
    manifest=load_json(root/'output_manifest.json')
    if not verify_output_manifest(root,manifest): raise IntegrityError('ACL08_OUTPUT_MANIFEST_INVALID')
    receipt=load_json(root/'report_receipt.json'); handoff=load_json(root/'handoff/acl09_handoff.json')
    run=load_json(root/'run/report_run.json'); batch=load_json(root/'reports/batch_report.json')
    experience=load_json(root/'experience/experience_bundle.json'); events=load_json(root/'events/report_event_ledger.json')
    provenance=load_json(root/'lineage/report_provenance_graph.json')
    if handoff.get('handoff_type')!=HANDOFF_IN or not verify_embedded_digest(handoff,'handoff_digest'): raise IntegrityError('ACL08_HANDOFF_INVALID')
    if set(handoff.get('required_acl09_actions',[]))!=REQUIRED_UPSTREAM_ACTIONS: raise IntegrityError('ACL08_REQUIRED_ACTION_SET_INVALID')
    if set(handoff.get('forbidden_acl09_actions',[]))!=FORBIDDEN_UPSTREAM_ACTIONS: raise IntegrityError('ACL08_FORBIDDEN_ACTION_SET_INVALID')
    if not verify_embedded_digest(receipt,'receipt_digest') or not verify_embedded_digest(run,'report_run_digest') or not verify_embedded_digest(batch,'batch_report_digest') or not verify_embedded_digest(experience,'experience_bundle_digest') or not verify_event_ledger(events) or not verify_embedded_digest(provenance,'graph_digest'): raise IntegrityError('ACL08_EMBEDDED_DIGEST_INVALID')
    if receipt['output_manifest_digest']!=manifest['manifest_digest'] or receipt['acl09_handoff_digest']!=handoff['handoff_digest']: raise IntegrityError('ACL08_RECEIPT_BINDING_INVALID')
    if handoff['report_run_digest']!=run['report_run_digest'] or handoff['batch_report_digest']!=batch['batch_report_digest'] or handoff['experience_bundle_digest']!=experience['experience_bundle_digest'] or handoff['event_ledger_digest']!=events['ledger_digest'] or handoff['provenance_graph_digest']!=provenance['graph_digest']: raise IntegrityError('ACL08_HANDOFF_BINDING_INVALID')
    if run.get('state')!='COMPLETED_NON_PROMOTIONAL' or run.get('validation_decisions_mutated') is not False: raise IntegrityError('ACL08_RUN_STATE_INVALID')
    if experience.get('memory_ingestion_status')!='NOT_INGESTED' or experience.get('active_planning_status')!='NOT_RUN': raise IntegrityError('ACL08_EXPERIENCE_ALREADY_CONSUMED')
    if not provenance.get('reaches_acl07_validation') or provenance.get('validation_decisions_mutated') is not False: raise IntegrityError('ACL08_PROVENANCE_INVALID')
    for doc in (handoff,receipt,run,experience):
        if doc.get('live_order_submission_allowed') is not False or doc.get('capital_activation_allowed') is not False or doc.get('promotion_allowed',False) is not False: raise IntegrityError('ACL08_AUTHORITY_ESCALATION')
    records=[]
    for ref in experience.get('records',[]):
        p=root/'experience/records'/f"{ref['experience_id']}.json"
        record=load_json(p)
        if not verify_embedded_digest(record,'experience_digest') or record['experience_digest']!=ref['experience_digest'] or record['setup_id']!=ref['setup_id']: raise IntegrityError('ACL08_EXPERIENCE_RECORD_INVALID')
        if record.get('source_decision_digest') is None or record.get('source_candidate_report_digest') is None: raise IntegrityError('ACL08_SOURCE_DIGEST_MISSING')
        if record.get('promotion_allowed') is not False or record.get('live_order_submission_allowed') is not False or record.get('capital_activation_allowed') is not False or record.get('doctrine_amendment_allowed') is not False: raise IntegrityError('ACL08_RECORD_AUTHORITY_ESCALATION')
        records.append(record)
    if len(records)!=experience['record_count']: raise IntegrityError('ACL08_RECORD_COUNT_MISMATCH')
    bundle_digest=digest_object({'manifest':manifest['manifest_digest'],'receipt':receipt['receipt_digest'],'handoff':handoff['handoff_digest'],'run':run['report_run_digest'],'batch':batch['batch_report_digest'],'experience':experience['experience_bundle_digest'],'events':events['ledger_digest'],'provenance':provenance['graph_digest'],'records':[r['experience_digest'] for r in sorted(records,key=lambda x:x['experience_id'])]})
    return {'root':root,'manifest':manifest,'receipt':receipt,'handoff':handoff,'run':run,'batch':batch,'experience':experience,'events':events,'provenance':provenance,'records':records,'bundle_digest':bundle_digest}
