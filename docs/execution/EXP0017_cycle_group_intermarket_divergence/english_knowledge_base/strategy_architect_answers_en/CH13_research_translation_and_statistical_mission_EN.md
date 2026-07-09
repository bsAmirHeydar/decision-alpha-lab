# EXP0017 Chapter 13 — Statistical Uncertainty and No Manual Quality Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

Before statistical testing, most quality claims are unknown and must remain unknown. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `unknown_quality_marker` as a mandatory or recommended statistical field
- `test_required_flag` as a mandatory or recommended statistical field
- `hypothesis_id` as a mandatory or recommended statistical field
- `family_id` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
