---
title: "ADR_FP_I07_001_RESOLVE_HOST_TIMEFRAME_ONCE"
status: accepted
phase: FP-I07
---
# Decision

Resolve host timeframe exactly once at initialization; `PERIOD_CURRENT` cannot remain dynamic.

## Consequences

The behavior is identity-bearing, tested in Python, mirrored in MQL5, represented by closed reason codes, and may not be silently changed by later product phases.
