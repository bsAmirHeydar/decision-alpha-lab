---
title: "Performance Architecture"
phase: 09
status: canonical
---
# Performance Architecture

The engine performs no file parsing, training, dynamic discovery or unbounded allocation in the observation path. Candidate state is preallocated and terminal outcomes are pushed to a bounded queue.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
