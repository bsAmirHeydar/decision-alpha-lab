---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Label Placement

## Purpose

Keep labels readable without making them source truth.

## Placement

Period labels use the midpoint in time and symbol High plus a configurable point offset. Micro labels use local quarter midpoints and the lower side of the source range.

## Density

Daily, Session, and Subcycle labels default on. Micro labels default off.

## Non-authority

Moving or hiding a label cannot change any domain state.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
