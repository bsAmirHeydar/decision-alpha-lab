import pytest

from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.migration import migrate_manifest_v1_to_v2


def source():
    return {"schema_version": "1.0.0", "context_id": "FP-CONTEXT-001", "symbols": ["SPXUSD", "NDXUSD"], "confirmation_timeframe": 3600, "lookback_days": 13}


def test_v1_to_v2_migration_is_explicit_and_deterministic():
    first = migrate_manifest_v1_to_v2(source())
    second = migrate_manifest_v1_to_v2(source())
    assert first == second
    assert first["quota_consumption_policy"] == "UNSET"
    assert first["open_decisions"] == ["FP-DEC-012"]
    assert first["replace_missing_offsets"] is False


def test_migration_rejects_unknown_source_version():
    payload = source()
    payload["schema_version"] = "0.9.0"
    with pytest.raises(FPI02Error) as exc:
        migrate_manifest_v1_to_v2(payload)
    assert exc.value.code == "FP_RC_CHECKPOINT_VERSION_MISMATCH"


def test_migration_rejects_missing_field_and_invalid_pair():
    payload = source()
    del payload["lookback_days"]
    with pytest.raises(FPI02Error):
        migrate_manifest_v1_to_v2(payload)
    payload = source()
    payload["symbols"] = ["SPXUSD", "SPXUSD"]
    with pytest.raises(FPI02Error):
        migrate_manifest_v1_to_v2(payload)
