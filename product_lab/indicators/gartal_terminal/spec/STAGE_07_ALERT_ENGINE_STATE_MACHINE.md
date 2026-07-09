# STAGE 07 — Alert Engine + State Machine Specification

## Objective

Implement a deterministic, duplicate-safe alert engine for the gartal terminal MT5 news indicator.

## Scope

- Pre-event alerts: 60m, 30m, 15m, 5m, 1m
- Release alerts
- Actual-value alerts
- Breaking-event alerts
- Runtime alert pause/resume from dashboard
- Alert delivery channels
- Alert diagnostics
- Obsidian documentation and validation script

## Out of scope

- Persistent alert ledger across terminal restarts
- Forex Factory live parser
- Actual-value refresh polling after release
- Per-user license gating

## Core contract

```text
GT_ProcessAlerts(config, store, filters, state, runtime)
```

The function scans visible/eligible events and attempts stage-specific alerts.

## Duplicate prevention

A unique key is generated from:

```text
event.id + "_" + stage
```

Sent keys are stored in `GT_AlertState.sent_keys`.

## Dashboard integration

A new `ALERTS ON/OFF` dashboard button toggles `filters.alerts_enabled`.

## Commercial requirement

The engine must avoid noisy behavior. It must never blast every missed threshold at once when attached near event time.
