---
title: "Failure Semantics"
phase: 08
status: canonical
---
# Failure Semantics

Policy SKIP means no candidate for that template. Invalid geometry is a deterministic rejection. Missing policy, policy ERROR, registry corruption, queue overflow under fail-engine and context mismatch are hard failures. The engine never substitutes a fallback price or silently changes a stop.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
