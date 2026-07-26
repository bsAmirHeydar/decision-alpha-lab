---
title: "Result Sink Integration"
phase: 06
status: canonical
---
# Result Sink Integration

Events and snapshots are written through the Phase 05 versioned sink under an active immutable generation. The run manifest, generation UID, descriptor hash, market hash, plugin configuration hash, and record payload hash remain attached to evidence.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
