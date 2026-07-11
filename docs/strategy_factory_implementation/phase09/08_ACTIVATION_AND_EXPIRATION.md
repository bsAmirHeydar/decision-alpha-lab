---
title: "Activation and Expiration"
phase: 09
status: canonical
---
# Activation and Expiration

A candidate cannot fill before activation and cannot remain pending after expiration. Expiration before fill produces a valid no-fill outcome with zero R and no fabricated transaction cost.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
