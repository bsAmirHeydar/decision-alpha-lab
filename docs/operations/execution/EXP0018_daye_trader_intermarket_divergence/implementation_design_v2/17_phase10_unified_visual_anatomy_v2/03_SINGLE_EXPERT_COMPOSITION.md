---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Single-Expert Composition

## Purpose

Explain why the unified chart-facing Expert is necessary and how source work is shared.

## Constraint

MetaTrader allows one Expert Advisor on a chart. Separate P08, P09, subcycle, and anchor Experts would overwrite one another operationally and duplicate data pipelines.

## Composition

`CDayeVisualEngine` owns a single `CDayeRenderEngine`. P08 runs P01-P07 exactly once, draws confirmed divergence, and exports P03 periods read-only. P10 then projects all time layers from the same source snapshot.

## Diagnostic Experts

Standalone P08 and P09 remain useful for isolated tests, but should not be attached together with the unified Expert on the same chart.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
