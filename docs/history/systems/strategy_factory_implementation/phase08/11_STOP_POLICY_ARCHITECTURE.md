---
title: "Stop Policy Architecture"
phase: 08
status: canonical
---
# Stop Policy Architecture

Stop plans represent deterministic invalidation geometry. At least one price or time invalidation mechanism is required. Initial risk distance is computed before exit construction. Directional geometry is validated centrally so every strategy uses the same definition of a legal long or short stop.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
