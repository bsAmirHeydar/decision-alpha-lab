---
title: "Candidate Lifecycle"
phase: 09
status: canonical
---
# Candidate Lifecycle

The lifecycle is Registered → Waiting Activation → Pending Fill → Filled or Partial → Terminal. Expired, Invalidated, Ambiguous and Rejected are explicit terminal states. No lifecycle transition may be inferred only from final PnL.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
