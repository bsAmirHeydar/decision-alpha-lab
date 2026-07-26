---
title: "Bounded Memory"
phase: 09
status: canonical
---
# Bounded Memory

Active candidates, path events, cost models and terminal outcome queues have fixed capacities. Overflow is visible and configured as reject, drop-oldest or fail-engine. Production defaults to fail closed.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
