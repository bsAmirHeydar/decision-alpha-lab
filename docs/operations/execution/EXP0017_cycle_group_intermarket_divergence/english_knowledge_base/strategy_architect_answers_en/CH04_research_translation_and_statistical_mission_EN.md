# EXP0017 Chapter 04 — Reference Scope and Same-Day Cycle Memory

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

All previous cycles from the same New York trading day are valid reference candidates until invalidated or day-expired. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `reference_cycle_start` as a mandatory or recommended statistical field
- `reference_cycle_end` as a mandatory or recommended statistical field
- `reference_age_cycles` as a mandatory or recommended statistical field
- `same_day_reference_index` as a mandatory or recommended statistical field
- `reference_status` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
