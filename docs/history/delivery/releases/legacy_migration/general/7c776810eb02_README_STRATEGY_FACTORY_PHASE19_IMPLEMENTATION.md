# Strategy Factory Phase 19 — Observability, Latency, Drift and Lifecycle Governance

Phase 19 instruments the Strategy Factory without expanding broker or model-mutation authority. It provides versioned telemetry contracts, exact lineage, bounded MQL5 rings, fixed latency histograms, feature and prediction distribution drift, execution and reconciliation drift, hysteretic alerting, immutable health snapshots, dashboard specifications, response playbooks, and operator-approved lifecycle recommendations.

## Core safety invariant

Monitoring can recommend `CONTINUE`, `OBSERVE`, `THROTTLE`, `SUSPEND`, `ROLLBACK`, `RETIRE`, or `INVESTIGATE`. Every recommendation requires operator approval and explicitly forbids automatic mutation. Phase 14 remains model-registry authority and Phase 18 remains broker and kill-switch authority.

## Main implementation

- `mql5/Include/AlphaLab/StrategyFactory/Monitoring` — typed MQL5 contracts and runtime components.
- `strategy_factory_monitoring` — Python conformance and offline reporting package.
- `schemas/v1` — telemetry, latency, drift, alert, health, lifecycle, dashboard, playbook, and report schemas.
- `examples/phase19` — golden stable/shifted distributions, telemetry sequence, policies, playbooks, and failure injection.
- `docs/strategy_factory_implementation/phase19` — 100 detailed implementation notes.

## Local verification

Run Engineering Policy, Phase 19 boundary/static checks, Python tests, then compile the MQL5 host, diagnostic, and self-test EAs with local MetaEditor. No claim of MetaEditor success is made by the generated patch.
