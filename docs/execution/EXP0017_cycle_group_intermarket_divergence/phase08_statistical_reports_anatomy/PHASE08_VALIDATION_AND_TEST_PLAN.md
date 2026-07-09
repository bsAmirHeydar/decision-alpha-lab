# Phase 08 — Validation and Test Plan

## Compile Test

Compile:

```text
EXP0017_CG_Statistical_Report_Anatomy.mq5
```

## File Read Test

Confirm that the expert can read:

```text
EXP0017_Phase07_Outcome_Study.csv
```

If no samples are loaded, check:

```text
Files folder
Common Files setting
CSV filename
header names
CSV delimiter
```

## Report Generation Test

Confirm creation of:

```text
Overall
By_CG
By_Direction
By_CG_Direction
By_Role
By_CG_Direction_Role
Red_Flags
```

## Metric Sanity Test

For a small manual CSV, verify:

```text
sample_count equals row count
win_count equals positive R count
loss_count equals negative R count
win_rate = wins / sample count
stop_count equals stop_hit_intraday true count
avg_r equals arithmetic mean
max_stop_streak increments only on consecutive stop-hit rows inside a group
```

## Boundary Test

Confirm that Phase 08 does not:

```text
place orders
change chart drawings
open positions
calculate position size
filter live signals
change CG permissions
```
