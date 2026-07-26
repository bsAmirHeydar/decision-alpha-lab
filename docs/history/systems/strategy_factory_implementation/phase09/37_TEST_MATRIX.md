---
title: "Test Matrix"
phase: 09
status: canonical
---
# Test Matrix

Tests cover market, limit and stop entries; target, stop and time exits; no-fill expiration; ambiguity policies; partial exits; MFE and MAE; costs; duplicate and out-of-order observations; capacity and schema boundaries.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
