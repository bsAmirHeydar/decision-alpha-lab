---
title: "Bounded Enumeration"
phase: 08
status: canonical
---
# Bounded Enumeration

The matrix, registries and candidate queue have explicit capacities. Overflow behavior is configured as reject-new, drop-oldest or fail-engine. Research may use larger bounds than runtime, but no unbounded candidate generation is permitted on tick or timer paths.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
