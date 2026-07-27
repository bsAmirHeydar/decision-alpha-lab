from __future__ import annotations

import hashlib
import json


def sha(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def test_semantic_baseline_freeze_matches_current_artifacts(repo_root):
    freeze = json.loads((repo_root / "registry/consolidation/uc04/w0/semantic_baseline_freeze.json").read_text())
    assert freeze["artifact_count"] == len(freeze["artifacts"])
    for row in freeze["artifacts"]:
        target = repo_root / row["path"]
        assert target.is_file(), row["path"]
        assert sha(target) == row["sha256"], row["path"]


def test_rthp_recovery_receipt_is_clean_pass(repo_root):
    receipt = json.loads((repo_root / "registry/consolidation/uc04/w0/rthp_recovery_receipt.json").read_text())
    assert receipt["status"] == "PASS"
    assert receipt["passed_test_count"] == 166
    assert receipt["failed_test_count"] == 0
    assert sum(row["passed"] for row in receipt["qualification_commands"]) == 166
    assert receipt["error_count"] == 0
    assert receipt["semantic_change"] is False


def test_rthp_registrations_use_canonical_existing_paths(repo_root):
    registration = json.loads((repo_root / "registry/history/strategy_factory/contexts/rthp/v1/rthp_ai_input_registration.json").read_text())
    assert registration["feature_catalog"].startswith("contexts/legacy/")
    assert (repo_root / registration["feature_catalog"]).is_file()
    assert (repo_root / registration["source_schema"]).is_file()
    assert all("lab/11_strategy_factory" not in value for value in registration.values() if isinstance(value, str))


def test_acl03_acceptance_preserves_zero_authority(repo_root):
    report = json.loads((repo_root / "contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1/generated/acl_03/RTHP_ACL03_ACCEPTANCE_REPORT.json").read_text())
    assert report["status"] == "PASS"
    assert report["semantic_change"] is False
    assert report["runtime_authority_created"] is False
    assert report["order_authority_created"] is False
    assert report["capital_authority_created"] is False
