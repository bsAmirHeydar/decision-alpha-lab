from .authority import verify_permit
from .canonical import digest_object,sha256_bytes
from .errors import IntegrityError
from .io import read_json,read_jsonl

def _d(o,f,l):
    if digest_object(o,f)!=o.get(f):raise IntegrityError(f"{l} digest invalid")
def verify_package(root):
    if root.is_symlink() or not root.is_dir():raise IntegrityError("shared-engine root missing or symlinked")
    marker=read_json(root/"shared_engine_marker.json");handoff=read_json(root/"handoff/lcm07_to_lcm08_handoff.json");receipt=read_json(root/"shared_engine_receipt.json");manifest=read_json(root/"output_manifest.json");permit=read_json(root/"authority/authority_permit.json")
    seen=set()
    for rec in manifest["artifacts"]:
        rel=rec["path"]
        if rel in seen:raise IntegrityError("duplicate manifest path")
        seen.add(rel);p=root/rel
        if p.is_symlink() or not p.is_file() or p.stat().st_size!=rec["size_bytes"] or sha256_bytes(p.read_bytes())!=rec["sha256"]:raise IntegrityError(f"manifest mismatch: {rel}")
    if manifest["artifact_count"]!=len(seen):raise IntegrityError("manifest count invalid")
    for o,f,l in ((marker,"marker_digest","marker"),(handoff,"handoff_digest","handoff"),(receipt,"receipt_digest","receipt"),(manifest,"output_manifest_digest","manifest")):_d(o,f,l)
    if marker.get("phase_id")!="LCM-07" or marker.get("shared_engine_run_id")!=root.name or marker.get("claim_ceiling")!="SHARED_ENGINE_EXTRACTION_REFERENCE_ONLY":raise IntegrityError("marker binding invalid")
    if handoff.get("handoff_type")!="LCM07_TO_LCM08" or handoff.get("shared_engine_extraction_authorized") is not False:raise IntegrityError("handoff authority invalid")
    verify_permit(permit,marker["source_handoff_digest"],marker["framework_run_id"])
    bind=read_json(root/"input/lcm06_binding.json");_d(bind,"binding_digest","binding")
    for p in sorted((root/"registries").glob("*.json")):
        o=read_json(p);_d(o,"registry_digest",p.name)
        if o.get("closed") is not True:raise IntegrityError("open registry")
    for p in sorted((root/"contracts").glob("*.json")):
        o=read_json(p);_d(o,"contract_digest",p.name)
        if o.get("source_mutation_allowed") is not False or o.get("target_materialization_allowed") is not False or o.get("authority_expansion_allowed") is not False:raise IntegrityError("contract authority escalation")
    datasets=(("candidates/selected_candidate_clusters.jsonl","candidate_digest"),("variance/variance_catalog.jsonl","variance_digest"),("equivalence/equivalence_results.jsonl","equivalence_digest"),("designs/parameterized_engine_designs.jsonl","design_digest"),("adapters/consumer_adapter_contracts.jsonl","adapter_digest"),("governance/shared_engine_governance_records.jsonl","governance_digest"),("decisions/extraction_decisions.jsonl","decision_digest"),("fixtures/metamorphic_fixture_catalog.jsonl","fixture_digest"))
    for rel,field in datasets:
        for i,o in enumerate(read_jsonl(root/rel),1):_d(o,field,f"{rel}:{i}")
    equiv=read_jsonl(root/"equivalence/equivalence_results.jsonl");designs=read_jsonl(root/"designs/parameterized_engine_designs.jsonl");adapters=read_jsonl(root/"adapters/consumer_adapter_contracts.jsonl");decisions=read_jsonl(root/"decisions/extraction_decisions.jsonl")
    if any(x.get("extraction_authorized") is not False for x in equiv) or any(x.get("materialized") is not False or x.get("extraction_authorized") is not False for x in designs) or any(x.get("write_performed") is not False for x in adapters) or any(x.get("materialization_authorized") is not False or x.get("merge_authorized") is not False for x in decisions):raise IntegrityError("extraction or mutation authority detected")
    for rel,field in (("reports/shared_engine_summary.json","summary_digest"),("reports/hostile_review.json","hostile_review_digest"),("reports/acceptance_report.json","acceptance_digest"),("events/shared_engine_event_ledger.json","ledger_digest"),("provenance/shared_engine_provenance_graph.json","provenance_digest")):_d(read_json(root/rel),field,rel)
    ledger=read_json(root/"events/shared_engine_event_ledger.json");prev=None
    for i,e in enumerate(ledger["events"],1):
        if e["sequence"]!=i or e["previous_event_digest"]!=prev:raise IntegrityError("event chain invalid")
        _d(e,"event_digest",f"event {i}")
        for f in ("source_move_authority","source_delete_authority","target_materialization_authority","semantic_refactor_authority","merge_authority","runtime_authority","live_order_authority","capital_authority"):
            if e.get(f) is not False:raise IntegrityError("event authority escalation")
        prev=e["event_digest"]
    if prev!=ledger["final_event_digest"]:raise IntegrityError("event final digest invalid")
    summary=read_json(root/"reports/shared_engine_summary.json")
    return {"passed":True,"shared_engine_run_id":root.name,"candidate_cluster_count":summary["candidate_cluster_count"],"selected_candidate_count":summary["selected_candidate_count"],"materialized_engine_count":summary["materialized_engine_count"],"manifest_artifact_count":manifest["artifact_count"]}
