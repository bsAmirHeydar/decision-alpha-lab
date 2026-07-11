---
title: "Definition of Done"
phase: 06
status: canonical
---
# Definition of Done

Done requires Python tests passing, boundary guard passing, schemas present, golden fixture validated, MQL5 self-test and host compiling locally, ledger evidence captured, no legacy coupling, and no live authority.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
