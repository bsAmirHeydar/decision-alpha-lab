---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Lookback and Cleanup

## Purpose

Bound source processing while preserving historical evidence safely.

## Lookback

Only source periods ending inside the configured number of weeks are projected in a refresh.

## Persistence

Existing objects are preserved by default. This avoids silent loss when history is temporarily unavailable.

## Explicit removal

The only automatic full cleanup is the optional prefix-scoped deinitialization policy.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
