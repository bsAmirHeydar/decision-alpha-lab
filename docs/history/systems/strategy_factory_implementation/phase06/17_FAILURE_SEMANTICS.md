---
title: "Failure Semantics"
phase: 06
status: canonical
---
# Failure Semantics

Insufficient bars waits without emitting. Invalid symbol specification, invalid bar geometry, contract failure, queue overflow, generation mismatch, or sink write failure is explicit. Strict mode fails closed; audit mode records the rejection.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
