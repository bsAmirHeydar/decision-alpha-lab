---
title: "Python Conformance Boundary"
phase: 06
status: canonical
---
# Python Conformance Boundary

Python validates observation schemas, lifecycle chains, fixture hashes, ledger uniqueness, and research ingestion. It does not redetect the anatomy for live use. MQL5 remains the source of event truth.

## Invariants

- MQL5 owns event truth.
- All time fields are causal and explicit.
- Output is deterministic for an identical ordered input stream.
- Queue, memory, and processing work are bounded.
- No previous strategy is integrated in this phase.
- No execution authority exists.

## Acceptance Evidence

Evidence is stored in the Phase 06 QA report, test suite, schema registry, fixture manifest, local compile logs, and the generated JSONL ledger.
