---
title: "Context Immutability"
phase: 08
status: canonical
---
# Context Immutability

Candidate construction verifies that event, snapshot and context-frame identities agree, that snapshot time is not earlier than known time and that state generations match. Candidate policies receive immutable inputs and cannot write into the Phase 07 context store.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
