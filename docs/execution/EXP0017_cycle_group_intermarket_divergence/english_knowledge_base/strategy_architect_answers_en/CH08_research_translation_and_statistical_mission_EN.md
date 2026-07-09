# EXP0017 Chapter 08 — Candle Close Confirmation and Trade Permission

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Research Translation

A divergence becomes confirmed and tradeable only after the active chart timeframe candle closes with asymmetry still valid. The research system must convert this doctrine into measurable events, stable fields, and comparable families.

## What Must Be Measured

- `confirmation_time` as a mandatory or recommended statistical field
- `confirmation_candle_timeframe` as a mandatory or recommended statistical field
- `potential_state` as a mandatory or recommended statistical field
- `confirmed_state` as a mandatory or recommended statistical field
- `invalid_at_confirmation` as a mandatory or recommended statistical field

## Research Questions

- Does this family improve win rate?
- Does it improve expectancy?
- Does it reduce stop frequency?
- Does it produce better R outcome, pip outcome, dollar outcome, or normalized pip outcome?
- Does it behave differently by CG, direction, symbol role, time of day, overlap state, reference age, or stop distance?

## Non-Mutation Rule

This chapter may generate research questions, but it does not create live filters in the current version. Statistical discovery must pass through the decision-promotion gate before changing the strategy.
