---
title: "Telemetry and Health"
phase: 08
status: canonical
---
# Telemetry and Health

The engine counts requests, templates considered, disabled templates, skips, policy errors, geometry rejections, duplicates, emissions, overflows and latency. Telemetry distinguishes healthy no-candidate outcomes from engine faults. Later monitoring phases consume these counters.

## Operational rules

- All identifiers and versions are explicit.
- Inputs are immutable and causal.
- Work and memory are bounded.
- Failure is explicit and fail-closed.
- No previous strategy is integrated in this phase.
- Every future extension must preserve deterministic candidate identity.
