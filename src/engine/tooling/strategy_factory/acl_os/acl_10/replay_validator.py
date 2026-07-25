from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .event_ledger import verify_event_ledger
from .io import load_json

def verify_generated_root(root:Path) -> dict:
    try:
        if not (root/'.acl10_generated_root').is_file(): return {'passed':False,'reason':'MARKER_MISSING'}
        manifest=load_json(root/'output_manifest.json'); receipt=load_json(root/'promotion_receipt.json'); run=load_json(root/'run/promotion_run.json'); decisions=load_json(root/'decisions/promotion_decision_bundle.json'); runtime=load_json(root/'runtime/runtime_candidate_manifest.json'); events=load_json(root/'events/promotion_event_ledger.json'); provenance=load_json(root/'lineage/promotion_provenance_graph.json'); handoff=load_json(root/'handoff/acl11_handoff.json')
        checks={'manifest':verify_output_manifest(root,manifest),'receipt':verify_embedded_digest(receipt,'receipt_digest'),'run':verify_embedded_digest(run,'promotion_run_digest'),'decisions':verify_embedded_digest(decisions,'decision_bundle_digest'),'runtime':verify_embedded_digest(runtime,'runtime_candidate_manifest_digest'),'events':verify_event_ledger(events),'provenance':verify_embedded_digest(provenance,'graph_digest'),'handoff':verify_embedded_digest(handoff,'handoff_digest'),'receipt_manifest':receipt['output_manifest_digest']==manifest['manifest_digest'],'receipt_handoff':receipt['acl11_handoff_digest']==handoff['handoff_digest'],'non_promotional':run['state']=='COMPLETED_NON_PROMOTIONAL' and decisions['promotion_executed_count']==0 and runtime['runtime_candidate_count']==0,'authority':not any([run['promotion_executed'],run['runtime_generation_allowed'],run['live_order_submission_allowed'],run['capital_activation_allowed'],handoff['promotion_execution_allowed'],handoff['runtime_generation_allowed'],handoff['live_order_submission_allowed'],handoff['capital_activation_allowed']])}
        return {'passed':all(checks.values()),'checks':checks,'artifact_count':manifest['artifact_count'],'promotion_run_id':run['promotion_run_id']}
    except Exception as exc: return {'passed':False,'reason':str(exc)}
