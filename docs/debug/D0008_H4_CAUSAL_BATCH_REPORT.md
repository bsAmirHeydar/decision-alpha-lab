# D0008 / H0004 Causal Known-Candle Batch Report

This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts samples by `outcome_index`, then by `entry_index`, then by `id`. That is acceptable as an exploratory sample sequence, but it can create fake within-candle transitions when several highs/lows are confirmed on the same bar.

The new causal batch layer groups samples by their knowable candle:

- `known_index = outcome_index` when available
- else `exit_index`
- else `entry_index`

All samples with the same `known_index` are treated as simultaneous. A batch with only reversal labels is a reversal batch. A batch with only continuation labels is a continuation batch. A batch containing both reversal and continuation labels is marked ambiguous and skipped from causal transition/run statistics.

The classic report is still printed for continuity, but the new `DAL_M0004_FINAL_CAUSAL_*` lines are the live-style sequence diagnostics that should be used before trusting H0004 as a regime-memory signal.

Important new log lines:

- `DAL_M0004_FINAL_CAUSAL_BATCH_AUDIT`
- `DAL_M0004_FINAL_CAUSAL_BATCH_SUMMARY`
- `DAL_M0004_FINAL_CAUSAL_BATCH_TRANSITION`
- `DAL_M0004_FINAL_CAUSAL_BATCH_RUNS`
- `DAL_M0004_FINAL_CAUSAL_VS_CLASSIC`
- `DAL_M0004_FINAL_CAUSAL_BATCH_TRANSITION_PERM_STRESS`
- `DAL_M0004_FINAL_CAUSAL_BATCH_RUN_SHUFFLE_STRESS`

The key field is `removedFakeTransitions`. If this number is materially large, the old sample-sequence report was turning same-candle simultaneous outcomes into fake regime transitions.
