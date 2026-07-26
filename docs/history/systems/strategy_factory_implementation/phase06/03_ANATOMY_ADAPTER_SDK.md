---
title: "Anatomy Adapter SDK"
phase: 06
status: canonical
---
# Anatomy Adapter SDK

An anatomy adapter owns market interpretation only. It declares requirements, consumes shared services, maintains bounded state, emits observations and canonical events, and exposes telemetry. It does not generate candidates, choose risk, train models, or call broker APIs.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
