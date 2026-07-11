---
title: "Schema and Artifacts"
phase: 08
status: canonical
---
# Schema and Artifacts

JSON Schemas define descriptors, templates, candidate matrices, trade candidates and build reports. Result sinks will later serialize candidate envelopes using the runtime generation and run manifest from Phase 05. Schema-major mismatches fail closed.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
