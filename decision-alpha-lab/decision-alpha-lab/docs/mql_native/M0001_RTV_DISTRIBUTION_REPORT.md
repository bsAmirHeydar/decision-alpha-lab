# M0001 RTV Distribution Report — Retired Module Note

This document describes the older verbose distribution-report phase from version `1.53`.

The active runtime no longer includes:

```text
mql5/Include/DecisionAlphaLab/M0001/DAL_M0001RtvDistribution.mqh
```

The current active report is the compact final-only node-vs-random logRTV report:

```text
DAL_M0001_FINAL_NODES
DAL_M0001_FINAL_RANDOM
```

The active statistical module is:

```text
mql5/Include/DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh
```

It still preserves the important distribution logic in compact form:

- raw RTV mean/median/percentiles,
- logRTV mean/median,
- positive logRTV percentage,
- skewness,
- excess kurtosis,
- Jarque-Bera statistic,
- KS distance to fitted normal,
- tail ratios,
- node-vs-random paired comparison.

For current semantics, use:

```text
docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md
```
