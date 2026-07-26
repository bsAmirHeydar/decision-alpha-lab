# Phase 12.5 Limits and Non-Goals

## Limits

- MQL5 row inspection is intentionally capped for terminal responsiveness.
- Python CSV loading is in-memory and should later be upgraded to streaming if datasets exceed available RAM.
- Timestamp audit validates parseability and fold order, not broker-history truth.
- Exact Phase 07 → Phase 10 lineage assumes Phase 10 preserves excluded identities as documented.
- The auditor cannot prove that market prices themselves were correct; it proves pipeline consistency.

## Non-goals

Phase 12.5 does not:

- rediscover divergence;
- alter the extreme-frontier algorithm;
- recompute outcomes;
- choose the best CG;
- optimize thresholds;
- train a production model;
- approve a strategy rule;
- place or manage trades;
- modify risk or targets.
