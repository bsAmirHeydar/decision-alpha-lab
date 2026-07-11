---
title: "Outcome Identity"
phase: 09
status: canonical
---
# Outcome Identity

Outcome IDs derive from complete terminal content. Replaying the same candidate under the same policy, observations and costs must produce the same identity. Changing ambiguity or cost assumptions creates a different outcome lineage.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
