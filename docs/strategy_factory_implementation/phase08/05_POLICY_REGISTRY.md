---
title: "Policy Registry"
phase: 08
status: canonical
---
# Policy Registry

The static registry rejects duplicate identity pairs, kind mismatches, invalid descriptors and post-compilation mutation. Exact policy ID and version resolution is mandatory. There is no latest-version lookup in the runtime path. The registry hash becomes part of every compiled matrix lineage.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
