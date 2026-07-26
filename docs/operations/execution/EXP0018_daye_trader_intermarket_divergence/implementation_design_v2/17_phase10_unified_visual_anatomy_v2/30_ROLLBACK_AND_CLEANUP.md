---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# Rollback and Cleanup

## Purpose

Define safe removal.

## Rollback

Remove the P10 files and restore the previous `DAYE_RenderEngine.mqh`. P08 and P09 standalone Experts remain usable.

## Object cleanup

Delete objects whose names start with `EXP0018_P10_`. Do not bulk-delete all chart objects.

## State

P10 creates no strategy state and no trade state; rollback cannot alter lifecycle evidence.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
