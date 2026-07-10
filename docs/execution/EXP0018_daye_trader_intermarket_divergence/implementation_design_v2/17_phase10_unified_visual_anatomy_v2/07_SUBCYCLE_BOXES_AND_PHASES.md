---
project: EXP0018
phase: P10
status: implemented-evidence-package
authority: visual-projection-only
execution_authority: false
schema_version: 2
---

# 90-Minute Subcycle Boxes and Phase Labels

## Purpose

Make every a1-p4 period directly visible.

## Registry

a1-a4, l1-l4, n1-n4, p1-p4 are read from P03 snapshots. Each receives a symbol-local range box, start boundary, and phase label.

## Label semantics

The numeric suffix maps to Q1-Q4 inside the parent Session. The letter preserves the Session context.

## Boundary precedence

Session boundaries are major; subcycle boundaries are dashed and lighter. Coincident lines are deterministic objects rather than inferred pixels.


## Non-authority statement

This document and the corresponding implementation do not authorize entries, exits, risk sizing, order placement, strategy mutation, model promotion, network access, or execution. Chart objects are projections of upstream immutable evidence and time contracts.
