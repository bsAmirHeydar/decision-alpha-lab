---
title: "Gap Policy"
phase: 09
status: canonical
---
# Gap Policy

Gaps can resolve at the trigger, at a conservative observed open, or reject the candidate. The policy is explicit because gap assumptions can dominate short-horizon strategy results.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
