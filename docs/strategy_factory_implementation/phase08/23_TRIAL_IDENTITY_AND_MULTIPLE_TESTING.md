---
title: "Trial Identity and Multiple Testing"
phase: 08
status: canonical
---
# Trial Identity and Multiple Testing

Every distinct template and parameter hash is a distinct statistical trial. Phase 08 does not yet calculate FDR or PBO, but it creates the immutable identities required for Phase 12. Renaming a template cannot erase its trial history because geometry and parameter hashes remain recorded.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
