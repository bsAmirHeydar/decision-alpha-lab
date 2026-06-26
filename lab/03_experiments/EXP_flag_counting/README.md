# EXP_flag_counting — Unified F-counting experiment

This experiment replaces separate numbered F1/F2 modules with one integrated, reusable flag-counting module.

## Goal

Detect and visualize F-counting structures as a single grammar:

- F1: first flag structure from raw market nodes
- F2: continuation count that starts from the parent F1 internal `2`

## Core idea

F-counting is not a trade system yet. It is a structural counting experiment.

The detector outputs structured events containing:

```text
level: F1 or F2
direction: bullish or bearish
origin
leg1
waist
leg2
internal 1
internal 2
branch type
confirmation rebreak
status
```

## F2 rule

F2 starts from the parent F1 internal `2`:

```text
F2 origin = F1.N2
```

F2 can complete its branch either by normal internal `1/2` or by breaking its own waist:

```text
normal: leg2 -> 1 -> 2 -> leg2 rebreak
waist-break: 1 = F2 waist, 2 = node that breaks F2 waist
```

## Visual rule

Only the body is drawn:

```text
origin -> leg1
leg1 -> waist -> leg2
F1/F2 label
1 and 2 labels only
```

No lines are drawn after leg2.

## MQL5 entry point

```text
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

## F2 symmetry / size filter

F2 now has an explicit parent-size symmetry filter. The body size of a flag is measured as the vertical price distance from its origin/start-of-leg to its Leg2 final point:

```text
flag_size = abs(Leg2.price - Origin.price)
```

For every F2 candidate:

```text
F2_size >= Parent_F1_size * InpF2MinParentSizeRatio
```

The default ratio is `1.0`, so F2 must be at least as large as its parent F1. This keeps F2 as a real continuation count, not a small noisy nested flag. The filter is controlled by:

```text
InpRequireF2AtLeastParentSize = true
InpF2MinParentSizeRatio = 1.0
```

### Label sizing note

The visual experiment uses tiny `F1/F2` labels by default to reduce chart clutter. The count labels `1` and `2` remain more visible because they mark internal count nodes.

## Visual cleanup and tiny labels

Current chart contract:

- `F1` and `F2` level labels are tiny by default.
- Internal `1` and `2` labels are also tiny by default.
- The default `InpInternalFontSize` is `7`.
- The experiment always removes objects with `InpObjectPrefix` during `OnDeinit`, independent of `InpCleanObjectsOnInit`.
- If the prefix was changed, `OnDeinit` also removes the default `DAL_FC_` layer to avoid stale chart drawings after recompiles or updates.

## Geometry guard: waist cannot fall behind origin

A valid flag body must keep its waist/correction inside the leg range. This fixes the most common false bearish drawings.

- Bullish: `origin low < waist low < leg1 high`, and `leg2 high > leg1 high`.
- Bearish: `origin high > waist high > leg1 low`, and `leg2 low < leg1 low`.

So the waist cannot move behind the start of the leg. F2 uses the same body geometry guard after it starts from the parent flag internal 2.

## Direction draw filters

The visual expert includes `InpDrawBullish` and `InpDrawBearish` so the chart can be inspected one side at a time. This is useful because F-counting is a chain grammar, not a pile of unrelated bullish and bearish patterns.

The F1/F2 label is anchored at Leg2 only. Confirmation/rebreak remains in calculation and logging, but the renderer does not move the label to the later confirmation node.

## Direction-first color contract

By default, chart colors represent direction, not F-level/status:

- bullish flags use `InpBullishPendingColor` / `InpBullishConfirmedColor`.
- bearish flags use `InpBearishPendingColor` / `InpBearishConfirmedColor`.
- F1/F2 and status are still available from tiny labels and logs.

Set `InpColorByDirection=false` only for legacy level/status coloring. The default is `true` because bearish structures must not appear green or blue just because they are F1 pending/confirmed events.
