# EXP0005 — MQL-native H0005 directional memory

Run `M0005_DirectionalMemory.mq5` in MetaTrader Strategy Tester.

Expected build sanity line:

```text
DAL_M0005_BUILD_SANITY ... build=1.00 ... hypothesis=H0005_DIRECTIONAL_MEMORY
```

Key checks:

1. `DAL_M0005_FINAL_OUTCOME_REVERSAL` — structural target success for reversal paths.
2. `DAL_M0005_FINAL_OUTCOME_CONTINUATION` — continuation follow-through before regime change.
3. `DAL_M0005_FINAL_EXCURSION_*` — MFE/MAE until path exit.
4. `DAL_M0005_FINAL_STRESS_*` — direction-flip and matched-random comparisons.
5. Run multiple regime sources and compare `LAST_ONLY` vs `EWMA_CONTEXT` vs `EWMA_CONSENSUS`.
