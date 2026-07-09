# EXP0017 Chapter 15 — Statistical Reporting and Metric Language

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

Reports must use measurable statistical language and include only confirmed tradeable signals in the primary sample. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `primary_sample_flag` as a mandatory or recommended statistical field
- `cg_type` as a mandatory or recommended statistical field
- `risk_reward` as a mandatory or recommended statistical field
- `pip_outcome` as a mandatory or recommended statistical field
- `daily_range_normalized_pip` as a mandatory or recommended statistical field
- `signal_frequency` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
