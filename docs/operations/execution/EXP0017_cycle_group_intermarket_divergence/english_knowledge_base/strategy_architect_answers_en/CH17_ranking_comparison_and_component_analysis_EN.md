# EXP0017 Chapter 17 — AI Role Boundary and Strategy Integrity

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

AI is an analyst, ranker, and comparer; it may learn the strategy architect language but cannot mutate the strategy.

## Locked Doctrine

- AI must not change CG definitions, entry conditions, time target, daily boundary, or fixed doctrine.
- AI may learn the strategy architect’s language if this improves reporting.
- Component analysis and quality ranking are more important than autonomous decisions.
- All signals should be analyzed; none should be silently ignored.

## Implementation Consequences

- Design AI interfaces as reports and comparisons.
- Route every suggested change through human review.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
