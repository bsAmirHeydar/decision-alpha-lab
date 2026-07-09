# EXP0017 Chapter 05 — Cycle Group Behavioral Unit and Daily Boundary

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

Each cycle group is an independent behavioral unit anchored to the 18:00 New York trading-day boundary.

## Locked Doctrine

- The trading day begins at 18:00 New York and ends at 17:00 New York.
- Each CG is a family of potential divergence behavior.
- All CGs are allowed in the base version.
- No CG is stronger or weaker before statistics.

## Implementation Consequences

- Build the CG calendar before reference and hunt logic.
- Avoid CG ranking in the base implementation.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
