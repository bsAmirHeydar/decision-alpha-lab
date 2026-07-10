---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Runtime Validation Guide

## Purpose

Provide the field procedure for validating all visual layers.

## Setup

Open SPXUSD and NDXUSD charts, compile the unified Expert, attach it to one chart, set broker offset correctly, and enable two weeks of lookback.

## Checks

Inspect Object List, exact 18/00/06/12/17 boundaries, a1-p4, p4 length, micro boundaries, gap, TDO/TWO, divergence lines, symbol-local ranges, restart behavior, and DST dates.

## Failure triage

Use Experts/Journal and tooltips. Distinguish no source period, no chart, invalid geometry, and object API failure.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
