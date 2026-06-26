# DAL Flag Counting Module

This module makes flag counting a single reusable experiment instead of splitting F1 and F2 across separate numbered modules.

## Files

```text
mql5/Include/FlagCounting/DAL_FlagCountingTypes.mqh
mql5/Include/FlagCounting/DAL_FlagCountingNodeDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingRenderer.mqh
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

The expert uses local relative includes:

```cpp
#include "../../Include/FlagCounting/DAL_FlagCountingDetector.mqh"
#include "../../Include/FlagCounting/DAL_FlagCountingRenderer.mqh"
```

So it does not require copying files into the terminal-level `MQL5/Include` folder.

## F1 logic

Bullish F1:

```text
origin low -> leg1 high -> waist low -> leg2 high breaking leg1
```

Bearish F1:

```text
origin high -> leg1 low -> waist high -> leg2 low breaking leg1
```

After leg2, the detector searches for internal `1` and `2`:

- bullish: low `1`, then lower low `2`, both above the F1 waist
- bearish: high `1`, then higher high `2`, both below the F1 waist

Then final confirmation is a rebreak of leg2 after `1/2`.

## F2 logic

F2 is a count that starts from the parent F1 internal `2`:

```text
F2 origin = parent F1 internal 2
```

The F2 direction is inherited from the parent F1.

Bullish F2:

```text
parent F1 internal 2 low -> F2 leg1 high -> F2 waist low -> F2 leg2 high breaking F2 leg1
```

Bearish F2:

```text
parent F1 internal 2 high -> F2 leg1 low -> F2 waist high -> F2 leg2 low breaking F2 leg1
```

## F2 branches

F2 can complete its `1/2` branch in two ways.

### Branch 1: normal internal 1/2

Same as F1:

```text
leg2 -> internal 1 -> internal 2 -> leg2 rebreak
```

### Branch 2: waist-break branch

F2 is allowed to break its own waist:

```text
1 = F2 waist
2 = the new node that breaks the F2 waist
```

Then confirmation still requires a later rebreak of F2 leg2 when `InpRequireF2Leg2RebreakForConfirm = true`.

## Renderer contract

The renderer is intentionally body-only:

```text
origin -> leg1 = straight line
leg1 -> waist -> leg2 = smooth curve
F1/F2 label
1 and 2 = numeric labels only
```

It does not draw any line from leg2 to `1`, `2`, or the final rebreak. Those points remain in the calculation and printed audit output.

## Main expert inputs

```text
InpScanF1
InpScanF2
InpRequireF1Internal12
InpRequireF1Leg2RebreakForConfirm
InpRequireParentF1ConfirmedForF2
InpAllowF2WaistBreakBranch
InpRequireF2Branch12
InpRequireF2Leg2RebreakForConfirm
InpDrawF1
InpDrawF2
InpDrawOnlyConfirmed
```

## Reuse pattern

Any future experiment can include the detector without the renderer:

```cpp
#include "../../Include/FlagCounting/DAL_FlagCountingDetector.mqh"
```

Then call:

```cpp
FC_Node nodes[];
FC_FlagEvent events[];
int n = FC_DetectFlags(rates, total, L, true, true, true, true, true, true, true, true, true, true, eps, nodes, events);
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

## Visual label sizing

`F1` and `F2` level labels are intentionally small by default so the body geometry remains readable on dense charts.

Default:

```text
InpFlagFontSize = 7
InpInternalFontSize = 12
```

The renderer also keeps the `F1/F2` label close to the Leg2/confirmation anchor. Internal `1` and `2` labels remain larger because they are structural count markers.

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

## Confirmation and invalidation contract

The detector now uses the simplified core contract:

- A flag is confirmed when price rebreaks the Leg2 extreme after the body exists.
- The rebreak is valid only if the flag has not invalidated first.
- F1 invalidation boundary is the F1 waist.
- F2 invalidation boundary is the F2 origin/start of leg.
- Internal `1` and `2` are counting/audit labels. They are not allowed to delete an otherwise valid body and they are not the confirmation gate.
- For F1, internal labels are searched before the confirming Leg2 rebreak.
- For F2, internal/waist-break labels may appear even after an early Leg2 extension, until the F2 origin invalidates.
