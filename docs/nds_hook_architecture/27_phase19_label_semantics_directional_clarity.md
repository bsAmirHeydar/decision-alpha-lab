# Phase 19 — Label Semantics and Directional Clarity

## Goal

Align the minimal Hook view with the intended Hook reading semantics:

- Sequence counting should be `1, 2, 3, 4` as the meaningful internal Hook sequence.
- The chart should not start numbering from `0` in minimal mode.
- The origin remains the structural start anchor, but it is left unlabeled in the minimal numeric view.
- Positive Hook reading is based on **valleys**.
- Negative Hook reading is based on **peaks**.

## What changed

### Node label mode

A new label mode was added:

```text
FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN
```

Behavior:

- origin: no numeric label
- X1: `1`
- X2: `2`
- X3: `3`
- X4: `4`

This mode is now the default for the minimal all-hooks view and the default Phase 02 node-label input.

### Directional semantics

The Phase 02 sequence builder already uses directional node typing as follows:

- `POSITIVE` Hook sequences use `VALLEY` nodes
- `NEGATIVE` Hook sequences use `PEAK` nodes

This patch documents that expectation explicitly so the minimal rendering semantics match the intended Hook anatomy.
