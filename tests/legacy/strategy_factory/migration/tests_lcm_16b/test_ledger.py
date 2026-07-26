from src.engine.tooling.strategy_factory.lcm.lcm_16b.io import load_json, load_jsonl


def test_final_ledger_counts(package_root):
    ledger = load_json(package_root / "final_migration_ledger.json")
    assert ledger["phase_count"] == 30
    assert ledger["candidate_path_count"] == 2168
    assert ledger["retained_candidate_count"] == 2168
    assert ledger["executed_deletion_count"] == 0


def test_final_locator_has_every_phase(package_root):
    locator = load_json(package_root / "final_locator_snapshot.json")
    assert locator["phase_locator_count"] == 30
    assert locator["locator_resolution_status"] == "PASS"


def test_control_plane_snapshot_unique(package_root):
    rows = load_jsonl(package_root / "records/control_plane_snapshot.jsonl")
    paths = [row["path"] for row in rows]
    assert len(paths) == len(set(paths))
    assert len(paths) >= 300


def test_program_state_is_not_trading_authority(package_root):
    state = load_json(package_root / "reports/program_state_report.json")
    assert state["migration_program_closed"] is False
    assert state["trading_system_production_authorized"] is False
    assert state["capital_authorized"] is False
