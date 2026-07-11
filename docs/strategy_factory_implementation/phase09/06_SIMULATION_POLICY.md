---
title: "Simulation Policy"
phase: 09
status: canonical
---
# Simulation Policy

All ambiguous choices are frozen in a versioned policy: same-bar ordering, gap behavior, market fills, limit improvement, stop slippage, monotonic observations, staleness and path capacity. Policy hashes are persisted in every outcome.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
