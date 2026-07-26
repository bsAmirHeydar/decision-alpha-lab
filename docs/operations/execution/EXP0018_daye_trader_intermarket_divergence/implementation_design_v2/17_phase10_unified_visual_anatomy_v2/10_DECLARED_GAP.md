---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Declared 17:00-18:00 Gap

## Purpose

Make the non-session interval visible without treating it as missing history.

## Geometry

The gap uses a full-chart-height gray band and dotted start/end lines.

## Meaning

Gap means valid domain time outside A/L/N/P. It is not no-data, no-hunt, or a synthetic fifth Session.

## Chart scaling

The band adapts to current chart price bounds and therefore is a visual overlay, not a price-range fact.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
