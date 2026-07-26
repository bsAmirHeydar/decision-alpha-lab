---
title: "MQL5 API Reference"
phase: 06
status: canonical
---
# MQL5 API Reference

Key modules are SF06_AnatomyObservation, SF06_EventLifecycle, SF06_EventBuilder, SF06_GoldenLedger, CSF06ReferenceSweepPlugin, CSF06ReferenceSweepFactory, SF06_StrategyHost, and SF06_ReferenceAnatomySelfTest.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
