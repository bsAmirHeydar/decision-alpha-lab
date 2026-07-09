# Cycle Group Calendar Doctrine

## Definition

A cycle group is a fixed-duration partition of the New York trading day.

The day is anchored at:

```text
18:00 New York
```

and ends at:

```text
17:00 New York next calendar day
```

This creates a 23-hour analysis window.

## Supported groups

```text
3, 5, 9, 10, 15, 18, 20, 24, 30, 40, 45, 60, 72, 90, 120, 150, 180, 240, 300, 360, 720 minutes
```

## Core formula

```text
minutes_from_day_start = NY_time - NY_day_start_18_00
cycle_index = floor(minutes_from_day_start / duration_minutes)
cycle_end = min(day_start + (cycle_index + 1) × duration, day_end_17_00)
```

## Important consequence

Some groups have incomplete final cycles because 1380 minutes is not divisible by every duration.

Incomplete final cycles remain valid. Their target end is 17:00 NY.

## First-cycle rule

The first cycle of every CG cannot produce a baseline signal because there is no previous completed cycle inside the same trading day.

