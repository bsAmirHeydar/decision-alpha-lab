---
title: "Authority Model"
phase: 09
status: canonical
---
# Authority Model

MQL5 is the primary authority for observation interpretation, fill semantics, path ordering, outcome construction and cost application. Python is a conformance and research mirror. Neither language may change candidate identity during simulation.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
