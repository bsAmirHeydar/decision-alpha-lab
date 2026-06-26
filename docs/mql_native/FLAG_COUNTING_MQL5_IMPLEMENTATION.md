# Flag Counting MQL5 Implementation

Active expert:

```text
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

Reusable modules:

```text
mql5/Include/FlagCounting/DAL_FlagCountingTypes.mqh
mql5/Include/FlagCounting/DAL_FlagCountingNodeDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingRenderer.mqh
```

## Architecture

```text
MqlRates
  -> multi-scale node streams
  -> fractal sequence registry
  -> F1/F2/F3 event records
  -> optional body-only renderer
```

The current detector is intended to be a multi-sequence counting engine, not a loose overlay scanner.

## Data contract

Each `FC_FlagEvent` should carry enough information to audit:

```text
level: F1/F2/F3
direction: bullish/bearish
status: open/confirmed/invalidated
scale_L: swing scale
chain_id: sequence id
chain_step: step inside that sequence
origin, leg1, waist, leg2
internal 1/2
confirm point
invalidation boundary
size, parent size, size ratio
```

## F1 implementation contract

F1 is the root body.

```text
bullish: origin low -> leg1 high -> waist low -> leg2 high
bearish: origin high -> leg1 low -> waist high -> leg2 low
```

F1 validity:

```text
waist must stay between origin and leg1
leg2 must break leg1
```

F1 lifecycle:

```text
confirmed = rebreak own Leg2 before waist invalidation
invalidated = break own waist before Leg2 rebreak
```

## F2/F3 implementation contract

Continuation levels inherit direction from the parent and start from the parent internal `2`.

```text
F2 origin = F1.N2
F3 origin = F2.N2
```

Continuation lifecycle:

```text
confirmed = rebreak own Leg2 before own origin invalidation
invalidated = break own origin/start before own Leg2 rebreak
```

Continuation levels may break their own waist. A waist-break branch is interpreted as:

```text
1 = waist
2 = node breaking the waist
```

## Mandatory but live continuation

After F1, the sequence waits for F2. After F2, it waits for F3. The child can be delayed or very large. The parent remains visible/live while the child is not yet complete.

`InpContinuationCoreSearchMaxNodes = 0` means no small-window cap; search continues until invalidation or the end of the node stream.

## Fractal multi-sequence layer

The market can produce F-counting sequences at different scales in parallel. The detector supports this with:

```text
InpUseMultiScale
InpSwingL..InpSwingL6
InpMaxRootSequencesPerScale
```

Every event receives `scale_L` and `chain_id` for audit. This avoids the previous failure mode where one global chain blocked the rest of the chart.

## Renderer

The renderer draws only the F body:

```text
origin -> leg1
leg1 -> waist -> leg2
small F-level label
small internal 1/2 labels
```

It does not draw post-Leg2 branches or confirmation paths.

## ND / Hook layer

ND is the non-hunted hook/cycle-close phase. The intended full grammar is:

```text
ND -> F1 -> F2 -> F3 -> ND -> ...
```

Explicit ND segmentation is still a roadmap item. The current implementation focuses on multi-scale parallel F-sequences and keeps ND as documented context.

## Compile note

MQL5 arrays must be passed by reference. Helper functions that accept arrays use signatures such as:

```cpp
bool FC_ScaleAlreadyListed(const int &scales[], const int count, const int value)
```

This avoids the MetaEditor compile error: `arrays are passed by reference only`.
