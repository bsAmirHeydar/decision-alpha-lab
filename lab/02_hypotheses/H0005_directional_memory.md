# H0005 — Directional Memory

**Hypothesis:** branch regimes have structural directional memory. Reversal regimes should travel toward the next opposite structural node/zone destination. Continuation regimes should keep moving from the last zone break until the branch regime changes.

Default detector: `LAST_ONLY`.

Context and consensus modes are available for comparison and confidence, but the hypothesis does not assume that context should hard-filter direction.

## v1.01 refinement — adaptive reversal stop and R diagnostics

Reversal paths now distinguish a simple zone-edge invalidation from a hunted zone that later reclaims and reverses. The default reversal stop is the farther of:

1. the far edge of the frozen M0001 zone, and
2. the most adverse hunt extreme reached beyond that edge before the path locks/reclaims.

This keeps a valid reversal hunt from being treated as immediate failure while still measuring the actual stop-loss distance needed by the structure. MFE/MAE remain stopped at path exit. Additional diagnostics report stop distance, hunt depth, stop-hit rate, target distance, R-multiple MFE/MAE/net, and whether the favorable 1x-zone excursion was reached before the adverse 1x-zone excursion.
