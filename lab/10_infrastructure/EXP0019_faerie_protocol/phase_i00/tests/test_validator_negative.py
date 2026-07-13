from copy import deepcopy
import json

from fp_i00_governance.validator import GovernanceValidator
from conftest import REPO_ROOT, load_policy


def codes(report):
    return {issue.code for issue in report.errors}


def test_missing_dependency_blocks():
    policy = deepcopy(load_policy())
    policy["shared_dependencies"][0]["relative_root"] = "mql5/Include/DOES_NOT_EXIST"
    report = GovernanceValidator(REPO_ROOT, policy).run()
    assert "FP_I00_DEPENDENCY_MISSING" in codes(report)


def test_open_decision_cannot_be_silently_closed(tmp_path):
    policy = deepcopy(load_policy())
    source = REPO_ROOT / policy["open_decisions_path"]
    data = json.loads(source.read_text())
    data["open_decisions"][0]["canonical_live_behavior"] = "ENABLED"
    mutated = tmp_path / "open.json"
    mutated.write_text(json.dumps(data), encoding="utf-8")
    policy["open_decisions_path"] = str(mutated)
    report = GovernanceValidator(REPO_ROOT, policy).run()
    assert "FP_I00_LIVE_GATE_NOT_CLOSED" in codes(report)


def test_relation_registry_mutation_blocks(tmp_path):
    policy = deepcopy(load_policy())
    source = REPO_ROOT / policy["relation_registry_path"]
    data = json.loads(source.read_text())
    data["relations"] = list(reversed(data["relations"]))
    mutated = tmp_path / "relations.json"
    mutated.write_text(json.dumps(data), encoding="utf-8")
    policy["relation_registry_path"] = str(mutated)
    report = GovernanceValidator(REPO_ROOT, policy).run()
    assert "FP_I00_RELATION_REGISTRY_INVALID" in codes(report)


def test_runtime_indicator_file_blocks_phase(tmp_path):
    policy = deepcopy(load_policy())
    runtime = tmp_path / "EXP0019_FaerieProtocol_Context.mq5"
    runtime.write_text("#property indicator_chart_window\n", encoding="utf-8")
    policy["forbidden_runtime_paths"] = [str(runtime)]
    report = GovernanceValidator(REPO_ROOT, policy).run()
    assert "FP_I00_RUNTIME_FILE_CREATED" in codes(report)


def test_manifest_tamper_blocks(tmp_path):
    policy = deepcopy(load_policy())
    source = REPO_ROOT / policy["baseline_manifest_path"]
    data = json.loads(source.read_text())
    data["next_phase"] = "FP-I99"
    mutated = tmp_path / "manifest.json"
    mutated.write_text(json.dumps(data), encoding="utf-8")
    policy["baseline_manifest_path"] = str(mutated)
    report = GovernanceValidator(REPO_ROOT, policy).run()
    assert "FP_I00_BASELINE_MANIFEST_HASH_MISMATCH" in codes(report)
