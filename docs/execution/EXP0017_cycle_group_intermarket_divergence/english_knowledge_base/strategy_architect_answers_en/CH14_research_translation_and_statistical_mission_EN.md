# EXP0017 Chapter 14 — Statistical Testing and Performance Metrics

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

The research engine must test win rate, expectancy, stop behavior, outcome windows, and multiple performance measures over a meaningful sample. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `win_rate` as a mandatory or recommended statistical field
- `stop_rate` as a mandatory or recommended statistical field
- `expectancy` as a mandatory or recommended statistical field
- `r_outcome` as a mandatory or recommended statistical field
- `pip_outcome` as a mandatory or recommended statistical field
- `max_intraday_reward` as a mandatory or recommended statistical field
- `stop_streak` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
