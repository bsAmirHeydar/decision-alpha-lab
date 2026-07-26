import json

import pytest

from src.engine.tooling.strategy_factory.lcm.lcm_14a.io import iter_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_14a.resolver import CompatibilityRedirectResolver


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_resolver_exactly_resolves_all_records(built):
    path = built / "records/compatibility_redirect_records.jsonl"
    resolver = CompatibilityRedirectResolver(path)
    rows = list(iter_jsonl(path))
    for row in rows:
        result = resolver.resolve(row["legacy_locator"], row["consumer_id"])
        assert result.canonical_locator == row["canonical_locator"]
        assert result.canonical_target_digest == row["canonical_target_digest"]
        assert result.warning_code == row["warning_code"]


def test_unknown_locator_fails_closed(built):
    resolver = CompatibilityRedirectResolver(built / "records/compatibility_redirect_records.jsonl")
    with pytest.raises(KeyError, match="UNKNOWN_LEGACY_LOCATOR"):
        resolver.resolve("not/a/known/legacy/locator")


def test_redirect_contracts_are_minimal_and_logic_free(built):
    rows = list(iter_jsonl(built / "records/compatibility_redirect_records.jsonl"))
    forbidden = ("OrderSend", "CTrade", "WebRequest", "importlib", "exec(", "eval(")
    for row in rows:
        contract = built / row["redirect_contract_path"]
        text = contract.read_text(encoding="utf-8")
        assert not any(token in text for token in forbidden)
        value = json.loads(text)
        assert value["domain_logic_present"] is False
        assert value["side_effect_authority"] is False


def test_repository_scan_is_complete_and_external_scope_unknown(built):
    scan = load(built / "active_reference_scan.json")
    assert scan["repository_scope_complete"] is True
    assert scan["external_scope_complete"] is False
    assert scan["external_scope_state"] == "UNKNOWN"
    assert scan["files_scanned"] > 1000
    assert scan["bytes_scanned"] > 1_000_000
    assert scan["record_count"] >= 613


def test_reference_records_retain_low_frequency_occurrences(built):
    rows = list(iter_jsonl(built / "records/active_reference_records.jsonl"))
    assert all(row["match_count"] >= 1 for row in rows)
    assert any(row["match_count"] == 1 for row in rows)
    assert len({row["consumer_id"] for row in rows}) == 613


def test_ambiguous_locator_requires_consumer_scope(built):
    path = built / "records/compatibility_redirect_records.jsonl"
    rows = list(iter_jsonl(path))
    grouped = {}
    for row in rows:
        grouped.setdefault(row["legacy_locator"], []).append(row)
    ambiguous_locator, ambiguous_rows = next(
        (locator, values) for locator, values in grouped.items() if len(values) > 1
    )
    resolver = CompatibilityRedirectResolver(path)
    with pytest.raises(KeyError, match="AMBIGUOUS_LEGACY_LOCATOR"):
        resolver.resolve(ambiguous_locator)
    selected = ambiguous_rows[0]
    result = resolver.resolve(ambiguous_locator, selected["consumer_id"])
    assert result.canonical_locator == selected["canonical_locator"]
