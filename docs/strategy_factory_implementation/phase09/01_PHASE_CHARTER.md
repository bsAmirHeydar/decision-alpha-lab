---
title: "Phase Charter"
phase: 09
status: canonical
---
# Phase Charter

The phase owns hypothetical trade lifecycle semantics. It consumes Phase 08 candidates unchanged and emits canonical OutcomeRecord artifacts. It does not own statistics, model training, risk sizing, paper trading, live trading or broker requests.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
