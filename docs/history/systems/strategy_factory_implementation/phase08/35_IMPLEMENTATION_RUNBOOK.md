---
title: "Implementation Runbook"
phase: 08
status: canonical
---
# Implementation Runbook

Compile Phase 01 through Phase 08 headers, run SF08_CandidateEngineSelfTest, run the Python phase tests, execute the repository engineering policy, verify no order-authority token exists in Phase 08 sources and record registry and matrix hashes in the run evidence.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
