---
title: "Path Tracking"
phase: 09
status: canonical
---
# Path Tracking

A bounded append-only path tracker records registration, fill, new favorable and adverse extremes, stop and target touches, partial exits, time exits, ambiguity and closure. The chain hash supports replay integrity.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
