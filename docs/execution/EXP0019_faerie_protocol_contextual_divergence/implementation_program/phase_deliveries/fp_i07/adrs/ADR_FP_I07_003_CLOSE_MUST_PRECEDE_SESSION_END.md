---
title: "ADR_FP_I07_003_CLOSE_MUST_PRECEDE_SESSION_END"
status: accepted
phase: FP-I07
---
# Decision

A close at or after session end expires the candidate.

## Consequences

The behavior is identity-bearing, tested in Python, mirrored in MQL5, represented by closed reason codes, and may not be silently changed by later product phases.
