---
title: "Reference Anatomy Algorithm"
phase: 06
status: canonical
---
# Reference Anatomy Algorithm

The reference plugin detects a closed-bar high sweep that closes back below the previous high, or a low sweep that closes back above the previous low. It uses exactly three closed bars, shared symbol specifications, canonical bar IDs, and a one-close-time processing cursor. It is intentionally simple, deterministic, and independent of legacy doctrine.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
