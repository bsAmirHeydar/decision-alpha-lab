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

---

## Astro stack

The astro research branch follows the same layered rule:

1. Python generates the canonical raw astro map.
2. MQL5 loads the raw map through shared CSV readers.
3. Shared doctrine modules derive classical/traditional structure such as sect, dignity, triplicity, decan, solar condition, reception, rulership chain, nodal pressure, and eclipse state.
4. Timing/doctrine/signal modules convert that raw sky state into macro, meso, micro, and minute astro execution language.
5. Dashboard and execution Experts consume the same shared doctrine objects so UI and execution remain aligned.

The intent is that no astro signal should come from ad hoc UI logic or isolated script math. Raw map, doctrine layer, timing layer, and signal layer must stay traceable end to end.

### Astro ML hardening

The astro machine-learning layer is research-first and skeptical by design:

1. Dataset audit is a gate for professional runs, not only a report.
2. Feature selection excludes future/outcome/label columns before training.
3. Evaluation must compare against a majority/time baseline.
4. Walk-forward uses a real embargo gap between train and test windows.
5. Model reports include worst-fold edge, negative-edge fold count, and probability-quality diagnostics.
6. Antifragile memory promotes only hardened principles; temporal survival alone is insufficient if contradiction or condition creep is detected.

No learned astro rule should become an execution filter until it has passed chronological OOS, walk-forward stability, and the final fragility audit.
