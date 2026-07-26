# EXP0017 Chapter 18 — Execution Freedom and Position Multiplicity

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

The base execution field has no position-count limit, allows repeated CG opportunities, and permits hedging unless statistics later justify constraints.

## Locked Doctrine

- Multiple positions from one CG are allowed.
- Loss in one cycle does not block the next cycle.
- Hedging is allowed in the base layer.
- Immediate entry after final confirmation is the base timing.
- Only invalidation at confirmation blocks trade permission.

## Implementation Consequences

- Raw execution must preserve signal freedom.
- Future exposure constraints are statistical hypotheses, not base filters.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
