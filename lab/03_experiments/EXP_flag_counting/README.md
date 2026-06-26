# EXP_flag_counting

Unified F-counting experiment for visual and logic research.

Current contract:

- F1 is the root flag body.
- F2 starts from the parent F1 internal `2`.
- F3 starts from the parent F2 internal `2`.
- After a body is promoted to F2/F3, the same body is suppressed from lower-level display by default.
- Every F confirms by rebreaking its own Leg2 before invalidation.
- F1 invalidates at its waist.
- F2/F3 invalidate at their origin/start-of-leg.
- F2/F3 can use the waist-break branch.
- Child levels must be at least parent-sized by default.
- Rendering is body-only: straight origin-to-leg1, curved leg1-waist-leg2, tiny labels only.

ND/hook is documented as the next context layer: the goal is to partition the market into ND cycle-close phases and F-counting movement phases.

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
