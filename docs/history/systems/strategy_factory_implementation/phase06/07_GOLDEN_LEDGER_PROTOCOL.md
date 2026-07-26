---
title: "Golden Ledger Protocol"
phase: 06
status: canonical
---
# Golden Ledger Protocol

Each golden case freezes input bars, input hash, expected observation IDs, expected event IDs, lifecycle sequence, and record count. A code change is accepted only when either the ledger remains byte-equivalent or a reviewed versioned doctrine change updates the manifest.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
