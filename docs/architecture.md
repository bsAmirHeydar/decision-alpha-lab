# System Architecture

Decision Alpha Lab uses a layered architecture for structural market research and execution.

---

## Research philosophy

The project does not assume that fixed time windows are the natural unit of market analysis. The core unit is a structural event: node, zone, revisit, hunt, break, known-time regime, and execution opportunity.

---

## Python layer

Python remains useful for:

- data engineering,
- large-scale offline analysis,
- feature extraction,
- visualization,
- exploratory statistics,
- parameter sweeps,
- external data pipelines.

Python is allowed to discover ideas. It must not be the only source of live-valid execution claims unless its replay is strictly causal.

---

## MQL5 layer

MQL5 is responsible for:

- MetaTrader-native replay,
- Expert Advisor execution,
- broker-facing order management,
- live-style state reconstruction,
- stop/target/trailing modeling,
- execution logs,
- validation close to the final trading environment.

MQL5 can now contain research validators when the question is platform/live-timing sensitive.

---

## Core modules

### M0001 — Structural node and event lifecycle

Responsible for structural highs/lows, zones, revisits, hunts, breaks, and raw events.

### M0002 — Branch sample pairing

Useful for exploratory reports. Not valid as the official live regime source for H4/H5 unless wrapped in causal known-time batching.

### M0004 — Regime memory

Official direction: atomic no-sample known-time batches from raw M0001 events.

### M0005 — Directional memory

Official direction: atomic no-sample replay with explicit family-level risk models.

---

## Validation hierarchy

1. Exploratory sample reports.
2. Causal sample-batch reports.
3. Atomic no-sample replay.
4. Execution EA reports with real risk and costs.

A result should not be promoted to strategy status before level 3 or 4.

---

## Design principle

Research logic may begin in Python or debug MQL5, but accepted live-valid contracts must be implemented in shared modules and used by the main Experts.
