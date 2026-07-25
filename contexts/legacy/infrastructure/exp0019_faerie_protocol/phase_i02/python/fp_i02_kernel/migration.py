"""Explicit manifest migration helpers. No implicit migration is permitted."""
from __future__ import annotations

from typing import Any, Mapping

from .canonical import canonical_sha256
from .errors import FPI02Error


V1_REQUIRED = {"schema_version", "context_id", "symbols", "confirmation_timeframe", "lookback_days"}


def migrate_manifest_v1_to_v2(source: Mapping[str, Any]) -> dict[str, Any]:
    if source.get("schema_version") != "1.0.0":
        raise FPI02Error("FP_RC_CHECKPOINT_VERSION_MISMATCH", "only manifest v1.0.0 can be migrated by this function")
    missing = sorted(V1_REQUIRED - set(source))
    if missing:
        raise FPI02Error("FP_RC_INVALID_CONFIG", "v1 manifest missing required fields", {"missing": missing})
    symbols = list(source["symbols"])
    if len(symbols) != 2 or symbols[0] == symbols[1]:
        raise FPI02Error("FP_RC_SYMBOL_PAIR_INVALID", "v1 symbols must contain two distinct entries")
    timeframe = int(source["confirmation_timeframe"])
    lookback = int(source["lookback_days"])
    if timeframe <= 0 or lookback <= 0:
        raise FPI02Error("FP_RC_INVALID_CONFIG", "v1 timeframe/lookback invalid")
    migrated = {
        "schema_version": "2.0.0",
        "context_id": source["context_id"],
        "decision_set_id": "FP-OWNER-DECISIONS-2026-07-13-V2",
        "profile": "CANONICAL_RESEARCH",
        "symbols": symbols,
        "resolved_confirmation_timeframe_seconds": timeframe,
        "historical_n_depth": lookback,
        "lookback_policy": "CALENDAR_DAY_DEPTH",
        "replace_missing_offsets": False,
        "quota_consumption_policy": "UNSET",
        "open_decisions": ["FP-DEC-012"],
        "migration": {
            "from_schema_version": "1.0.0",
            "source_hash": canonical_sha256(source),
            "migration_id": "FP-MIGRATE-MANIFEST-1_TO_2@1.0.0",
        },
    }
    migrated["migration"]["result_hash"] = canonical_sha256(migrated)
    return migrated
