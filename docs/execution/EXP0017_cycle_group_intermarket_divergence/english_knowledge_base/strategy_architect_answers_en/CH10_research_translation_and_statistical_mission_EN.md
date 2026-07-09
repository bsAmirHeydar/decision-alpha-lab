# EXP0017 Chapter 10 — Risk, Stop, Time Exit, and Outcome Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

Risk is fixed in the base version, stop is absolute at the clean reference, and the initial target concept is time-based. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `risk_percent` as a mandatory or recommended statistical field
- `stop_price` as a mandatory or recommended statistical field
- `stop_distance` as a mandatory or recommended statistical field
- `cycle_end_time` as a mandatory or recommended statistical field
- `dollar_outcome` as a mandatory or recommended statistical field
- `r_outcome` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
