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
- After a confirmed parent, `InpForceContinuationAfterConfirmedParent` keeps the state machine waiting for the mandatory next F-level instead of restarting the same flow as another F1.

This is a practical partition step toward the intended market grammar: `ND -> F1 -> F2 -> F3 -> ND -> ...`, instead of loose overlapping pattern overlays.

## Mandatory continuation state machine v3

The flag-counting experiment is no longer allowed to reinterpret the same flow as repeated F1 bodies. The active contract is:

- F1 is the only root level.
- After a confirmed F1, the engine must search F2 from the parent F1 internal 2.
- After a confirmed F2, the engine must search F3 from the parent F2 internal 2.
- F2/F3 may extend for many nodes and remain live/pending until their own Leg2 is rebroken.
- `InpContinuationCoreSearchMaxNodes = 0` means continuation search is not capped by a small local window; it searches until origin invalidation or the end of the available node stream.
- `InpForceContinuationAfterConfirmedParent = true` prevents the detector from falling back to another same-flow F1 when the mandatory child level is not yet resolved.
- F1 can repair an early waist candidate by selecting a later valid waist/core before confirmation. This prevents premature fragmentation into many F1 labels.
- F1 invalidation boundary is its selected waist.
- F2 and F3 invalidation boundary is their own origin/start-of-leg.
- Confirmation for every F level remains: rebreak of the event's own Leg2 before its invalidation boundary.

Recommended live settings:

```text
InpRootCoreSearchMaxNodes = 80
InpContinuationCoreSearchMaxNodes = 0
InpForceContinuationAfterConfirmedParent = true
InpRequireParentConfirmedForNextF = true
InpRequireChildAtLeastParentSize = true
InpChildMinParentSizeRatio = 1.0
```

- A confirmed F1 without internal 2 is not accepted as a chain root, because it cannot hand off to F2.

## Live root visibility repair

A valid F1 must not be hidden merely because its internal `2` is not yet available for F2 continuation. In live counting this means the F1 owns the current segment and the next level is pending. Confirmed or open F1 roots remain drawable; F2/F3 are added only when their continuation origin and body become available.
