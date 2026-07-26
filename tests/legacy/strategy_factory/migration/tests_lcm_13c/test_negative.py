import json
import shutil

from src.engine.tooling.strategy_factory.lcm.lcm_13c.verify import verify_package


def rewrite_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def clone(built, tmp_path):
    destination = tmp_path / "package"
    shutil.copytree(built, destination)
    return destination


def test_missing_rollback_report_fails(built, tmp_path):
    package = clone(built, tmp_path)
    next((package / "rollback_rehearsal_reports").glob("*.json")).unlink()
    errors = verify_package(package)
    assert any(error.startswith("ROLLBACK_REPORT:") or error.startswith("OUTPUT_MISSING:") for error in errors)


def test_reopen_required_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/cutover_closure_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["closure_state"] = "REOPEN_REQUIRED"
    rewrite_jsonl(path, rows)
    assert "REOPEN_REQUIRED" in verify_package(package)


def test_missing_state_plane_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/state_recovery_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line][1:]
    rewrite_jsonl(path, rows)
    errors = verify_package(package)
    assert "STATE_COUNT" in errors or "STATE_PLANE_COVERAGE" in errors


def test_live_mutation_claim_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/state_recovery_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["live_state_mutation_performed"] = True
    rewrite_jsonl(path, rows)
    assert "LIVE_STATE_MUTATION" in verify_package(package)


def test_deletion_authority_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "LCM13C_TO_LCM14A_HANDOFF.json"
    value = json.loads(path.read_text())
    value["deletion_authority_created"] = True
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    assert "AUTHORITY:handoff" in verify_package(package)


def test_output_tamper_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "residual_cutover_risk.md"
    path.write_text(path.read_text() + "tamper\n")
    assert "OUTPUT_HASH:residual_cutover_risk.md" in verify_package(package)
