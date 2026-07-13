---
title: "ADR_FP_I07_006_MISSED_CLOSE_REQUIRES_REPLAY"
status: accepted
phase: FP-I07
---
# Decision

A missed live close is not evaluated using later state; replay is required.

## Consequences

The behavior is identity-bearing, tested in Python, mirrored in MQL5, represented by closed reason codes, and may not be silently changed by later product phases.
