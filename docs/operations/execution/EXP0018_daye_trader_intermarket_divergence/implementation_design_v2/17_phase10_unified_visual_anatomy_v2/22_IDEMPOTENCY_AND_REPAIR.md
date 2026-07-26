---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Idempotency and Repair

## Purpose

Ensure repeated timers and restarts do not duplicate objects.

## Upsert

Each pass creates missing deterministic objects or updates existing geometry and style.

## Repair

A manually moved P10 object is restored from source truth on the next refresh.

## Separation

P10 repair cannot touch P08 or foreign objects.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
