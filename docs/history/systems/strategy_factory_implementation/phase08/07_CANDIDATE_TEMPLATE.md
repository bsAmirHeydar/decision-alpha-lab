---
title: "Candidate Template"
phase: 08
status: canonical
---
# Candidate Template

A template binds one exact entry policy, one exact stop policy and one exact exit policy with immutable parameter packets. It has its own version, priority, enabled flag, admissibility tag and hash. Templates are experiment units and must be registered in the trial registry once research begins.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
