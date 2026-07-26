---
title: "Performance Budget"
phase: 06
status: canonical
---
# Performance Budget

The plugin runs on timer/new-bar scope, reads only three cached closed bars after startup, performs constant-time geometry checks, emits at most one event per closed bar, and never performs file I/O or model inference in the detection path.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
