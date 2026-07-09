# EXP0017 Chapter 09 — Clean Symbol Execution Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

The trade candidate is always the clean symbol: the symbol whose corresponding reference has not been hunted.

## Locked Doctrine

- The clean symbol holds the healthy/unhunted reference.
- Buy divergence expresses buying pressure in the clean symbol.
- Sell divergence expresses selling pressure in the clean symbol.
- No additional quality filter exists in the base layer.

## Implementation Consequences

- Execution modules must bind trade_symbol to clean_symbol.
- Drawing modules must still show hunter evidence clearly.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
