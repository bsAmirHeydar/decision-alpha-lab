from __future__ import annotations
from pathlib import Path
from .canonical import file_digest, digest_object
from .errors import VerificationError
from .io import load_json, load_jsonl, nonempty_lines
from .service import build_reference_closure

REQUIRED = (
    "context_wave_migration_marker.json", "input/lcm08a_portfolio_binding.json", "input/lcm08b_pilot_binding.json",
    "registries/context_package_registry.jsonl", "registries/context_parity_registry.jsonl",
    "registries/context_variance_registry.jsonl", "registries/context_blocker_registry.jsonl",
    "reports/context_portfolio_closure_report.json", "reports/hostile_review.json", "reports/acceptance_report.json",
    "handoff/lcm08c_to_lcm09a_handoff.json", "output_manifest.json", "context_wave_migration_receipt.json",
)

def verify_package(root: Path) -> dict:
    root = root.resolve()
    for rel in REQUIRED:
        if not (root / rel).is_file(): raise VerificationError(f"missing package artifact: {rel}")
    manifest = load_json(root / "output_manifest.json")
    for row in manifest["files"]:
        p = root / row["path"]
        if not p.is_file() or p.stat().st_size != row["size_bytes"] or file_digest(p) != row["sha256"]:
            raise VerificationError(f"manifest mismatch: {row['path']}")
    closure = load_json(root / "reports/context_portfolio_closure_report.json")
    hostile = load_json(root / "reports/hostile_review.json")
    acceptance = load_json(root / "reports/acceptance_report.json")
    handoff = load_json(root / "handoff/lcm08c_to_lcm09a_handoff.json")
    packages = load_jsonl(root / "registries/context_package_registry.jsonl")
    parity = load_jsonl(root / "registries/context_parity_registry.jsonl")
    blockers = load_jsonl(root / "registries/context_blocker_registry.jsonl")
    if closure["portfolio_record_count"] != 321 or not closure["all_portfolio_records_accounted"]: raise VerificationError("portfolio accounting failed")
    if closure["migrated_cutover_ready_count"] != 1 or closure["blocked_count"] != 320: raise VerificationError("disposition count mismatch")
    if len(packages) != 321 or len(parity) != 321 or len(blockers) != 320: raise VerificationError("registry count mismatch")
    if closure["locator_collision_count"] != 0 or closure["migrated_hard_parity_failure_count"] != 0: raise VerificationError("non-compensatory gate failed")
    if not hostile["hostile_review_passed"] or not acceptance["acceptance_gate_passed"]: raise VerificationError("acceptance failed")
    for key in ("consumer_cutover_allowed","source_move_allowed","source_delete_allowed","runtime_authority_created","live_order_authority_created","capital_authority_created"):
        if handoff.get(key): raise VerificationError(f"authority expansion: {key}")
    return {"passed":True,"closure_id":closure["closure_id"],"portfolio_record_count":321,"migrated_count":1,"blocked_count":320,"manifest_file_count":manifest["file_count"]}

def verify_installation(repo_root: Path, closure_root: Path, patch_index: Path) -> dict:
    lines = nonempty_lines(patch_index)
    missing = [x for x in lines if not (repo_root / x).exists()]
    if missing: raise VerificationError(f"patch index missing: {missing[:10]}")
    expected = build_reference_closure(repo_root)
    actual = load_json(closure_root / "reports/context_portfolio_closure_report.json")
    if expected["closure_id"] != actual["closure_id"]: raise VerificationError("closure identity mismatch")
    if expected["closure_report"]["closure_report_digest"] != actual["closure_report_digest"]: raise VerificationError("closure digest mismatch")
    return {**verify_package(closure_root),"patch_index_count":len(lines),"installation_passed":True}
