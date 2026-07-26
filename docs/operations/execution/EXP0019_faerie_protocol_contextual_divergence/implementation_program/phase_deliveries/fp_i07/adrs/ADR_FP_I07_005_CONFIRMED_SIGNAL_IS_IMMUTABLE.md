---
title: "ADR_FP_I07_005_CONFIRMED_SIGNAL_IS_IMMUTABLE"
status: accepted
phase: FP-I07
---
# Decision

Later revisions preserve confirmed evidence and only affect future rebuilds.

## Consequences

The behavior is identity-bearing, tested in Python, mirrored in MQL5, represented by closed reason codes, and may not be silently changed by later product phases.
