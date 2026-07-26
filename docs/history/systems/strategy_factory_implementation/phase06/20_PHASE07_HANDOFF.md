---
title: "Phase 07 Handoff"
phase: 06
status: canonical
---
# Phase 07 Handoff

Phase 07 implements context state, feature provider registry, dependency DAG, dirty-generation propagation, immutable context frames, feature freshness, and fixed feature-vector compilation. The reference anatomy becomes the first event source used to test that feature system.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
