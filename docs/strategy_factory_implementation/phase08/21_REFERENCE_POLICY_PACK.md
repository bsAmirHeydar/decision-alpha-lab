---
title: "Reference Policy Pack"
phase: 08
status: canonical
---
# Reference Policy Pack

The neutral fixture pack implements confirmation-market and reference-limit entries, anatomy and buffered invalidation stops, and fixed-R and time-only exits. It proves extensibility without importing any legacy strategy. These policies are examples, not promoted trading logic.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
