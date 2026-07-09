# EXP0017 Chapter 11 — Cycle Group Independence and Daily Reset

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

CGs, directions, and daily fields are independent in the base layer; previous days do not carry decision authority. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `trading_day` as a mandatory or recommended statistical field
- `cg_name` as a mandatory or recommended statistical field
- `direction` as a mandatory or recommended statistical field
- `same_day_signal_count` as a mandatory or recommended statistical field
- `previous_day_carryover_flag` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
