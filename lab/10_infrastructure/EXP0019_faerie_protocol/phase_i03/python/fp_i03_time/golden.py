"""Golden FP-I03 fixtures and cross-language vector material."""
from __future__ import annotations
from datetime import datetime, timezone
from fp_i02_kernel.canonical import canonical_sha256
from fp_i02_kernel.contracts import SymbolPair
from .calendar import build_session, build_trading_day, build_week_from_sunday, previous_completed_week, snapshot
from .contracts import TimeKernelConfig, canonical_registry_snapshot
from .enums import CalendarSegment, LocalResolutionPolicy
from .time_math import dst_end_utc, dst_start_utc, epoch_ms, resolve_local, utc_to_new_york

UTC = timezone.utc


def utc_ms(iso: str) -> int:
    value = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return epoch_ms(value)


def golden_snapshots():
    points = {
        "A_OPEN": utc_ms("2026-07-12T22:00:00Z"),  # Sunday 18:00 EDT
        "A_END": utc_ms("2026-07-13T08:00:00Z"),
        "L_END": utc_ms("2026-07-13T13:30:00Z"),
        "N_END": utc_ms("2026-07-13T21:00:00Z"),
        "GAP_MID": utc_ms("2026-07-13T21:30:00Z"),
        "WEEKEND": utc_ms("2026-07-18T12:00:00Z"),
    }
    return {key: snapshot(value) for key, value in points.items()}


def golden_vector_material() -> dict:
    config = TimeKernelConfig()
    snaps = golden_snapshots()
    registry = canonical_registry_snapshot()
    pair = SymbolPair("SPXUSD", "NDXUSD")
    monday = datetime(2026, 7, 13).date()
    tday = build_trading_day(monday, config)[0]
    sessions = {code.value: build_session(monday, code, None, config)[0] for code in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N)}
    week = build_week_from_sunday(datetime(2026, 7, 12).date(), None, config)[0]
    prior = previous_completed_week(utc_ms("2026-07-15T12:00:00Z"), config)
    ambiguous = resolve_local(datetime(2026, 11, 1, 1, 30), LocalResolutionPolicy.EARLIEST, config)
    nonexistent = resolve_local(datetime(2026, 3, 8, 2, 30), LocalResolutionPolicy.REJECT, config)
    window_ids = {code: item.to_i02_window_key("FP-CONTEXT-001", pair.pair_id, "FIXTURE-REV-001").window_id for code, item in sessions.items()}
    material = {
        "config_hash": config.config_hash,
        "registry_hash": registry.registry_hash,
        "time_contract_registry_hash": __import__("fp_i03_time.registry", fromlist=["DEFAULT_TIME_CONTRACT_REGISTRY"]).DEFAULT_TIME_CONTRACT_REGISTRY.registry_hash,
        "dst_start_utc": dst_start_utc(2026, config).isoformat(),
        "dst_end_utc": dst_end_utc(2026, config).isoformat(),
        "trading_day_id": tday.trading_day_id,
        "trading_day_window_id": tday.window_id,
        "session_window_ids": {code: item.window_id for code, item in sessions.items()},
        "i02_window_ids": window_ids,
        "week_id": week.week_id,
        "week_window_id": week.window_id,
        "previous_completed_week_id": prior.week_id,
        "snapshot_ids": {key: value.snapshot_id for key, value in snaps.items()},
        "segments": {key: value.segment.value for key, value in snaps.items()},
        "ambiguous_candidates": ambiguous.candidate_utc_ms,
        "nonexistent_candidate_count": len(nonexistent.candidate_utc_ms),
    }
    material["vector_hash"] = canonical_sha256(material)
    return material
