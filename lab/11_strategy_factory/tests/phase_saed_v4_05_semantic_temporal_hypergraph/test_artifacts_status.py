import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_acceptance_evidence_denies_unearned_claims():
    evidence = load("lab/11_strategy_factory/artifacts/SAED_V4_05_ACCEPTANCE_EVIDENCE.json")
    assert evidence["real_alpha_claimed"] is False
    assert evidence["model_trained"] is False
    assert evidence["treatment_selected"] is False
    assert evidence["runtime_activated"] is False
    assert evidence["orders_sent"] is False


def test_phase_status_is_reference_only():
    status = load("lab/11_strategy_factory/phase_status/SAED_V4_05.json")
    assert status["implementation_status"] == "reference_implementation_complete"
    assert status["production_authorization"] is False
    assert status["metaeditor_compile"] == "pending_local_windows"
    assert status["next_phase"] == "SAED_V4_06"


def test_schema_registry_hashes_current_files():
    import hashlib

    registry = load("lab/11_strategy_factory/artifacts/SAED_V4_05_SCHEMA_REGISTRY.json")
    assert registry["schema_count"] == len(registry["entries"])
    for entry in registry["entries"]:
        path = ROOT / "lab/11_strategy_factory/schemas/saed_v4_05" / entry["name"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
        assert entry["closed"] is True
