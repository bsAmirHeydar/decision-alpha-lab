---
title: "Market Entry Semantics"
phase: 09
status: canonical
---
# Market Entry Semantics

Market candidates can fill at the first causal observation, at the requested reference price for controlled experiments, or at a conservative side-aware price. The selected rule is part of SimulationPolicy.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
