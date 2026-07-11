---
title: "Deterministic Ordering"
phase: 08
status: canonical
---
# Deterministic Ordering

Candidate templates are ordered by integer priority and then template ID. Registry compilation and matrix compilation are deterministic. Candidate emission preserves compiled order. This guarantees stable rows, reproducible reports and exact cross-language comparisons.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
