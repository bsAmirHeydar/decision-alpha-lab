from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .event_ledger import verify_event_ledger
from .io import load_json
def verify_generated_root(root:Path)->dict:
    checks={}; checks['marker']=(root/'.acl08_generated_root').is_file() and not (root/'.acl08_generated_root').is_symlink()
    manifest=load_json(root/'output_manifest.json'); checks['manifest']=verify_output_manifest(root,manifest)
    receipt=load_json(root/'report_receipt.json'); checks['receipt_digest']=verify_embedded_digest(receipt,'receipt_digest'); checks['receipt_manifest_binding']=receipt['output_manifest_digest']==manifest['manifest_digest']
    run=load_json(root/'run/report_run.json'); checks['run_digest']=verify_embedded_digest(run,'report_run_digest'); checks['run_safe']=run['state']=='COMPLETED_NON_PROMOTIONAL' and run['validation_decisions_mutated'] is False
    batch=load_json(root/'reports/batch_report.json'); checks['batch_digest']=verify_embedded_digest(batch,'batch_report_digest'); checks['no_authority']=all(batch[x] is False for x in ['alpha_claim_allowed','promotion_allowed','live_order_submission_allowed','capital_activation_allowed'])
    experience=load_json(root/'experience/experience_bundle.json'); checks['experience_digest']=verify_embedded_digest(experience,'experience_bundle_digest'); checks['not_ingested']=experience['memory_ingestion_status']=='NOT_INGESTED' and experience['active_planning_status']=='NOT_RUN'
    events=load_json(root/'events/report_event_ledger.json'); checks['event_chain']=verify_event_ledger(events)
    handoff=load_json(root/'handoff/acl09_handoff.json'); checks['handoff_digest']=verify_embedded_digest(handoff,'handoff_digest'); checks['handoff_safe']=handoff['promotion_allowed'] is False and handoff['live_order_submission_allowed'] is False and handoff['capital_activation_allowed'] is False
    external=(root/'views/external_restricted.json').read_text(encoding='utf-8'); checks['external_redaction']=not any(x in external for x in ['SETUP_','CAND_','VALDEC_','candidate_id','setup_id'])
    return {'passed':all(checks.values()),'checks':checks}
