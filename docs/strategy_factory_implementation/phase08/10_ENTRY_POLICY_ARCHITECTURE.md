---
title: "Entry Policy Architecture"
phase: 08
status: canonical
---
# Entry Policy Architecture

Entry plans define order kind, requested price, activation time, expiration time, fill delay and slippage allowance. Entry policies do not define position size or broker filling mode. Those belong to later risk and execution phases. Every entry price must be reproducible from known-time inputs.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
