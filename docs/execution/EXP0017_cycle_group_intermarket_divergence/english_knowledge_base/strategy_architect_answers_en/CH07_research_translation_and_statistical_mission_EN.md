# EXP0017 Chapter 07 — Time Validity, Cash Session, and Stop Pressure

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

All times are valid before statistics; the 09:30–16:00 New York cash session is a hypothesis, not a hard rule. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `cash_session_flag` as a mandatory or recommended statistical field
- `time_from_cash_open` as a mandatory or recommended statistical field
- `time_to_cash_close` as a mandatory or recommended statistical field
- `stop_distance` as a mandatory or recommended statistical field
- `cg_stop_pressure_rank` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
