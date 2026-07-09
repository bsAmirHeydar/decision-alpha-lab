---
type: adr
product: gartal terminal
status: accepted
language: en
adr: 0004
---

# ADR-0004 — Object Prefix Discipline

## Decision

Every MT5 chart object created by gartal terminal must use an explicit `GT_` prefix namespace.

## Rationale

Indicators that delete generic objects can destroy user annotations and other indicators.

## Consequence

Each renderer owns only its own prefix.

## Enforcement

Cleanup functions delete only:

```text
GT_DASH_*
GT_LINE_*
GT_LABEL_*
GT_TL_*
GT_DIAG_*
```
