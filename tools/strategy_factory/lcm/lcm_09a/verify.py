from __future__ import annotations
from pathlib import Path
from .canonical import file_digest
from .contracts import validate_contract
from .embedded import validate_candidates
from .errors import VerificationError
from .io import load_json,load_jsonl,nonempty_lines
REQUIRED=("setup_freeze_marker.json","inventory/setup_inventory.jsonl","embedded/embedded_setup_registry.jsonl","families/setup_family_registry.json","variants/setup_variant_registry.jsonl","bindings/setup_context_binding_registry.jsonl","bindings/setup_treatment_binding_registry.jsonl","unknowns/setup_unknown_queue.jsonl","reports/setup_portfolio_summary.json","reports/hostile_review.json","reports/acceptance_report.json","handoff/lcm09a_to_lcm09b_handoff.json","output_manifest.json","setup_freeze_receipt.json")
def verify_package(root:Path)->dict:
    root=root.resolve()
    for rel in REQUIRED:
        if not (root/rel).is_file(): raise VerificationError("missing package artifact: "+rel)
    manifest=load_json(root/"output_manifest.json")
    for row in manifest["files"]:
        p=root/row["path"]
        if not p.is_file() or p.stat().st_size!=row["size_bytes"] or file_digest(p)!=row["sha256"]: raise VerificationError("manifest mismatch: "+row["path"])
    inv=load_jsonl(root/"inventory/setup_inventory.jsonl")
    emb=load_jsonl(root/"embedded/embedded_setup_registry.jsonl")
    variants=load_jsonl(root/"variants/setup_variant_registry.jsonl")
    bindings=load_jsonl(root/"bindings/setup_context_binding_registry.jsonl")
    summary=load_json(root/"reports/setup_portfolio_summary.json")
    hostile=load_json(root/"reports/hostile_review.json")
    acceptance=load_json(root/"reports/acceptance_report.json")
    handoff=load_json(root/"handoff/lcm09a_to_lcm09b_handoff.json")
    if len(inv)!=60 or len(variants)!=60 or summary["contract_count"]!=60: raise VerificationError("setup portfolio count mismatch")
    if len(set(x["setup_id"] for x in inv))!=60: raise VerificationError("duplicate setup identity")
    canonical={"CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1"}
    if any(x["canonical_context_identity_id"] not in canonical|{None} for x in bindings): raise VerificationError("non-canonical Context reference")
    failures=[]
    for p in sorted((root/"setup_contracts").glob("*.json")): failures.extend(validate_contract(load_json(p),canonical))
    failures.extend(validate_candidates(emb))
    if failures: raise VerificationError("contract/candidate failures: "+str(failures[:10]))
    if not hostile["hostile_review_passed"] or not acceptance["acceptance_gate_passed"]: raise VerificationError("acceptance failed")
    if handoff["implementation_authorized_setup_ids"]: raise VerificationError("blocked implementation authority expansion")
    for key in ("consumer_cutover_allowed","source_move_allowed","source_delete_allowed","runtime_authority_created","live_order_authority_created","capital_authority_created"):
        if handoff.get(key): raise VerificationError("authority expansion: "+key)
    return {"passed":True,"freeze_id":summary["freeze_id"],"setup_identity_count":60,"contract_count":60,"embedded_candidate_count":len(emb),"open_unknown_count":summary["open_unknown_count"],"manifest_file_count":manifest["file_count"]}
def verify_installation(repo_root:Path,freeze_root:Path,patch_index:Path)->dict:
    lines=nonempty_lines(patch_index)
    missing=[x for x in lines if not (repo_root/x).exists()]
    if missing: raise VerificationError("patch index missing: "+str(missing[:10]))
    source_mutations=[x for x in lines if x.startswith(("mql5/","lab/10_infrastructure/","lab/11_strategy_factory/python/"))]
    if source_mutations: raise VerificationError("implementation source path in patch: "+str(source_mutations[:10]))
    return {**verify_package(freeze_root),"patch_index_count":len(lines),"installation_passed":True}
