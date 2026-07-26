---
title: "Policy Parameters"
phase: 08
status: canonical
---
# Policy Parameters

Policies receive a bounded generic parameter packet with eight numeric slots, eight integer slots and one short string. The packet is hashed canonically. The generic packet accelerates matrix generation while policy documentation defines semantic meaning for each slot. Parameter meaning must never change without a policy-version change.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
