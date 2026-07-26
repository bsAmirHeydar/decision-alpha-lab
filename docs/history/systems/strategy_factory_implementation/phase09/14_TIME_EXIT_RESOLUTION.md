---
title: "Time Exit Resolution"
phase: 09
status: canonical
---
# Time Exit Resolution

Maximum holding and time invalidation are causal terminal mechanisms. Time exits use the first eligible observation after the horizon and record timing overshoot for later fidelity analysis.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
