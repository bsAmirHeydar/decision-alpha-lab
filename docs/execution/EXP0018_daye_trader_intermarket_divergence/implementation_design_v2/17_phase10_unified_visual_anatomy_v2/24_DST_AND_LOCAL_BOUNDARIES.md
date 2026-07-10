---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# DST and Local Boundaries

## Purpose

Preserve New York wall-time meaning through daylight-saving transitions.

## P01 authority

P10 never hard-codes server hours. P01 resolves New York local windows to UTC.

## Micro boundaries

22.5-minute boundaries are resolved separately because a local time can be ambiguous or nonexistent.

## Identity

Source period identity remains UTC-based even when elapsed UTC duration changes.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
