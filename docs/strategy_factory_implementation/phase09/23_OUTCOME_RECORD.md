---
title: "Outcome Record"
phase: 09
status: canonical
---
# Outcome Record

OutcomeRecord is immutable and terminal. It stores candidate lineage, fill and exit data, state, reason, data fidelity, ambiguity, partial use, gross and net metrics, costs, MFE, MAE, holding time, policy hashes and path hash.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
