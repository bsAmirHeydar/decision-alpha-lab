---
type: strategy-factory-document
status: canonical
title: "Candidate Compatibility and Pruning"
tags:
  - strategy-factory
---

# Candidate Compatibility and Pruning

Candidate pruning must control combinatorics without using outcomes.

## Compatibility table

Some entries require specific stops or targets; a time-only exit may not pair with an unlimited holding policy; a zone-limit entry may expire before a cycle-end target. These constraints are declared as compatibility rules and tested.

## Pruning principles

Prefer a small orthogonal set: immediate versus pullback entry, structural versus volatility-buffered stop, fixed versus structural/time exit. Numeric grids are admitted only after a coarse family shows value and then must use nested training-only selection.

## Audit

The report lists theoretical combinations, excluded combinations, reason codes, and emitted candidates. Silent truncation is forbidden. If `max_candidates_per_event` is reached, the deterministic ordering and pruning policy are materialized.

