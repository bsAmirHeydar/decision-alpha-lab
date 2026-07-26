---
title: "Policy Plugin Contracts"
phase: 08
status: canonical
---
# Policy Plugin Contracts

Entry, stop and exit policies implement separate typed interfaces. Each exposes an exact descriptor, an admissibility decision and a build operation. ADMIT, SKIP and ERROR are intentionally distinct. SKIP is a valid absence of a candidate; ERROR is a broken contract and fails the engine closed.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
