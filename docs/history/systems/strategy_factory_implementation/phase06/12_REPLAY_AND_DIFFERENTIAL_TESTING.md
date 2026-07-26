---
title: "Replay and Differential Testing"
phase: 06
status: canonical
---
# Replay and Differential Testing

Replay feeds the same ordered closed bars into the same plugin and compares the resulting event ledger. Differential testing later compares a migrated legacy adapter against this canonical event language without allowing the legacy system to redefine contracts.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
