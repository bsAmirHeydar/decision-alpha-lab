---
title: CTX_REFERENCE_ALPHA Context Doctrine
status: draft
version: 0.1.0
---
# CTX_REFERENCE_ALPHA Context Doctrine

## Intended market relationship
The primary symbol displaces beyond its protected reference while the comparison symbol remains inside its corresponding reference during the same registered session.

## Observable definition
At known time, primary_close is beyond primary_reference by at least one tick and comparison_close is not beyond comparison_reference on the same completed bar.

## Falsification conditions
The interpretation is falsified when both symbols close beyond their references before confirmation or the session validity window expires.

## Economic hypothesis — non-authoritative
This relationship may condition future path distributions and must be tested against random, unconditional and manual baselines.

## Non-goals
See `contracts/scope.yaml`.
