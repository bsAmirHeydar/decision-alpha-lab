# Phase 12.5 — Pipeline Integrity & Schema Reconciliation

## Purpose

Phase 12.5 is the mandatory integrity barrier between the completed research pipeline and Phase 13 controlled model comparison.

It verifies that Phase 07 through Phase 12 are not merely present, but internally coherent:

1. expected files exist;
2. CSV schemas match producer/consumer contracts;
3. primary identifiers are present and unique;
4. lineage survives across phase boundaries;
5. direction, side, hunter, clean, risk, and label semantics remain valid;
6. walk-forward train/embargo/test boundaries do not overlap;
7. writer summaries match materialized CSV row counts;
8. a formal readiness status is emitted.

## Canonical result

- `READY_FOR_PHASE13`
- `READY_WITH_WARNINGS`
- `BLOCKED_FOR_PHASE13`

## Components

- MQL5 preflight auditor for Terminal-side outputs.
- Python deep auditor for full row-level and cross-file reconciliation.
- PowerShell runner for repeatable local execution.
- CSV, JSON, Markdown, and HTML evidence surfaces.

## Non-negotiable boundary

This phase does not rank live signals, filter CGs, place trades, alter risk, alter targets, or mutate the strategy.
