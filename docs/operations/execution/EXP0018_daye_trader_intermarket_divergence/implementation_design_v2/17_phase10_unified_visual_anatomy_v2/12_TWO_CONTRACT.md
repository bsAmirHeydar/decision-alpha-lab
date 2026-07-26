---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# TWO Contract

## Purpose

Render Tuesday Weekly Open while keeping the source ambiguity explicit.

## Default policy

`DAYE_TWO_TUESDAY_1800_LITERAL`: use the Daily snapshot whose New York start is Tuesday 18:00 and extend to Friday 17:00.

## Alternative policy

`DAYE_TWO_MONDAY_1800_TUESDAY_TRADING_DAY`: use Monday 18:00 as the start of the trading day commonly labeled Tuesday in supplementary material.

## Governance

The policy is an input and is recorded in deterministic object identity. Changing it creates a different evidence object rather than mutating source doctrine silently.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
