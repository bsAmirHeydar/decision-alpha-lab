---
title: "Market State Generations and Dirty Propagation"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Generation purpose

Low latency requires recalculating only what changed. Phase 03 therefore assigns generations to mutable shared state.

## Bar generation

A series generation increments when a bar is inserted or materially replaced. Duplicate observations do not increment it.

## Specification generation

A symbol specification generation increments only when material broker fields change.

## Tick generation

The tick cache records source generation and source/receive timestamps. A later context engine may maintain a separate monotonically increasing tick-state generation.

# Downstream use

Phase 07 feature providers will declare dependencies such as:

```text
feature: divergence_strength
depends_on:
  - NQ/M1 bar generation
  - ES/M1 bar generation
  - session schedule version
```

When none of the dependency generations changes, the feature remains cached. When one changes, only the affected DAG branch becomes dirty.

# Reproducibility

A context snapshot should eventually include the generations used to create it. This allows a replay to prove whether the model saw the same state as live runtime.

# Constraints

Generations are local monotonic counters, not universal IDs. They must be paired with run/generation identity and source hashes when persisted across restarts.
