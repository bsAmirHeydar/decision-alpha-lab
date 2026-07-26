---
title: "Research Matrix vs Runtime Matrix"
phase: 08
status: canonical
---
# Research Matrix vs Runtime Matrix

Research matrices may deliberately explore many candidate templates. Runtime matrices must contain only promoted templates. The same contracts serve both, but manifests, capacities and promotion state differ. Live runtime must never enumerate a new parameter grid.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
