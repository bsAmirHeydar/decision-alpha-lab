from __future__ import annotations
from pathlib import Path
from .canonical import verify_embedded_digest
from .io import load_json, load_jsonl

REQUIRED=("documentation_authority_registry.json","documentation_duplicate_registry.json","documentation_canonical_map.json","documentation_contradiction_registry.json","documentation_inbound_reference_graph.json","documentation_unknown_queue.json","LCM12A_TO_LCM12B_HANDOFF.json","output_manifest.json","rollback_manifest.json","reports/acceptance_report.json","reports/hostile_review_report.json","records/documentation_records.jsonl","references/documentation_reference_edges.jsonl","unknowns/documentation_unknowns.jsonl")
DIGEST_FIELDS={"documentation_authority_registry.json":"registry_digest","documentation_duplicate_registry.json":"registry_digest","documentation_canonical_map.json":"map_digest","documentation_contradiction_registry.json":"registry_digest","documentation_inbound_reference_graph.json":"graph_digest","documentation_unknown_queue.json":"queue_digest","LCM12A_TO_LCM12B_HANDOFF.json":"handoff_digest","output_manifest.json":"output_manifest_digest","rollback_manifest.json":"rollback_digest","reports/acceptance_report.json":"report_digest","reports/hostile_review_report.json":"report_digest"}

def verify_package(root:Path):
    errors=[]
    for rel in REQUIRED:
        if not (root/rel).is_file():errors.append(f"MISSING:{rel}")
    if errors:return errors
    for rel,field in DIGEST_FIELDS.items():
        value=load_json(root/rel)
        if not verify_embedded_digest(value,field):errors.append(f"DIGEST:{rel}:{field}")
    authority=load_json(root/"documentation_authority_registry.json")
    records=load_jsonl(root/authority["records_path"])
    if len(records)!=authority["document_count"]:errors.append("DOCUMENT_COUNT_MISMATCH")
    canonical=load_json(root/"documentation_canonical_map.json")
    if canonical["move_count"]!=0:errors.append("MOVE_COUNT_NONZERO")
    if canonical["delete_count"]!=0:errors.append("DELETE_COUNT_NONZERO")
    if canonical["target_collisions"]:errors.append("TARGET_COLLISION")
    acceptance=load_json(root/"reports/acceptance_report.json")
    if not acceptance["passed"]:errors.append("ACCEPTANCE_FAILED")
    handoff=load_json(root/"LCM12A_TO_LCM12B_HANDOFF.json")
    if handoff["runtime_authority_created"] or handoff["live_order_authority_created"] or handoff["capital_authority_created"]:errors.append("AUTHORITY_CREATED")
    return errors
