---
title: "Phase 09 Handoff"
phase: 08
status: canonical
---
# Phase 09 Handoff

Phase 09 builds the virtual outcome engine and cost model. It consumes TradeCandidate without changing candidate identity. It must implement activation, fill, expiration, stop, target, time exit, intrabar ambiguity, MFE, MAE, path sequence and outcome records.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
