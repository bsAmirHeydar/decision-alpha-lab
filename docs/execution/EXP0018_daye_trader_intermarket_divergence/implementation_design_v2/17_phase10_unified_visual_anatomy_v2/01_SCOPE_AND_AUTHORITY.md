---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Scope and Authority

## Purpose

Define exactly what P10 may draw and what it may never decide.

## In scope

Immutable P08 divergence lines, Daily frames, A/L/N/P ranges, a1-p4 ranges, 22.5-minute micro-quarter boundaries, Daye gap, TDO, TWO, optional extended Session True Opens, optional provisional week boundaries, labels, legend, repair, multi-chart targeting, and prefix-scoped cleanup.

## Out of scope

DFR projections, AMDX/XAMD classification, news overlays, seasonal bias, inferred trade direction, entries, stops, targets, risk, positions, orders, and any change to P00-P07 state.

## Authority boundary

P10 consumes P03 symbol-local snapshots and P07 accepted-use evidence through a read-only P08 export. It cannot synthesize a signal or convert a visual observation into strategy truth.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
