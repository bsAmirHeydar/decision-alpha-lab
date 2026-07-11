---
title: "Python API Reference"
phase: 08
status: canonical
---
# Python API Reference

The Python package exposes frozen candidate records, PolicyRegistry, CandidateMatrixPlan, CandidateEngine and neutral fixtures. It is designed for parity tests, dataset auditing and future statistical tooling rather than live broker operation.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
