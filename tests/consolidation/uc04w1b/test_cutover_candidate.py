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


def test_cutover_candidate_is_bounded_and_non_mutating(repo_root: Path, tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    receipt = build_native_evidence(repo_root, evidence)
    review_document = review_native_receipt(repo_root, receipt)
    review = evidence / "independent_native_review.json"
    write_json(review, review_document)
    before_hashes = {path: sha256_file(repo_root / path) for path, _, _ in MEMBERS}

    output = tmp_path / "candidate"
    candidate_root = build_cutover_candidate(repo_root, receipt, review, output)
    payload = candidate_root / "payload"
    manifest = json.loads((candidate_root / "CUTOVER_CANDIDATE_MANIFEST.json").read_text(encoding="utf-8"))

    assert manifest["status"] == "GENERATED_PENDING_POST_CUTOVER_NATIVE_QUALIFICATION"
    assert manifest["consumer_count"] == 10
    assert manifest["active_call_site_count"] == 41
    assert manifest["implementation_authority"] is False
    assert (payload / PRODUCTION_INCLUDE).is_file()
    assert len(manifest["patch_paths"]) == 12

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
        assert all(not name.startswith("/") and ".." not in Path(name).parts for name in names)


def test_cutover_candidate_rollback_restores_all_consumers(repo_root: Path, tmp_path: Path) -> None:
    receipt = build_native_evidence(repo_root, tmp_path / "evidence")
    review = receipt.parent / "independent_native_review.json"
    write_json(review, review_native_receipt(repo_root, receipt))
    candidate = build_cutover_candidate(repo_root, receipt, review, tmp_path / "candidate")
    rollback = json.loads((candidate / "ROLLBACK_MANIFEST.json").read_text(encoding="utf-8"))
    assert rollback["status"] == "READY"
    assert len(rollback["restore_files"]) == 10
    assert len(rollback["delete_files"]) == 2
