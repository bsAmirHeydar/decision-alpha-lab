---
title: "Bar-to-Tick Promotion"
phase: 09
status: canonical
---
# Bar-to-Tick Promotion

Broad matrices can be screened with closed bars. Survivors are rerun with synthetic or real ticks. Outcome divergence is measured and candidates with unstable ordering are not promoted.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
