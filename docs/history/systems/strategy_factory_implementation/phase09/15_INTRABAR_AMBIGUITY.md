---
title: "Intrabar Ambiguity"
phase: 09
status: canonical
---
# Intrabar Ambiguity

When a bar touches stop and target, ordering is unknowable. The platform supports stop-first, target-first, excluded and lower-fidelity-required policies. Conservative production research defaults to stop-first or excluded.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
