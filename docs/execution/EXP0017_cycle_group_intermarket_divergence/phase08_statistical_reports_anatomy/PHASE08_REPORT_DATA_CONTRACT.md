# Phase 08 — Report Data Contract

## Input CSV

Default:

```text
EXP0017_Phase07_Outcome_Study.csv
```

Expected columns:

```text
signal_id
trading_day
confirmation_time
cg_name
direction
side
hunter_symbol
clean_symbol
stop_distance_points
cycle_end_points
cycle_end_R
plus1_cycle_points
plus1_cycle_R
plus2_cycle_points
plus2_cycle_R
plus3_cycle_points
plus3_cycle_R
day_end_points
day_end_R
MFE_points
MFE_R
MAE_points
MAE_R
stop_hit_intraday
stop_hit_time
daily_range_points
day_end_normalized_by_daily_range
MFE_normalized_by_daily_range
```

## Output Reports

```text
EXP0017_Phase08_Overall.csv
EXP0017_Phase08_By_CG.csv
EXP0017_Phase08_By_Direction.csv
EXP0017_Phase08_By_CG_Direction.csv
EXP0017_Phase08_By_Role.csv
EXP0017_Phase08_By_CG_Direction_Role.csv
EXP0017_Phase08_Red_Flags.csv
```

## Report Row Contract

Each report row represents one statistical bucket.

```text
dimension
key
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

## Role Key

The role key is constructed as:

```text
hunter_symbol + "_hunter__" + clean_symbol + "_clean"
```

This allows the reports to compare symbol-role asymmetry without assuming a fixed leader.
