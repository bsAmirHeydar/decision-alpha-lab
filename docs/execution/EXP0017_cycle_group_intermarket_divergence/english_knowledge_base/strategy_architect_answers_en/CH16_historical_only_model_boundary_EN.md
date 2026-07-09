# EXP0017 Chapter 16 — Statistical Model and Decision Support

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

The model is a historical statistical observer and quality scorer, not an entry/exit authority.

## Locked Doctrine

- The model analyzes past confirmed signals.
- It can evaluate CG type, CG position, win rate, expectancy, pip outcome, and normalized pip outcome.
- It does not alter entries, exits, or strategy rules.
- One unified model should analyze all CGs while preserving separable family tags.

## Implementation Consequences

- Prepare model-ready datasets from ledger fields.
- Keep model output descriptive until rule promotion.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
