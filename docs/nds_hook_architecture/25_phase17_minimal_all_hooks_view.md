# Phase 17 — Minimal All Hooks View

## Goal

Show all Hook sequences in a minimal structural rendering:

- all Hook sequences
- sequence arc + path
- node markers
- only node numbers on chart
- node/line/arc colors derived from sequence color
- no long labels, no quality/type overlays, no thresholds

## New view profile

```text
FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS
```

This profile keeps only Phase 02 visible and disables Phase 03 through Phase 06.

## Minimal view behavior

When `MINIMAL_ALL_HOOKS` is active:

- `Phase 02` remains enabled
- `draw_origin = true`
- `draw_x_nodes = true`
- `draw_x_lines = true`
- `draw_cycle_arc = true`
- `draw_sequence_count_label = false`
- `draw_labels = true`
- `use_sequence_palette_colors = true`
- `color_origin_with_sequence = true`
- `color_node_labels_with_sequence = true`
- `minimal_numbers_only = true`
- `node_label_mode = NUMBERS_FROM_ZERO`
- `sequence_draw_mode = RECENT_N`
- `max_sequences_to_draw = 0` (draw all filtered sequences)

## New Phase 02 visual controls

```text
InpHookPhase02NodeLabelMode
InpHookPhase02UseSequencePaletteColors
InpHookPhase02ColorOriginWithSequence
InpHookPhase02ColorNodeLabelsWithSequence
InpHookPhase02MinimalNumbersOnly
```

## Recommended inputs

```text
InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_HOOK_ONLY
InpHookPhase07ViewProfile = FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS
InpHookPhase02MaxSequencesToDraw = 0
```

This produces a minimal view where each Hook sequence is color-coherent and the only text on the chart is the node number itself.
