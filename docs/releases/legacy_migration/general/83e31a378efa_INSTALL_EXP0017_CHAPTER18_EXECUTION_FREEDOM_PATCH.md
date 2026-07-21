# INSTALL — EXP0017 Chapter 18 Execution Freedom Patch

This patch adds Chapter 18 strategy-architect doctrine for EXP0017 Cycle Group Intermarket Divergence.

Scope:
- execution permission after final candle-close confirmation
- no base limit on number of positions
- independent cycle groups and independent cycles
- multiple positions from the same CG allowed
- repeated opportunities allowed even after a losing cycle
- hedging allowed in the base layer
- immediate entry after final confirmation
- no restriction except true divergence invalidation at the final confirmation moment

No code is included in this patch.
