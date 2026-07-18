from __future__ import annotations
from pathlib import Path
from .artifact_manifest import verify_output_manifest
from .canonical import verify_embedded_digest
from .event_ledger import verify_event_ledger
from .io import load_json
def verify_generated_root(root:Path)->dict:
    try:
        if not (root/'.acl09_generated_root').is_file(): return {'passed':False,'reason':'MARKER_MISSING'}
        manifest=load_json(root/'output_manifest.json'); receipt=load_json(root/'memory_receipt.json'); run=load_json(root/'run/memory_run.json'); index=load_json(root/'memory/memory_index.json'); portfolio=load_json(root/'planner/plan_portfolio.json'); events=load_json(root/'events/memory_event_ledger.json'); prov=load_json(root/'lineage/memory_provenance_graph.json'); handoff=load_json(root/'handoff/acl10_handoff.json')
        checks={'manifest':verify_output_manifest(root,manifest),'receipt':verify_embedded_digest(receipt,'receipt_digest'),'run':verify_embedded_digest(run,'memory_run_digest'),'index':verify_embedded_digest(index,'memory_index_digest'),'portfolio':verify_embedded_digest(portfolio,'portfolio_digest'),'events':verify_event_ledger(events),'provenance':verify_embedded_digest(prov,'graph_digest'),'handoff':verify_embedded_digest(handoff,'handoff_digest'),'receipt_manifest':receipt['output_manifest_digest']==manifest['manifest_digest'],'receipt_handoff':receipt['acl10_handoff_digest']==handoff['handoff_digest'],'authority':not any([run['research_execution_allowed'],run['promotion_allowed'],run['live_order_submission_allowed'],run['capital_activation_allowed'],handoff['research_execution_allowed'],handoff['promotion_allowed'],handoff['live_order_submission_allowed'],handoff['capital_activation_allowed']])}
        return {'passed':all(checks.values()),'checks':checks,'artifact_count':manifest['artifact_count'],'memory_run_id':run['memory_run_id']}
    except Exception as exc: return {'passed':False,'reason':str(exc)}
