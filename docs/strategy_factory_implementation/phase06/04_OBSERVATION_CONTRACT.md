---
title: "Observation Contract"
phase: 06
status: canonical
---
# Observation Contract

An observation is a pre-event evidence object containing occurrence time, known time, reference geometry, source bar identity, source hash, and market-event cluster identity. Observations are immutable and deterministically identified.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
