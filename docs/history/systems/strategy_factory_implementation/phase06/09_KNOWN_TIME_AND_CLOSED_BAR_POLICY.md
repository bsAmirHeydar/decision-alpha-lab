---
title: "Known Time and Closed-Bar Policy"
phase: 06
status: canonical
---
# Known Time and Closed-Bar Policy

The reference plugin emits only after a bar is closed. Event time, known time, and confirmation time are equal to the canonical close timestamp. No forming-bar high or low may affect the event. This establishes the baseline causal contract for future adapters.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
