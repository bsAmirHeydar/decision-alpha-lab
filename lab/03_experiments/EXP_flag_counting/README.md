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
