---
title: "Security and No Authority"
phase: 09
status: canonical
---
# Security and No Authority

Phase 09 has no account, risk or broker authority. It cannot send, check, modify or close orders. A simulated fill is a research artifact, never proof that a broker would have filled the order.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
