---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# 22.5-Minute Micro Quarters

## Purpose

Define the smallest Core visual subdivision supplied by the sources.

## Construction

Every full 90-minute subcycle is divided in New York local time at +1,350, +2,700, and +4,050 seconds. These produce four 22.5-minute quarters.

## DST safety

Each local boundary is independently resolved to UTC using the P01 ambiguity policy. A nonexistent local boundary is skipped with degraded evidence rather than shifted silently.

## Labels

q1-q4 labels are implemented but disabled by default to avoid excessive visual density.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
