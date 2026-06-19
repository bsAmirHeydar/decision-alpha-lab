# M0004 reports

Paste or archive MT5 Journal output for `DAL_M0004_*` final reports here.

## v1.01 report additions

M0004 v1.01 adds expanded regime detail and strict engineered random/null diagnostics:

- `FINAL_BLOCK_PROFILE_FAST/MAIN/SLOW` for branch concentration across multiple event-block granularities.
- `FINAL_RUN_LENGTH_TRANSITION` for duration-dependent branch persistence.
- `FINAL_LAG_DECAY` for local-vs-far branch memory decay.
- `FINAL_STRATIFIED_PERM_SESSION/PREVOL/REVISIT/COMPOSITE` for stricter label shuffles preserving branch counts inside regime strata.
- `FINAL_CIRCULAR_SHIFT_STRESS` for far-shift adjacency placebo.
- `FINAL_BLOCK_ORDER_SHUFFLE_STRESS` for a block-preserving null.
- `FINAL_*_DETAIL_*` lines for richer session, pre-volatility, revisit, and event-spacing regime diagnostics.

The strongest null is the composite stratified permutation, which preserves branch counts within `session × pre-vol tercile × trend regime × revisit bucket` before testing branch inertia.

## v1.04 consensus quality diagnostics

M0004-v1.04 adds modular signal-quality reports for comparing:

```text
last-only branch signal
last-context consensus accepted signal
last-only signals rejected by consensus
conflict last-branch signal
conflict context signal
neutral last-branch signal
```

Use the `*_QUALITY_COMPARE_*` lines to determine whether consensus is merely reproducing last-only behavior or truly filtering for higher-quality branch-regime states.
