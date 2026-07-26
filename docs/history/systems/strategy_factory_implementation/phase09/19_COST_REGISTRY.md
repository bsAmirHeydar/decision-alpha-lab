---
title: "Cost Registry"
phase: 09
status: canonical
---
# Cost Registry

The static registry rejects duplicates and post-compilation mutation. Every run records the exact cost model ID, version, descriptor hash and registry hash.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
