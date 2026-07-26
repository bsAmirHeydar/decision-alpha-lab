# Phase 08 — Red Flag Reporting Contract

## Purpose

The red-flag report identifies statistical weakness. It does not disable signals.

## Red Flag Types

```text
bad_win_rate
bad_average_r
stop_streak
```

## Default Thresholds

```text
minimum_sample_for_flag = 30
bad_win_rate_threshold_percent = 40.0
bad_average_r_threshold = 0.0
bad_stop_streak_threshold = 5
```

## Interpretation

A red flag means:

```text
This family needs review.
```

It does not mean:

```text
Disable the CG.
Change the strategy.
Filter the signal.
Change risk.
Change target.
```

Any rule promotion belongs to a later decision phase.
