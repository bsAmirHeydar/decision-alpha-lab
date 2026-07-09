# EXP0017 Chapter 01 — Strategy Identity and Divergence Language

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

EXP0017 treats intermarket divergence as behavioral asymmetry between two related markets inside a defined cycle-group field.

## Locked Doctrine

- Divergence is the strategy language, not an auxiliary filter.
- The project studies the difference between two markets inside selected time cycles.
- Profitability is the ultimate validation layer, but anatomy must be built before profitability decisions.
- The strategy is a complete behavioral language for SPXUSD and NDXUSD, not a single pattern label.

## Implementation Consequences

- Build a signal vocabulary before an execution module.
- Do not add external narratives before the internal anatomy is stable.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
