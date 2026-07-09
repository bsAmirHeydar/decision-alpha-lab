# EXP0017 Chapter 10 — Risk, Stop, Time Exit, and Outcome Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

Risk is fixed in the base version, stop is absolute at the clean reference, and the initial target concept is time-based.

## Locked Doctrine

- Base risk is fixed at 1% equity.
- Stop price is the clean symbol reference level.
- No quality-based risk adjustment exists before statistics.
- Cycle-end exit is the base time target, but later studies may add alternative targets.
- Dollar result is an important statistical outcome.

## Implementation Consequences

- Separate stop logic from model scoring.
- Record multiple outcome windows even if base exit remains cycle-end.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
