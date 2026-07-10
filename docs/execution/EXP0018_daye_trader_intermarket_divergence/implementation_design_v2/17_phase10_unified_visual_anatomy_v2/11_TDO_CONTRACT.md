---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# TDO Contract

## Purpose

Render Trading Day Open as a finite symbol-local anchor.

## Anchor

TDO is the Open of Session L at 00:00 New York.

## Extent

The line begins at 00:00 and ends at 17:00 of the same civil date.

## Evidence

Price is taken from the P03 L snapshot for the chart symbol; no other symbol scale is used.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
