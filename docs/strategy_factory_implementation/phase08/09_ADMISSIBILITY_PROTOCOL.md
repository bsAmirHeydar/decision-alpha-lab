---
title: "Admissibility Protocol"
phase: 08
status: canonical
---
# Admissibility Protocol

Admissibility answers whether a policy is meaningful for a specific event and context. A zone-edge entry can skip events without a valid zone. A cycle-end exit can skip events without a cycle container. Missing required features produce SKIP unless the policy declares the condition a contract violation, in which case ERROR is returned.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
