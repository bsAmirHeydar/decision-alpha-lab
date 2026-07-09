# EXP0017 Chapter 05 — Cycle Group Behavioral Unit and Daily Boundary

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

Each cycle group is an independent behavioral unit anchored to the 18:00 New York trading-day boundary. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `cg_name` as a mandatory or recommended statistical field
- `cg_minutes` as a mandatory or recommended statistical field
- `trading_day_start_ny` as a mandatory or recommended statistical field
- `cycle_index` as a mandatory or recommended statistical field
- `cycle_boundary` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
