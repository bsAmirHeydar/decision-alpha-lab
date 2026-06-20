# VAL0008 — H4 Causal Batch Validation

Goal: validate H0004 branch-regime memory using the candle on which each regime label becomes knowable, not an arbitrary sample order inside the same candle.

Procedure:

1. Run `M0004_BranchRegimeClustering.mq5` after this release.
2. Compare the classic H4 output against the new `DAL_M0004_FINAL_CAUSAL_*` lines.
3. Treat mixed same-candle reversal/continuation batches as ambiguous rather than as a sequential regime transition.

Decision rule:

- If `removedFakeTransitionPct` is small and causal metrics stay close to classic metrics, H4 is robust to the batch correction.
- If `removedFakeTransitionPct` is high or `DAL_M0004_FINAL_CAUSAL_VS_CLASSIC` says `classic_sequence_materially_changed_by_causal_batching`, the old H4 result must not be used for live regime inference.
