# DAL Flag Counting Module

This module is the unified flag-counting experiment. It is not a loose pattern scanner. The intended model is a fractal, multi-sequence counting grammar over market nodes.

## Files

```text
mql5/Include/FlagCounting/DAL_FlagCountingTypes.mqh
mql5/Include/FlagCounting/DAL_FlagCountingNodeDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingDetector.mqh
mql5/Include/FlagCounting/DAL_FlagCountingRenderer.mqh
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

The expert uses local relative includes, so it does not require copying files into the terminal-level `MQL5/Include` folder.

## Core idea

Flag counting is a counting language, not isolated pattern detection.

```text
ND / Hook phase -> F1 -> F2 -> F3 -> ...
```

Several sequences can exist in parallel because the structure is fractal. A small-scale sequence and a larger-scale sequence may both be valid at the same time. The detector therefore supports multiple swing scales and multiple active sequences.

## Node and scale model

The node engine builds alternating swing highs/lows from one or more swing scales.

Useful scale inputs:

```text
InpUseMultiScale = true
InpSwingL = 3
InpSwingL2 = 5
InpSwingL3 = 8
InpSwingL4 = 13
InpSwingL5 = 21
InpSwingL6 = 0
```

`scaleL` is stored and printed for every event so a drawn F can be traced back to the scale that generated it.

## Sequence model

Each accepted F1 opens a sequence. That sequence waits for F2. When F2 is confirmed, the same sequence waits for F3.

```text
sequence A, scale 3: F1 -> waiting F2 -> F2 -> waiting F3
sequence B, scale 8: F1 -> waiting F2
sequence C, scale 13: ND / hook context -> F1
```

This means the chart should not depend on one global state machine. A blocked or live continuation in one sequence must not prevent other sequences from existing.

## F1 contract

F1 is the root body.

Bullish F1:

```text
origin low -> leg1 high -> waist low -> leg2 high breaking leg1
```

Bearish F1:

```text
origin high -> leg1 low -> waist high -> leg2 low breaking leg1
```

F1 geometry guard:

```text
bullish: origin < waist < leg1, and leg2 > leg1
bearish: origin > waist > leg1, and leg2 < leg1
```

The waist/correction cannot fall behind the start of the leg.

F1 confirmation and invalidation:

```text
confirmed = own Leg2 rebreak before invalidation
invalidated = own waist break before Leg2 rebreak
```

After F1 is accepted, the continuation of that sequence is F2. Another F1 may still exist in another scale or another sequence, but the same sequence does not reinterpret its continuation as another F1.

## F2 contract

F2 is a continuation count from the parent F1.

```text
F2 origin = parent F1 internal 2
```

F2 direction is inherited from the parent sequence. F2 can extend for a long time. It remains live/pending until confirmed or invalidated.

F2 confirmation and invalidation:

```text
confirmed = own Leg2 rebreak before invalidation
invalidated = own origin/start break before Leg2 rebreak
```

Important difference from F1: F2 may break its own waist without invalidation. A waist-break branch is allowed:

```text
1 = F2 waist
2 = node that breaks F2 waist
```

F2 can also extend beyond its Leg2 and later return to form its branch/labels. This does not invalidate the F2 as long as its origin is not broken.

## F3 contract

F3 is the next continuation count.

```text
F3 origin = parent F2 internal 2
```

F3 uses the continuation-level contract, like F2:

```text
confirmed = own Leg2 rebreak before invalidation
invalidated = own origin/start break before Leg2 rebreak
```

F3 may also use the continuation waist-break branch. The current experiment stops at F3 for chart readability, but the grammar is written so higher levels can be added later.

## Internal 1/2 labels

Internal `1` and `2` are part of the counting audit and child-origin logic. They are drawn as tiny labels only; no post-Leg2 path is drawn.

For F1, the internal branch is expected before the confirming Leg2 rebreak.

For F2/F3, the branch may form after extension beyond Leg2, until origin invalidation.

## Size symmetry

Continuation levels are checked against their direct parent by default.

```text
child_size >= parent_size * InpChildMinParentSizeRatio
flag_size = abs(Leg2.price - Origin.price)
```

Default:

```text
InpRequireChildAtLeastParentSize = true
InpChildMinParentSizeRatio = 1.0
```

So a child F should be at least the body size of its parent unless the input is disabled.

## Mandatory continuation

The logical continuation contract is:

```text
F1 confirmed -> search/wait for F2 from F1 internal 2
F2 confirmed -> search/wait for F3 from F2 internal 2
```

The child may be delayed and very large. `InpContinuationCoreSearchMaxNodes = 0` means child search is not capped by a small node window; it searches until invalidation or end of available data.

## Fractal multi-sequence behavior

The latest engine layer allows every valid F1 root to open its own sequence. This is necessary because the structure is fractal and can appear across several scales.

Controls:

```text
InpUseMultiScale
InpSwingL / InpSwingL2 / InpSwingL3 / InpSwingL4 / InpSwingL5 / InpSwingL6
InpMaxRootSequencesPerScale
```

`InpMaxRootSequencesPerScale = 0` means no per-scale root cap.

## ND / Hook context

ND is the hook/cycle-close context that is not hunted. It does not need a strict 90% return. Conceptually, every market segment should eventually be classified as either ND/hook context or F-counting movement.

Current implementation status:

```text
implemented: F1/F2/F3 multi-scale sequence registry
not fully implemented yet: explicit ND segment renderer/partitioner
```

ND remains the next layer: it should decide when a sequence ends and when a new root context is allowed.

## Renderer contract

The renderer is intentionally body-only:

```text
origin -> leg1 = straight line
leg1 -> waist -> leg2 = smooth curve
F1/F2/F3 label = tiny text
1 and 2 = tiny numeric labels only
```

It does not draw a line from Leg2 to `1`, `2`, or the final rebreak.

Direction-first colors are enabled by default:

```text
bullish pending/confirmed = bullish colors
bearish pending/confirmed = bearish colors
```

F-level and status are read from tiny labels and logs.

## Main expert inputs

```text
InpUseMultiScale
InpSwingL
InpSwingL2
InpSwingL3
InpSwingL4
InpSwingL5
InpSwingL6
InpMaxRootSequencesPerScale
InpScanF1
InpScanF2
InpScanF3
InpDrawF1
InpDrawF2
InpDrawF3
InpDrawBullish
InpDrawBearish
InpDrawOnlyConfirmed
InpContinuationCoreSearchMaxNodes
InpRequireParentConfirmedForNextF
InpRequireChildAtLeastParentSize
InpChildMinParentSizeRatio
InpAllowChildWaistBreakBranch
InpColorByDirection
```

## Recommended live research settings

```text
InpUseMultiScale = true
InpSwingL = 3
InpSwingL2 = 5
InpSwingL3 = 8
InpSwingL4 = 13
InpSwingL5 = 21
InpSwingL6 = 0
InpMaxRootSequencesPerScale = 0
InpContinuationCoreSearchMaxNodes = 0
InpRequireParentConfirmedForNextF = true
InpRequireChildAtLeastParentSize = true
InpChildMinParentSizeRatio = 1.0
InpDrawOnlyConfirmed = false
```

## Debug log fields

`FC_EVENT` should include:

```text
level=
direction=
status=
branch=
scaleL=
chain=
step=
size=
parentSize=
sizeRatio=
```

Use `scaleL`, `chain`, and `step` to determine whether a visual issue comes from scale selection, sequence ownership, or F-level continuation.
