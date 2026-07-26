---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Performance and Refresh

## Purpose

Keep the complete visual suite bounded.

## Single source pipeline

P01-P07 run once inside P08. P10 reads the exported period array rather than launching a second data engine.

## Timer

The Expert is timer-driven. Object names are deterministic and existing objects are updated in place.

## Bounds

Lookback, source period limits, pair limits, chart limits, and upstream stores remain configurable.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
