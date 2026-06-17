# M0001 RTV Distribution Report

## Purpose

This module proves whether final RTV values have a fat-tailed distribution and
how far they are from a fitted normal distribution.

The report uses only final ready events:

```text
event.closed == true
event.rtv_ready == true
event.rtv > 0
```

Unfinished events and `RTV n/a` values are excluded.

## New module

```text
mql5/Include/DecisionAlphaLab/M0001/DAL_M0001RtvDistribution.mqh
```

## Journal report

The EA prints one copyable text report to the Strategy Tester Journal whenever
the ready RTV distribution changes.

Markers:

```text
DAL_M0001_RTV_DISTRIBUTION_REPORT_BEGIN
...
DAL_M0001_RTV_DISTRIBUTION_REPORT_END
```

## Distribution metrics

The report includes:

```text
mean
median
min
max
range
variance
stdev
sample_variance
sample_stdev
coefficient_of_variation
p01/p05/p10/p25/p50/p75/p90/p95/p99
IQR
MAD
robust_sigma_mad
stdev_to_robust_sigma
skewness
excess_kurtosis
Jarque-Bera statistic
Kolmogorov-Smirnov distance to fitted normal
Anderson-Darling statistic to fitted normal
2-sigma and 3-sigma tail percentages
tail ratios against normal expectations
right/left tail asymmetry
normal percentile-width tail ratios
```

## Histogram

The report also prints a tab-separated histogram:

```text
histogram_bin    from    to    count    pct    bar
```

This can be copied directly into Excel or parsed in Python.

## Version

`M0001_LiveVisualLab.mq5` version: `1.53`.
