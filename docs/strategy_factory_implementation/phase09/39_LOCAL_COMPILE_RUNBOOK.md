---
title: "Local Compile Runbook"
phase: 09
status: canonical
---
# Local Compile Runbook

Run Python and policy checks first, then compile SF09 self-test, diagnostic and host in MetaEditor. The phase remains pending until the local compiler and self-test EA pass.

## Invariants

- Candidate identity is immutable.
- Every decision uses information available at or before the observation known time.
- Missing or ambiguous information is never silently optimized in favor of the strategy.
- Runtime work and memory are bounded.
- Every policy, cost model and output carries exact versioned lineage.

## Acceptance evidence

Evidence consists of MQL5 self-tests, Python conformance tests, schema validation, static authority guards, deterministic replay hashes and local MetaEditor compile logs.
