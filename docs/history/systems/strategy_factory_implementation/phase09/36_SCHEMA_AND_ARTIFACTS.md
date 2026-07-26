---
title: "Schema and Artifacts"
phase: 09
status: canonical
---
# Schema and Artifacts

JSON schemas cover observations, simulation policies, cost descriptors, outcomes and run manifests. Full datasets are later exported by the Strategy Tester research harness.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
