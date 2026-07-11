---
title: "Outcome Domain Model"
phase: 09
status: canonical
---
# Outcome Domain Model

The domain is decomposed into PriceObservation, SimulationPolicy, CostModel, CandidateRuntime, PathEvent, OutcomeRecord and OutcomeQueue. Separating these records prevents the simulator from becoming an opaque backtest function.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
