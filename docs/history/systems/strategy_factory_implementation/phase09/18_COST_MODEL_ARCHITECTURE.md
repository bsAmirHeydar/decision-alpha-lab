---
title: "Cost Model Architecture"
phase: 09
status: canonical
---
# Cost Model Architecture

Cost models are exact-version plugins. The initial deterministic model supports observed or fixed spread, entry and exit slippage, commission in R and other R-denominated costs. Costs never improve outcomes and always reconcile with net R.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
