# EXP0005 — MQL-native H0005 directional memory

Run `M0005_DirectionalMemory.mq5` in MetaTrader Strategy Tester.

Expected build sanity line:

```text
DAL_M0005_BUILD_SANITY ... build=1.03 ... hypothesis=H0005_DIRECTIONAL_MEMORY
```

Key checks:

1. `DAL_M0005_FINAL_OUTCOME_REVERSAL` — structural target success for reversal paths.
2. `DAL_M0005_FINAL_OUTCOME_CONTINUATION` — continuation follow-through before regime change.
3. `DAL_M0005_FINAL_EXCURSION_*` — MFE/MAE until path exit.
4. `DAL_M0005_FINAL_REALIZED_R_*` — realized win rate, R:R, profit factor, and expectancy R.
5. `DAL_M0005_FINAL_FLOATING_R_*` — floating MFE/MAE R, floating R:R, and R-based first-hit order.
6. `DAL_M0005_FINAL_RANDOM_PERFORMANCE_*` — actual versus matched-random win rate, profit factor, expectancy R, MFE R, and floating R:R.
7. `DAL_M0005_FINAL_STRESS_*` — direction-flip and matched-random excursion comparisons.
8. Run multiple regime sources and compare `LAST_ONLY` vs `EWMA_CONTEXT` vs `EWMA_CONSENSUS`.


M0005 v1.03 adds `DAL_M0005_FINAL_REVERSAL_TRADE_R1` and `DAL_M0005_FINAL_REVERSAL_TRADE_R2` report lines. These are raw cost-excluded, execution-style reversal simulations with fixed +1R/+2R targets, -1R structural stop, path-exit fallback, same-bar TP/SL policy, and matched-random baselines.
