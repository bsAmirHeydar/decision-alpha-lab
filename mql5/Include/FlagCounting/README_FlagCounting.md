# DAL Flag Counting Module

This module makes flag counting one reusable experiment and one counting grammar instead of separate numbered modules.

## Files

```text
mql5/Include/FlagCounting/DAL_FlagCountingTypes.mqh
mql5/Include/FlagCounting/DAL_FlagCountingNodeDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingRenderer.mqh
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

The expert uses local relative includes, so it does not require copying files into the terminal-level `MQL5/Include` folder.

## Counting grammar

The detector now treats flags as a chained count:

```text
F1 -> F2 -> F3
```

A root `F1` is detected from market nodes. A continuation `F2` starts from the parent F1 internal `2`. A continuation `F3` starts from the parent F2 internal `2`.

The same body should not be shown as root F1 and child F2 at the same time. When a body is promoted to a higher F-level, the lower-level duplicate is suppressed by default.

## F1 logic

Bullish F1:

```text
origin low -> leg1 high -> waist low -> leg2 high breaking leg1
```

Bearish F1:

```text
origin high -> leg1 low -> waist high -> leg2 low breaking leg1
```

F1 confirmation/invalidation:

```text
confirmed = rebreak Leg2 before invalidation
invalidated = break F1 waist before rebreak
```

## F2 logic

F2 is a continuation count from the parent F1:

```text
F2 origin = parent F1 internal 2
```

F2 direction is inherited from the parent F1. F2 body shape is the same as F1 body shape, but its invalidation is different:

```text
confirmed = rebreak F2 Leg2 before invalidation
invalidated = break F2 origin/start-of-leg before rebreak
```

F2 can break its own waist without invalidating. In that case the waist-break branch is allowed:

```text
1 = F2 waist
2 = node that breaks F2 waist
```

## F3 logic

F3 is the next continuation count:

```text
F3 origin = parent F2 internal 2
```

F3 uses the continuation-level contract, like F2:

```text
confirmed = rebreak F3 Leg2 before invalidation
invalidated = break F3 origin/start-of-leg before rebreak
```

The current experiment stops at F3 for readability, but the code is structured so more continuation levels can be added by reusing the same child-builder.

## Geometry guard

A valid flag body must keep its waist/correction inside the leg range.

- Bullish: `origin low < waist low < leg1 high`, and `leg2 high > leg1 high`.
- Bearish: `origin high > waist high > leg1 low`, and `leg2 low < leg1 low`.

So the waist cannot move behind the start of the leg.

## Size symmetry

Continuation levels are checked against their direct parent by default:

```text
child_size >= parent_size * InpChildMinParentSizeRatio
```

Size is measured from origin/start-of-leg to Leg2:

```text
flag_size = abs(Leg2.price - Origin.price)
```

Default:

```text
InpRequireChildAtLeastParentSize = true
InpChildMinParentSizeRatio = 1.0
```

## Renderer contract

The renderer is intentionally body-only:

```text
origin -> leg1 = straight line
leg1 -> waist -> leg2 = smooth curve
F1/F2/F3 label = tiny text
1 and 2 = tiny numeric labels only
```

It does not draw any line from Leg2 to `1`, `2`, or the final rebreak.

## Main expert inputs

```text
InpScanF1
InpScanF2
InpScanF3
InpSuppressPromotedLowerLevelBodies
InpRequireParentConfirmedForNextF
InpRequireChildAtLeastParentSize
InpChildMinParentSizeRatio
InpAllowChildWaistBreakBranch
InpDrawF1
InpDrawF2
InpDrawF3
InpDrawBullish
InpDrawBearish
InpColorByDirection
```

## Direction-first color contract

By default, chart colors represent direction, not F-level/status:

- bullish flags use `InpBullishPendingColor` / `InpBullishConfirmedColor`.
- bearish flags use `InpBearishPendingColor` / `InpBearishConfirmedColor`.
- F1/F2/F3 and status remain visible from tiny labels and logs.

## ND / hook context

The current patch does not try to fully formalize ND yet. The intended grammar is:

```text
ND / hook closes a cycle -> F counting starts from the new movement
```

ND is the non-hunted hook / cycle-close context. The next implementation step is to add ND segments as calculation context so the market path can be partitioned into ND phases and F-counting phases rather than drawing isolated flags.

## Reuse pattern

Any future experiment can include only the detector:

```cpp
#include "../../Include/FlagCounting/DAL_FlagCountingDetector.mqh"
```

Then call `FC_DetectFlags(...)` and use `FC_FlagEvent` arrays without the renderer.
