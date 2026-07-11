---
title: "Definition of Done"
phase: 09
status: canonical
---
# Definition of Done

The phase is complete when identical inputs produce identical outcomes, costs reconcile, all lifecycle edge cases are explicit, no authority exists, Python mirrors pass, MetaEditor compiles and the self-test EA succeeds.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
