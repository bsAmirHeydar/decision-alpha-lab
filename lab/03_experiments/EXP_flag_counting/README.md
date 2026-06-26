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
