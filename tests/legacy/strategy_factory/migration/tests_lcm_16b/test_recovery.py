from pathlib import Path

import pytest

from src.engine.tooling.strategy_factory.lcm.lcm_16b.io import load_json, load_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_16b.recovery import run_control_plane_round_trip, run_lcm16a_rehydration


def test_local_recovery_receipt_passes(package_root):
    receipt = load_json(package_root / "recovery_drill_receipt.json")
    assert receipt["local_control_plane_status"] == "PASS"
    assert receipt["lcm16a_rehydration_status"] == "PASS"
    assert receipt["repository_mutated"] is False


def test_round_trip_records_all_pass(package_root):
    rows = load_jsonl(package_root / "records/recovery_round_trip.jsonl")
    assert rows
    assert all(row["restore_status"] == "PASS" for row in rows)
    assert any(row["simulated_loss"] for row in rows)


def test_control_plane_round_trip_reexecutes(repo_root, package_root, tmp_path):
    snapshot = load_jsonl(package_root / "records/control_plane_snapshot.jsonl")
    report, rows = run_control_plane_round_trip(repo_root, snapshot[:25], tmp_path / "drill")
    assert report["status"] == "PASS"
    assert len(rows) == 25


def test_round_trip_rejects_bad_hash(repo_root, package_root, tmp_path):
    snapshot = load_jsonl(package_root / "records/control_plane_snapshot.jsonl")[:2]
    snapshot[0] = {**snapshot[0], "sha256": "sha256:" + "0" * 64}
    with pytest.raises(ValueError, match="immutable recovery source mismatch"):
        run_control_plane_round_trip(repo_root, snapshot, tmp_path / "bad")


def test_lcm16a_rehydration_reexecutes(repo_root):
    report = run_lcm16a_rehydration(repo_root)
    assert report["status"] == "PASS"
    assert report["mismatch_count"] == 0
