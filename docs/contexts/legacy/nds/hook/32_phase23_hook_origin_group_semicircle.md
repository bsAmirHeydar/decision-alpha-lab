# Phase 23 — Hook-Origin Grouped Cycle Semicircle

## Problem

The previous implementation still drew a cycle arc **per sequence**. Even with straight X-lines disabled, this produced multiple overlapping arc traces that visually looked like node-to-node connections.

That is not the intended Hook schematic.

## Intended semantics

- Node numbering should show **all sequences**.
- But the cycle semicircle should represent the **Hook envelope**, not each inner sequence leg separately.
- Therefore the cycle arc should be drawn **once per Hook origin group**.

## Grouping rule

A Hook-origin group is defined by:

- `direction`
- `origin_time`
- `origin_price`

All selected sequences that share those fields belong to the same Hook envelope group.

## Group arc endpoint

For each origin group:

- start = Hook origin
- end = directional extreme across all X points (`X1..X4`) of all sequences in the group
  - positive Hook ⇒ lowest valley reached by the group
  - negative Hook ⇒ highest peak reached by the group

## Rendering behavior

- per-sequence cycle arcs are suppressed when grouped arc mode is enabled
- a single dim-gray semicircle is drawn for each origin group
- node markers and node numbers for all sequences are still drawn and stacked as before

## New input

```text
InpHookPhase02GroupCycleArcByOrigin
```

Default for minimal all-hooks view: `true`
