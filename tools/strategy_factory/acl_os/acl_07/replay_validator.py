from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .event_ledger import verify_event_ledger
from .io import load_json

def verify_generated_root(root:Path)->dict:
    checks={}
    checks['marker']=(root/'.acl07_generated_root').is_file() and not (root/'.acl07_generated_root').is_symlink()
    manifest=load_json(root/'output_manifest.json'); checks['manifest']=verify_output_manifest(root,manifest)
    receipt=load_json(root/'validation_receipt.json'); checks['receipt_digest']=verify_embedded_digest(receipt,'receipt_digest'); checks['receipt_manifest_binding']=receipt['output_manifest_digest']==manifest['manifest_digest']
    validation=load_json(root/'validation/validation_run.json'); checks['validation_digest']=verify_embedded_digest(validation,'validation_run_digest')
    decisions=load_json(root/'decisions/validation_decision_bundle.json'); checks['decision_digest']=verify_embedded_digest(decisions,'decision_bundle_digest'); checks['no_promotion']=decisions['promotion_allowed'] is False and decisions['alpha_claim_allowed'] is False
    events=load_json(root/'events/validation_event_ledger.json'); checks['event_chain']=verify_event_ledger(events)
    handoff=load_json(root/'handoff/acl08_handoff.json'); checks['handoff_digest']=verify_embedded_digest(handoff,'handoff_digest'); checks['authority_denied']=handoff['live_order_submission_allowed'] is False and handoff['capital_activation_allowed'] is False
    return {'passed':all(checks.values()),'checks':checks}
