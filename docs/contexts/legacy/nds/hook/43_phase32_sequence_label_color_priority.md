# Phase 32 — Sequence Color Priority for Hook Labels

## Goal

Ensure every label that belongs to the same Hook branch sequence uses one identical sequence color.

## Problem

The renderer already supported sequence-based label colors, but if the older `color_node_numbers_by_index` flag was still enabled in saved EA inputs, the final node-label color could be overwritten by the numeric node-index palette.

That made labels inside one sequence appear with different colors.

## Fix

The semantic Hook renderer now gives sequence color priority:

```text
if color_node_labels_with_sequence = true:
    use the branch/sequence color for every label in that branch
else:
    optionally use node-number-index colors
```

So all labels of a single sequence remain visually tied together.

## Behavior

- same branch sequence => same label color
- different branch sequences => different label colors from the sequence palette
- node-number-index coloring still exists, but only when sequence-color labeling is disabled
