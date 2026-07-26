---
type: strategy-factory-document
status: canonical
title: "Paper Execution Architecture"
tags:
  - strategy-factory
---

# Paper Execution Architecture

Paper execution is a live-time rehearsal of the exact decision and lifecycle contracts, not a second historical backtest.

## Flow

Live anatomy event → immutable snapshot → candidate generation → rule/model decision → hard risk gate → paper broker → fill simulation from live quotes → position lifecycle → reconciliation → trace artifact.

## Parity

Paper and live share the same intent, risk, expiry, duplicate prevention, and monitoring code. Only the broker adapter changes. Research assumptions are compared with paper fills and costs.

## Readiness evidence

Event completeness, decision latency, model compatibility, fill rate, cost error, missed signals, duplicate rate, restart recovery, and research/paper outcome reconciliation. Paper duration is measured in unique clusters and market conditions, not only calendar days.

