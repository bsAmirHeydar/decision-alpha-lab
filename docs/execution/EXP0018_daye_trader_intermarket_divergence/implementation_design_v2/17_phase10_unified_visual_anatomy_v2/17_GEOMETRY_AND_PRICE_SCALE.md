---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Geometry and Symbol-Local Price Scale

## Purpose

Define hard geometry invariants.

## Price

Every rectangle and horizontal anchor uses the chart symbol snapshot only. SPX coordinates never enter an NDX object and vice versa.

## Time

All source UTC boundaries are converted through the configured broker-time adapter before object creation.

## Fail closed

Nonpositive prices, inverted ranges, invalid windows, and unresolved local times are not drawn.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
