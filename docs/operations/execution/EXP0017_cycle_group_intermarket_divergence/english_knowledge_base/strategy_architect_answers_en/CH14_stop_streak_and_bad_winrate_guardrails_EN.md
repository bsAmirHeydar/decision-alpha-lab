# EXP0017 Chapter 14 — Statistical Testing and Performance Metrics

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

The research engine must test win rate, expectancy, stop behavior, outcome windows, and multiple performance measures over a meaningful sample.

## Locked Doctrine

- Win rate matters as an early health filter because fewer stop-outs matter.
- Expectancy matters as a result layer.
- All metric families should be tested independently.
- A minimum initial study of roughly 400 trading days is appropriate.
- Stop streaks and very bad win rate are major red flags.

## Implementation Consequences

- Do not rely only on cycle-end target result.
- Calculate multi-window and maximum intraday outcomes.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
