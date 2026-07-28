from __future__ import annotations

import json
import zipfile
from pathlib import Path

from tools.consolidation.uc04w1.characterize import MEMBERS
from tools.consolidation.uc04w1b.contracts import (
    CANONICAL_FUNCTION_NAME,
    PRODUCTION_INCLUDE,
    PRODUCTION_INCLUDE_DIRECTIVE,
    sha256_file,
    write_json,
)
from tools.consolidation.uc04w1b.cutover_candidate import build_cutover_candidate
from tools.consolidation.uc04w1b.native_review import review_native_receipt
from tests.consolidation.uc04w1b.test_native_review import build_native_evidence

TRANSITION = Path("registry/consolidation/uc04/complete/w1_candidate_transition.json")


def test_cutover_candidate_or_accepted_transition_is_bounded(repo_root: Path, tmp_path: Path) -> None:
    transition_path = repo_root / TRANSITION
    if transition_path.is_file():
        transition = json.loads(transition_path.read_text(encoding="utf-8"))
        assert transition["status"] == "PASS"
        assert transition["member_count"] == 10
        assert transition["active_call_site_count"] == 41
        assert transition["semantic_change_authority"] is False
        assert transition["deletion_authority"] is False
        for row in transition["members"]:
            assert sha256_file(repo_root / row["artifact_path"]) == row["current_sha256"]
            assert row["adapter_token"] in (repo_root / row["artifact_path"]).read_text(encoding="utf-8-sig")
        return

    evidence = tmp_path / "evidence"
    receipt = build_native_evidence(repo_root, evidence)
    review = evidence / "independent_native_review.json"
    write_json(review, review_native_receipt(repo_root, receipt))
    before_hashes = {path: sha256_file(repo_root / path) for path, _, _ in MEMBERS}
    candidate_root = build_cutover_candidate(repo_root, receipt, review, tmp_path / "candidate")
    payload = candidate_root / "payload"
    manifest = json.loads((candidate_root / "CUTOVER_CANDIDATE_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "GENERATED_PENDING_POST_CUTOVER_NATIVE_QUALIFICATION"
    assert manifest["consumer_count"] == 10
    assert (payload / PRODUCTION_INCLUDE).is_file()
    for path, function_name, _ in MEMBERS:
        candidate = (payload / path).read_text(encoding="utf-8")
        assert candidate.count(PRODUCTION_INCLUDE_DIRECTIVE) == 1
        assert candidate.count(f"return {CANONICAL_FUNCTION_NAME}(value);") == 1
        assert function_name in candidate
        assert sha256_file(repo_root / path) == before_hashes[path]
    archives = list(candidate_root.glob("ALPHA_LAB_UC04_W1B_CUTOVER_CANDIDATE_*.zip"))
    assert len(archives) == 1
    with zipfile.ZipFile(archives[0]) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names))


def test_rollback_or_transition_recovery_is_complete(repo_root: Path, tmp_path: Path) -> None:
    transition_path = repo_root / TRANSITION
    if transition_path.is_file():
        transition = json.loads(transition_path.read_text(encoding="utf-8"))
        assert transition["unexplained_behavior_delta_count"] == 0
        assert all(row["current_sha256"].startswith("sha256:") for row in transition["members"])
        return
    receipt = build_native_evidence(repo_root, tmp_path / "evidence")
    review = receipt.parent / "independent_native_review.json"
    write_json(review, review_native_receipt(repo_root, receipt))
    candidate = build_cutover_candidate(repo_root, receipt, review, tmp_path / "candidate")
    rollback = json.loads((candidate / "ROLLBACK_MANIFEST.json").read_text(encoding="utf-8"))
    assert rollback["status"] == "READY"
    assert len(rollback["restore_files"]) == 10
    assert len(rollback["delete_files"]) == 2
