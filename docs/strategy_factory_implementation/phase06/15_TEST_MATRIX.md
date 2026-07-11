---
title: "Test Matrix"
phase: 06
status: canonical
---
# Test Matrix

Tests cover stable observation IDs, causal time, lifecycle transitions, hash continuity, duplicate observations, duplicate events, schema presence, package discovery, no live authority, no legacy coupling, golden fixture hash, MQL5 include inventory, and local MetaEditor self-tests.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
