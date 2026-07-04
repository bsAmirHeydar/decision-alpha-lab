# Phase 20 — Minimal Arc-Only View with Stacked Number Labels

## Goal

Refine the minimal Hook rendering so it matches the intended reading style:

- no straight line segments between Hook nodes
- only the semi-circular cycle arc should be drawn
- node numbers should use distinct colors by number (`1`, `2`, `3`, `4`)
- if the same chart node participates in multiple sequences, its numbers should be stacked vertically in a clean column
- origin stays visually marked but unlabeled in the minimal number mode

## What changed

### Arc-only minimal view

In `FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS`:

- `draw_x_lines = false`
- `draw_cycle_arc = true`

So the minimal view no longer connects `origin -> X1 -> X2 -> X3 -> X4` with direct straight segments.

### Distinct colors by node number

Phase 02 now supports dedicated colors for numeric node labels:

- `node1_label_color`
- `node2_label_color`
- `node3_label_color`
- `node4_label_color`

And a switch:

```text
InpHookPhase02ColorNodeNumbersByIndex
```

### Clean vertical stacking on collisions

When multiple sequences place labels on the same node/time-price anchor, the labels are no longer drawn on top of one another. Instead they are stacked vertically using:

```text
InpHookPhase02StackNodeLabelsOnCollisions
InpHookPhase02NodeLabelStackStepPoints
```

This is especially useful when one node appears as `1` in one sequence, `2` in another, and `3` in a third.

## Minimal profile defaults

`FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS` now forces:

- `color_node_numbers_by_index = true`
- `stack_node_labels_on_collisions = true`
- `node_label_stack_step_points = 14`
- `color_node_labels_with_sequence = false`

This makes the node numbers semantically readable by number rather than by sequence.
