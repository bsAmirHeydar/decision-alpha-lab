from __future__ import annotations

import json
from pathlib import Path

from tools.consolidation.uc04complete.build import CAPABILITIES, build_records
from tools.consolidation.uc04complete.verify import verify

ROOT = Path(__file__).resolve().parents[3]


def test_complete_records_are_reproducible() -> None:
    expected = build_records(ROOT)
    for name, value in expected.items():
        stored = json.loads((ROOT / "registry/consolidation/uc04/complete" / name).read_text(encoding="utf-8"))
        assert stored == value


def test_selected_candidate_partition_is_complete() -> None:
    records = build_records(ROOT)
    ledger = records["capability_implementation_ledger.json"]
    variants = records["explicit_variant_registry.json"]
    assert ledger["selected_capability_count"] == 14
    assert ledger["consumer_adapter_count"] == 109
    assert variants["historical_candidate_count"] == 205
    assert variants["explicit_variant_count"] == 191
    assert 14 + 191 == 205


def test_every_selected_capability_has_one_canonical_function() -> None:
    for spec in CAPABILITIES:
        text = (ROOT / spec["include"]).read_text(encoding="utf-8")
        assert f"{spec['function']}(" in text
        assert "CTX_RTHP" not in text
        assert "RTHP" not in text


def test_every_historical_member_is_a_local_adapter() -> None:
    ledger = build_records(ROOT)["capability_implementation_ledger.json"]
    by_id = {item["candidate_id"]: item for item in CAPABILITIES}
    for capability in ledger["capabilities"]:
        token = by_id[capability["candidate_id"]]["adapter_token"]
        for member in capability["members"]:
            text = (ROOT / member["artifact_path"]).read_text(encoding="utf-8")
            assert token in text
            assert member["adapter_call_present"] is True


def test_exit_record_has_no_authority() -> None:
    exit_record = build_records(ROOT)["uc04_exit_decision.json"]
    assert exit_record["implementation_status"] == "COMPLETE"
    assert exit_record["native_seal_status"] == "PENDING_INSTALL_HOST"
    assert exit_record["uc05_handoff_authorized"] is False
    assert exit_record["deletion_authority"] is False
    assert exit_record["runtime_authority"] is False
    assert exit_record["order_authority"] is False
    assert exit_record["capital_authority"] is False


def test_native_contract_covers_all_impacted_mq5_targets() -> None:
    contract = build_records(ROOT)["native_acceptance_contract.json"]
    assert contract["compile_target_count"] == len(contract["compile_targets"])
    assert contract["compile_target_count"] >= 30
    assert "mql5/Tests/Scripts/UC04/UC04_Phase4SharedPrimitivesSelfTest.mq5" in contract["compile_targets"]
    assert contract["live_trading_allowed"] is False
    assert contract["dll_import_allowed"] is False


def test_complete_verifier_passes_without_upstream_replay() -> None:
    assert verify(ROOT, include_upstream=False) == []


def test_native_seal_tooling_is_fail_closed_and_windows_ps51_compatible() -> None:
    script = (ROOT / "tools/consolidation/uc04complete/Invoke-UC04CompleteNativeSeal.ps1").read_text(encoding="utf-8")
    assert "PYTHONDONTWRITEBYTECODE" in script
    assert "0\\s+errors" in script
    assert "0\\s+warnings" in script
    assert "AllowLiveTrading=0" in script
    assert "AllowDllImport=0" in script
    assert "ShutdownTerminal=1" in script
    assert "-FinalizeRepository" in script or "$FinalizeRepository" in script
    assert "git add" not in script
    assert "git commit" not in script
    assert "New-Item -ItemType Directory -LiteralPath" not in script


def test_native_seal_schemas_are_closed_and_valid() -> None:
    from jsonschema import Draft202012Validator

    names = (
        "native_seal_receipt.schema.json",
        "native_seal_review.schema.json",
        "uc04_acceptance.schema.json",
        "uc05_handoff_decision.schema.json",
    )
    for name in names:
        schema = json.loads((ROOT / "schemas/consolidation/uc04/complete" / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False


def test_optional_acceptance_records_are_absent_before_native_pass() -> None:
    assert not (ROOT / "registry/consolidation/uc04/complete/uc04_acceptance.json").exists()
    assert not (ROOT / "registry/consolidation/uc04/complete/uc05_handoff_decision.json").exists()
