# EXP0017 Chapter 04 — Reference Scope and Same-Day Cycle Memory

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

All previous cycles from the same New York trading day are valid reference candidates until invalidated or day-expired.

## Locked Doctrine

- Reference candidates are the high and low of previous cycles in the same CG and same trading day.
- No previous-day reference is used for live decision.
- No reference hierarchy is assumed before statistics.
- A reference becomes invalid for divergence only when the asymmetry is removed by double hunt.

## Implementation Consequences

- The reference field must store all previous same-day cycle highs/lows.
- The engine must not use yesterday’s references for live signals.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
