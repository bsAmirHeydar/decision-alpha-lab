---
title: "Price Observation Contract"
phase: 09
status: canonical
---
# Price Observation Contract

Ticks and closed bars enter one normalized observation language. Every observation carries symbol, data fidelity, sequence, known time, interval, OHLC geometry, optional bid and ask, spread, source hash and stable identity.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
