---
title: "Test Matrix"
phase: 08
status: canonical
---
# Test Matrix

Tests cover duplicate registration, exact version resolution, registry immutability, deterministic hashes, matrix ordering, unresolved policies, admissibility skip/error, long and short geometry, zero risk, context mismatch, capacity overflow, duplicate IDs, missing features and absence of order authority.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
