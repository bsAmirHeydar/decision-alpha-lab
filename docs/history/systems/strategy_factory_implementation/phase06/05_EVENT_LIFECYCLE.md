---
title: "Event Lifecycle"
phase: 06
status: canonical
---
# Event Lifecycle

The allowed lifecycle is UNKNOWN→OBSERVED→CONFIRMED→EMITTED→RETIRED, with explicit rejection branches. Every transition is hash-chained and sequence-numbered. Illegal transition, missing previous hash, or sequence gap fails validation.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
