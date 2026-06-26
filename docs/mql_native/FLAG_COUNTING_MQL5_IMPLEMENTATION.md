# Flag Counting MQL5 Implementation

The active expert is:

```text
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```

It includes reusable modules from:

```text
mql5/Include/FlagCounting/
```

## Core architecture

```text
NodeDetector -> FlagCountingDetector -> optional Renderer
```

The detector emits `FC_FlagEvent` records. The renderer is optional and only draws body geometry and labels.

## Active levels

```text
F1 root
F2 child of F1 from F1.n2
F3 child of F2 from F2.n2
```

Continuation levels share the same builder and can be extended later.

## Confirmation and invalidation

```text
confirm = Leg2 rebreak before invalidation
F1 invalid = waist break
F2/F3 invalid = origin/start break
```

Internal `1/2` are labels/audit and child-origin points. They are not a hard validity gate for the parent body.

## Renderer

The renderer draws:

```text
origin -> leg1
leg1 -> waist -> leg2
F-level label
1/2 labels
```

No post-Leg2 lines are drawn.

## 2026-06 chain-engine repair

The detector is no longer a loose sliding-window pattern scanner. It is now a greedy forward chain counter.

Contract:

- F1 is the only root level.
- After an accepted/confirmed F1, the continuation of that same movement is F2, not another overlapping F1.
- After an accepted/confirmed F2, the continuation is F3.
- F2 origin is parent F1 internal 2.
- F3 origin is parent F2 internal 2.
- Confirmation for every F-level is a rebreak of that F's own Leg2 before invalidation.
- F1 invalidation boundary is its waist.
- F2/F3 invalidation boundary is their own origin/start-of-leg.
- F1 internal 1/2 is searched before the confirming Leg2 rebreak.
- F2/F3 internal 1/2 may appear after a Leg2 extension/rebreak, until origin invalidation.
- The renderer receives only accepted chain events, not all possible overlapping F candidates.

This is a structural correction: market movement is partitioned into unused/ND regions and accepted F-counting chains instead of drawing every local candidate.

## State-machine repair v2

The flag-counting engine is no longer allowed to treat every four-node window as an independent F1 on the same flow. The next continuation level now keeps the parent origin contract but searches flexibly for the child body:

- F2/F3 origin is fixed at the parent internal 2.
- The child Leg1/Waist/Leg2 body may appear within `InpContinuationCoreSearchMaxNodes` nodes after that origin.
- A child continuation is rejected immediately if its own origin/start is invalidated before a valid body appears.
- After a confirmed chain, `InpAvoidSameDirectionF1Restarts` prevents immediate same-direction F1 restarts on the same flow; that unresolved region is treated as ND/hook/transition until an opposite root direction appears or the scan ends.

This is a practical partition step toward the intended market grammar: `ND -> F1 -> F2 -> F3 -> ND -> ...`, instead of loose overlapping pattern overlays.
