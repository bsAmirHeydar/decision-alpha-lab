# CH15 — Metric Catalog and Recommended Fields

## Purpose

This document collects the metric families that should be present in the EXP0017 statistical report.

The user defined several core measures and allowed additional recommendations where helpful. This catalog keeps them organized as strategy-level measurement language.

## Mandatory identity fields

Every confirmed signal should preserve:

- trading day;
- confirmation time;
- cycle group;
- current cycle;
- reference cycle;
- reference distance;
- direction;
- hunter symbol;
- clean symbol;
- high-side or low-side divergence;
- cash-session status;
- cycle-end time;
- final validity state.

## Mandatory performance fields

Every confirmed signal should preserve:

- win or loss;
- stop hit or not;
- realized R;
- risk-to-reward result;
- pip / point result;
- dollar result;
- result at cycle end;
- maximum favorable movement;
- maximum adverse movement;
- maximum same-day reward;
- final day result if studied.

## Daily-range-normalized fields

The user defined a key index:

> pip profit divided by total daily market movement in pips.

Recommended normalized fields:

- cycle-end pip result divided by daily range;
- maximum favorable movement divided by daily range;
- maximum adverse movement divided by daily range;
- realized R divided by daily volatility category if later needed;
- clean-symbol movement share of the day.

## Frequency fields

Signal count is part of strategy character.

Recommended fields:

- total signals per day;
- total signals per week;
- total signals per month;
- signals per CG per day;
- buy signals per day;
- sell signals per day;
- SPX clean signals per day;
- NDX clean signals per day;
- cash-session signals per day;
- outside-cash signals per day;
- overlapping signal count;
- conflicting signal count.

## Cycle-group overlap fields

Cycle-group overlap matters but is not assumed to be stronger.

Recommended overlap fields:

- overlap exists or not;
- number of overlapping CGs;
- same-direction overlap;
- opposite-direction overlap;
- same clean-symbol overlap;
- different clean-symbol overlap;
- overlap inside cash session;
- overlap outside cash session;
- overlap with high stop-pressure condition.

## Sequence and fragility fields

Recommended risk-health measures:

- consecutive stops;
- maximum stop streak per CG;
- maximum stop streak per direction;
- maximum stop streak per symbol role;
- drawdown by signal sequence;
- recovery after stop streak;
- dense-day stop behavior;
- monthly bad-sequence behavior.

## Timing fields

Recommended timing fields:

- time from confirmation to first favorable movement;
- time from confirmation to maximum favorable movement;
- time from confirmation to stop;
- time from confirmation to invalidation;
- time from confirmation to cycle end;
- whether best movement happened before or after cycle end.

## Report grouping recommendations

At minimum, every performance report should be groupable by:

- all signals;
- cycle group;
- direction;
- hunter symbol;
- clean symbol;
- time window;
- reference distance;
- cash-session status;
- overlap condition;
- signal frequency regime.

## Non-emotional naming rule

Metric names must describe measurable behavior.

Use:

- high win rate;
- low win rate;
- positive expectancy;
- negative expectancy;
- high normalized movement;
- low normalized movement;
- high signal density;
- repeated stop condition.

Do not use:

- beautiful;
- ugly;
- scary;
- weak by feeling;
- strong by feeling;
- emotional conviction;
- discretionary confidence.

## Final catalog principle

A metric is useful when it helps answer one of these questions:

1. Does this signal family win often enough?
2. Does it produce enough reward when right?
3. Does it move enough in market terms?
4. Does it capture meaningful daily range?
5. Does it appear often enough to matter?
6. Does it fail in dangerous streaks?
7. Does overlap change its behavior?
8. Does timing change its behavior?
9. Does symbol role change its behavior?
10. Does cycle group identity change its behavior?
