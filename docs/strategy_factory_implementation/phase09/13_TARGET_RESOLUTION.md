---
title: "Target Resolution"
phase: 09
status: canonical
---
# Target Resolution

Targets close the full position unless a partial fraction is explicitly declared. Target identity comes from the candidate and cannot be optimized after observing the path.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
