---
title: "Security and Capital Boundary"
phase: 06
status: canonical
---
# Security and Capital Boundary

Phase 06 has no order construction or order submission capability. The only execution boundary is no-send. Anatomy output is evidence, not authorization to trade.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
