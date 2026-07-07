# Phase 37 — Hook Terminal and Valid-Only Label Doctrine

## Problem

Two separate concepts were previously too loose:

1. Hook terminal was effectively tied to an individual compact sequence row.
2. Valid-only rendering could hide invalid arcs while still allowing labels from unqualified Hook sequence groups to remain visible through sequence-level rendering paths.

This is not aligned with the Hook doctrine.

## Positive Hook Terminal

For a positive Hook, the terminal point is the lowest same-side valley reached by the Hook origin group.

A positive Hook does not end at an arbitrary `X2`, `X3`, or compact display slot. It ends at the lowest valley the Hook has seen before its lifecycle is resolved.

## Negative Hook Mirror

For a negative Hook, the terminal point is the highest same-side peak reached by the Hook origin group.

## Hook Group vs Sequence Row

A Hook is an origin group. A sequence row is a readable branch inside that Hook.

Therefore, Hook terminal normalization runs after sequence rows are built. Each sequence in the same Hook origin group receives the same structural terminal:

- positive Hook: lowest resolve price in the group
- negative Hook: highest resolve price in the group

This normalized terminal is the terminal used by Hook-after-Hook validity.

## Hook After Hook Validity

A Hook-2 is valid only when its origin is exactly the terminal node of Hook-1:

```text
Hook-1 normalized terminal node == Hook-2 origin node
```

## Valid-Only Labels

When valid-only Hook view is active, labels must be restricted to visible Hook groups:

- immediate Hook after opposing F3
- Hook-2 after Hook-1
- Hook-1 only as parent companion of a visible Hook-2

Labels from unrelated or unqualified Hook groups must not be drawn.

## Implementation

Rules layer:

- normalizes Hook group terminal after seed-owned sequence construction
- uses normalized terminal for Hook-after-Hook continuity

Visual layer:

- starts from valid Hook sequences
- adds parent companion for Hook-after-Hook
- expands selected valid hooks to their same-origin-group sequences
- draws labels only for selected valid groups
