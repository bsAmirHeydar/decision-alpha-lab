---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Daily Frame and Boundaries

## Purpose

Specify the 18:00 New York to 17:00 next-day Daily visual.

## Geometry

The rectangle uses the P03 symbol-local Daily High and Low and the exact P01 UTC window converted to broker chart time.

## Boundaries

Start and end are explicit vertical lines. The end is exclusive at 17:00. The 17:00-18:00 gap is a separate domain layer.

## Open period

An open Daily frame updates from closed source bars. A completed frame is verified and repaired from source truth.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
