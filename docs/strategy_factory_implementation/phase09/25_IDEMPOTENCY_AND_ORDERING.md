---
title: "Idempotency and Ordering"
phase: 09
status: canonical
---
# Idempotency and Ordering

Observation sequence is monotonic per candidate. Duplicate observations are ignored and counted; regressions fail closed in strict mode. This prevents duplicated ticks or replay retries from creating repeated exits.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
