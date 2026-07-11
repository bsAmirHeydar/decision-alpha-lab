---
title: "Event Identity and Clustering"
phase: 06
status: canonical
---
# Event Identity and Clustering

Event identity derives from strategy, version, symbols, direction, event/known/confirmation times, timeframe, parent, cluster, and source hash. Cluster identity groups all representations of the same market occurrence and later controls split, bootstrap, portfolio exposure, and duplicate risk.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
