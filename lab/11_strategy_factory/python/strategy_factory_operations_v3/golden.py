from __future__ import annotations

from strategy_factory_qualification_v3.contracts import ReleaseManifest
from strategy_factory_qualification_v3.enums import ReleaseStage

from .contracts import (
    DeploymentTarget,
    EndOfDayReport,
    OperationsPolicy,
    ProspectiveWindow,
    ReconciliationReport,
    RiskEnvelope,
    TelemetrySnapshot,
)
from .enums import DeploymentStage

NOW = 1_800_000_000_000
H1 = "1" * 64
H2 = "2" * 64
H3 = "3" * 64
H4 = "4" * 64
H5 = "5" * 64
H6 = "6" * 64
H7 = "7" * 64
H8 = "8" * 64


def release(stage: ReleaseStage = ReleaseStage.MICRO_LIVE, risk: float = 0.25) -> ReleaseManifest:
    live = stage in (ReleaseStage.MICRO_LIVE, ReleaseStage.LIMITED_LIVE, ReleaseStage.PRODUCTION)
    return ReleaseManifest(
        manifest_id="release:golden",
        schema_version="1.0.0",
        release_version="1.0.0",
        source_commit="abc123",
        qualification_report_hash=H1,
        environment_hash=H2,
        generation_hash=H3,
        stage=stage,
        authority_order=live,
        authority_broker=live,
        max_risk_units=risk if live else 0.0,
        approved_by="i18-approver",
        approved_at_ms=NOW - 100_000,
        artifact_refs=(),
        rollback_generation_hash=H4,
        expires_at_ms=NOW + 10_000_000,
    )


def target() -> DeploymentTarget:
    return DeploymentTarget("target-1", H2, H5, (H6,), ("EURUSD", "GBPUSD"), ("terminal-1",), "UTC", NOW - 50_000)


def envelope(total: float = 0.25) -> RiskEnvelope:
    return RiskEnvelope("env-1", total, total, min(0.05, total), 0.15, 0.30, 3, 5, {"EURUSD": total, "GBPUSD": total}, {"context-1": total})


def policy() -> OperationsPolicy:
    minimums = {"shadow": 2, "micro_live": 3, "limited_live": 5, "production": 10}
    events = {"shadow": 100, "micro_live": 200, "limited_live": 500, "production": 1000}
    days = {"shadow": 1, "micro_live": 2, "limited_live": 5, "production": 20}
    return OperationsPolicy("ops-policy-1", "1.0.0", 5_000, 60_000, 100.0, 100, 64.0, 0.05, 0.20, 10_000, 60, True, True, True, minimums, events, days)


def telemetry(**changes) -> TelemetrySnapshot:
    values = dict(
        snapshot_id="telemetry-1",
        environment_hash=H2,
        generation_hash=H3,
        captured_at_ms=NOW,
        last_heartbeat_ms=NOW - 100,
        max_feature_age_ms=1000,
        p99_latency_ms=10.0,
        queue_depth=1,
        memory_growth_mb=1.0,
        broker_connected=True,
        history_synchronized=True,
        open_positions=0,
        open_risk_units=0.0,
        reserved_risk_units=0.0,
        daily_pnl_units=0.0,
        weekly_pnl_units=0.0,
        reject_rate=0.0,
        drift_score=0.0,
        duplicate_action_count=0,
        stale_action_count=0,
        unreserved_action_count=0,
        critical_error_count=0,
    )
    values.update(changes)
    return TelemetrySnapshot(**values)


def reconciliation(**changes) -> ReconciliationReport:
    values = dict(
        report_id="reconciliation-1",
        environment_hash=H2,
        generation_hash=H3,
        expected_reservation_hash=H5,
        observed_reservation_hash=H5,
        expected_order_hash=H6,
        observed_order_hash=H6,
        expected_position_hash=H7,
        observed_position_hash=H7,
        orphan_order_count=0,
        orphan_position_count=0,
        missing_order_count=0,
        missing_position_count=0,
        duplicate_intent_count=0,
        unreserved_position_count=0,
        reconciled_at_ms=NOW,
    )
    values.update(changes)
    return ReconciliationReport(**values)


def window(stage: DeploymentStage = DeploymentStage.SHADOW, **changes) -> ProspectiveWindow:
    values = dict(
        window_id="window-1",
        stage=stage,
        environment_hash=H2,
        generation_hash=H3,
        started_at_ms=NOW - 10_000_000,
        ended_at_ms=NOW - 1000,
        sessions=20,
        events=5000,
        calendar_days=30,
        reconciliations=100,
        reconciliation_failures=0,
        high_incidents=0,
        critical_incidents=0,
        policy_breaches=0,
        max_drawdown_units=0.05,
        reject_rate=0.0,
        p99_latency_ms=10.0,
        drift_score=0.0,
        evidence_hashes=(H8,),
    )
    values.update(changes)
    return ProspectiveWindow(**values)


def eod(**changes) -> EndOfDayReport:
    values = dict(
        report_id="eod-1",
        environment_hash=H2,
        generation_hash=H3,
        trading_day="2026-07-15",
        reservation_hash=H4,
        order_hash=H5,
        position_hash=H6,
        ledger_hash=H7,
        all_events_persisted=True,
        all_intents_terminal=True,
        exact_reconciliation=True,
        unresolved_high_incidents=0,
        unresolved_critical_incidents=0,
        daily_loss_units=0.0,
        evidence_hashes=(H8,),
    )
    values.update(changes)
    return EndOfDayReport(**values)
