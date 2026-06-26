# Flag Counting MQL5 Implementation

## Why this exists

The old split between `M0007` and `M0008` made F-counting harder to maintain. The new design treats F-counting as one experiment and one module family:

```text
mql5/Include/FlagCounting/*
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

## Include strategy

The expert uses relative quoted includes, not terminal-level angle includes. This avoids this error:

```text
file MQL5/Include/M0008/... not found
```

## Module layers

```text
DAL_FlagCountingTypes.mqh        shared event/node types
DAL_FlagCountingNodeDetector.mqh swing node detector and alternating compression
DAL_FlagCountingDetector.mqh     F1/F2 structural logic
DAL_FlagCountingRenderer.mqh     chart drawing only
```

## Reusability

Future execution or statistics modules should depend on `DAL_FlagCountingDetector.mqh` and ignore the renderer.

The event object is intentionally generic:

```text
level
parent_event_index
direction
status
branch_type
origin
leg1
waist
leg2
n1
n2
confirm
```

This allows the same detector output to be used for:

- chart visualization
- CSV export
- volatility around F nodes
- directional-memory tests
- continuation/reversal tests
- trade simulation
- multi-timeframe counting

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

## Renderer label size contract

The unified renderer keeps `F1/F2` text small by default (`InpFlagFontSize = 7`) and places it close to the body endpoint so the curved flag body is not visually blocked. Internal `1/2` labels are not reduced by this change.

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

## Sequencing repair: F1 versus F2

The detector now separates root F1 counting from child F2 counting more strictly.

- F1 internal `1` and `2` must appear before the F1 Leg2 extreme is rebroken. If the Leg2 extreme is rebroken before the branch `1/2` is formed, that candidate is not accepted as F1.
- F2 is different: after F2 Leg2, price is allowed to extend through/rebreak the F2 Leg2 extreme first and only then come back to form `2`, either through the normal internal branch or through the F2 waist-break branch.
- When a body is promoted into F2 from a parent F1 internal `2`, the same body is suppressed from the root F1 display by default. This prevents one structure from being shown simultaneously as both F1 and F2.

Default input:

```text
InpSuppressF1BodiesPromotedToF2 = true
```
