---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Multi-Chart Targeting

## Purpose

Render the same time architecture on all relevant open symbol charts.

## Default

All open charts whose exact broker symbol matches Symbol A or Symbol B.

## Alternatives

Current chart only or first matching open chart.

## Missing charts

Automatic chart opening is off by default. No target chart is a waiting state, not a successful projection.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
