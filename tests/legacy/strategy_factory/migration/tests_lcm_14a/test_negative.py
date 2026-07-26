import json
import shutil

from src.engine.tooling.strategy_factory.lcm.lcm_14a.verify import verify_package


def clone(built, tmp_path):
    destination = tmp_path / "package"
    shutil.copytree(built, destination)
    return destination


def rewrite_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")


def test_floating_redirect_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/compatibility_redirect_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["floating_version_resolution"] = True
    rewrite_jsonl(path, rows)
    assert "REDIRECT_LOGIC_OR_AUTHORITY" in verify_package(package)


def test_redirect_domain_logic_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/compatibility_redirect_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["domain_logic_present"] = True
    rewrite_jsonl(path, rows)
    assert "REDIRECT_LOGIC_OR_AUTHORITY" in verify_package(package)


def test_late_warning_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/compatibility_redirect_records.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["warning_before_resolution"] = False
    rewrite_jsonl(path, rows)
    assert "WARNING_ORDER" in verify_package(package)


def test_external_unknown_cannot_be_ignored(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "records/external_consumer_evidence.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    rows[0]["ignored"] = True
    rewrite_jsonl(path, rows)
    assert "EXTERNAL_UNKNOWN_HANDLING" in verify_package(package)


def test_quarantine_authority_fails(built, tmp_path):
    package = clone(built, tmp_path)
    path = package / "LCM14A_TO_LCM14B_HANDOFF.json"
    value = json.loads(path.read_text())
    value["quarantine_authority_created"] = True
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    assert "AUTHORITY:handoff" in verify_package(package)


def test_contract_tamper_fails_output_manifest(built, tmp_path):
    package = clone(built, tmp_path)
    contract = next((package / "redirect_contracts").rglob("*.json"))
    contract.write_text(contract.read_text() + " ", encoding="utf-8")
    errors = verify_package(package)
    assert any(error.startswith("OUTPUT_HASH:") for error in errors)
