# Phase 08 — Statistical Reports Specification

## Purpose

Phase 08 converts raw signal outcomes into aggregate statistical reports.

The input is the Phase 07 outcome-study CSV. The output is a family of CSV reports that can be used for strategy review, model preparation, and later decision-promotion analysis.

## Primary Question

For confirmed tradeable divergence samples, what does each family do statistically?

Families include:

```text
overall
cycle group
direction
cycle group + direction
hunter-clean role
cycle group + direction + role
```

## Metrics

Each group report includes:

```text
sample_count
win_count
loss_count
zero_count
win_rate_percent
stop_count
stop_rate_percent
max_stop_streak
avg_r
avg_points
avg_normalized
avg_mfe_r
avg_mae_r
avg_stop_distance_points
max_r
min_r
max_points
min_points
```

## Primary Outcome Window

The report can be generated from different outcome windows:

```text
cycle_end
plus1_cycle
plus2_cycle
plus3_cycle
day_end
mfe
```

Default:

```text
cycle_end
```

This preserves the current base target doctrine while allowing later comparison with forward-window and maximum-reward results.

## Red Flags

Phase 08 creates a red-flag report for statistically weak or dangerous families:

```text
bad win rate
negative or weak average R
large stop streak
```

These are warnings only. They do not disable or mutate the strategy.

## Non-Mutation Boundary

Phase 08 may reveal that a family is weak, but it cannot change the execution doctrine. Any change must pass through a later decision-promotion gate.
