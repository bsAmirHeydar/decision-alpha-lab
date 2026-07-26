# Phase 22 — Gray Cycle Arcs and Sequence-Colored Number Labels

## Goal

Align the minimal Hook rendering with the intended visual semantics:

- the cycle arc represents the overall Hook envelope from origin to the Hook's own directional extreme
- the cycle arc should be a dim low-contrast gray, close to black
- node numbers should show **all visible sequence memberships**
- within one sequence, all node numbers should share the **same sequence color**
- different sequences should use different number colors
- label collisions at the same node should remain stacked vertically for readability

## What changed

### Fixed gray cycle arcs

A new Phase 02 flag was added:

```text
InpHookPhase02CycleArcUseSequenceColor
```

In the minimal all-hooks profile this is forced to `false`, and the arc color is forced to a dim near-black gray:

```text
C'40,40,40'
```

So the semicircle no longer inherits the sequence palette color.

### Sequence-colored numbers

In the minimal all-hooks profile:

- `color_node_labels_with_sequence = true`
- `color_node_numbers_by_index = false`
- `use_sequence_palette_colors = true`

So every number belonging to the same sequence uses the same color, and a different sequence uses a different color.

### Collision stacking preserved

If the same chart node participates in multiple sequences, their numeric labels remain stacked vertically using the existing collision-stack logic.
