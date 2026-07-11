---
title: "Central Engine Only Policy"
phase: 06
status: canonical
---
# Central Engine Only Policy

The reference anatomy is a conformance instrument, not a trading strategy. Its purpose is to expose missing abstractions in the shared engine before legacy integration. No legacy include, strategy constant, feature name, or execution rule may enter this phase.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
