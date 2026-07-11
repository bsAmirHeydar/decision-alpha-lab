---
title: "Stop Resolution"
phase: 09
status: canonical
---
# Stop Resolution

Stops are deterministic invalidation boundaries. The engine records touch, exit time, exit price and adverse path. Price stops and time invalidations are distinct mechanisms and must be testable separately.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
