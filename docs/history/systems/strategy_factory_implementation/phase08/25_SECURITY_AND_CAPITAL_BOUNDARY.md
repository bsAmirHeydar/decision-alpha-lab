---
title: "Security and Capital Boundary"
phase: 08
status: canonical
---
# Security and Capital Boundary

Phase 08 has no account access, sizing authority, broker request construction or order lifecycle. TradeCandidate is hypothetical geometry only. The presence of a valid candidate is not permission to trade. Risk and execution remain separated by later hard gates.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
