---
title: "Limit Entry Semantics"
phase: 09
status: canonical
---
# Limit Entry Semantics

A long limit requires the tradable path to reach or pass the requested price; a short limit uses the mirrored rule. Price improvement is disabled by default because bar-only data cannot prove queue position or true executable improvement.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
