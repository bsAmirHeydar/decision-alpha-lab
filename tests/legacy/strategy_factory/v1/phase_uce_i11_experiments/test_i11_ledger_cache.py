from dataclasses import replace

import pytest

from strategy_factory_experiments_v3.cache import ContentAddressedCache
from strategy_factory_experiments_v3.canonical import canonical_sha256
from strategy_factory_experiments_v3.enums import CacheStatus, LedgerAction
from strategy_factory_experiments_v3.errors import ExperimentError
from strategy_factory_experiments_v3.ledger import SelectionLedger


def test_selection_ledger_is_hash_chained_and_tamper_evident():
    ledger = SelectionLedger("exp", "a" * 64)
    first = ledger.append(trial_id="t1", node_id="n1", action=LedgerAction.ATTEMPTED, reason_code="start")
    second = ledger.append(trial_id="t1", node_id="n1", action=LedgerAction.SUCCEEDED, reason_code="done")
    assert second.previous_entry_hash == first.entry_hash
    assert ledger.verify()
    ledger._entries[1] = replace(second, reason_code="tampered")
    assert not ledger.verify()


def test_every_report_model_must_be_selected_or_ensembled():
    ledger = SelectionLedger("exp", "a" * 64)
    ledger.append(trial_id="t1", node_id="n1", action=LedgerAction.SELECTED, reason_code="best")
    ledger.assert_report_models_accounted(("t1",))
    with pytest.raises(ExperimentError, match="report_model_missing_from_ledger"):
        ledger.assert_report_models_accounted(("t1", "t2"))


def test_cache_valid_roundtrip_and_disk_resume(tmp_path):
    cache = ContentAddressedCache(tmp_path)
    inputs = ("a" * 64, "b" * 64)
    provenance = "c" * 64
    record = cache.put(
        namespace="uce_i11",
        artifact_kind="predictions",
        producer_version="1.0.0",
        schema_version="1.0.0",
        input_hashes=inputs,
        provenance_hash=provenance,
        payload=b"payload",
        created_sequence=1,
    )
    resumed = ContentAddressedCache(tmp_path)
    lookup = resumed.lookup(
        record.cache_key,
        producer_version="1.0.0",
        schema_version="1.0.0",
        input_hashes=inputs,
        provenance_hash=provenance,
    )
    assert lookup.status is CacheStatus.VALID
    assert resumed.payload(record.cache_key) == b"payload"


def test_cache_rejects_stale_incompatible_and_corrupt_entries():
    cache = ContentAddressedCache()
    inputs = ("a" * 64,)
    provenance = "c" * 64
    record = cache.put(
        namespace="uce_i11",
        artifact_kind="model",
        producer_version="1.0.0",
        schema_version="1.0.0",
        input_hashes=inputs,
        provenance_hash=provenance,
        payload=b"model",
        created_sequence=1,
    )
    assert cache.lookup(record.cache_key, producer_version="1.0.1", schema_version="1.0.0", input_hashes=inputs, provenance_hash=provenance).status is CacheStatus.STALE
    assert cache.lookup(record.cache_key, producer_version="1.0.0", schema_version="1.0.0", input_hashes=("b" * 64,), provenance_hash=provenance).status is CacheStatus.INCOMPATIBLE
    cache.corrupt_for_test(record.cache_key, b"corrupt")
    assert cache.lookup(record.cache_key, producer_version="1.0.0", schema_version="1.0.0", input_hashes=inputs, provenance_hash=provenance).status is CacheStatus.CORRUPT


def test_cache_miss_is_explicit():
    cache = ContentAddressedCache()
    lookup = cache.lookup(
        "a" * 64,
        producer_version="1.0.0",
        schema_version="1.0.0",
        input_hashes=("b" * 64,),
        provenance_hash="c" * 64,
    )
    assert lookup.status is CacheStatus.MISS
    assert lookup.reason_code == "cache_key_not_found"
