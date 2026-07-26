# EXP0017 Chapter 15 — Statistical Reporting and Metric Language

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

Reports must use measurable statistical language and include only confirmed tradeable signals in the primary sample.

## Locked Doctrine

- Primary samples include valid confirmed tradeable signals only.
- Reports should include CG type, win rate, R:R, pip outcome, normalized pip outcome, CG overlap, and signal frequency.
- Emotional language has no place in expert reports.
- Recommended metrics may be added if they enrich statistical memory.

## Implementation Consequences

- Build a report schema before AI scoring.
- Keep raw observations and primary samples separate.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
