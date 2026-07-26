---
title: "Data Fidelity Ladder"
phase: 09
status: canonical
---
# Data Fidelity Ladder

Bar approximation, synthetic ticks and real ticks are explicit fidelity levels. Screening may use lower fidelity, but any candidate dependent on intrabar ordering must be promoted through higher-fidelity validation before paper or live stages.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
