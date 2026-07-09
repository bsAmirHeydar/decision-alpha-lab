# EXP0017 Chapter 12 — Signal Persistence and Invalidation Boundary

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

A signal persists unless the divergence itself is invalidated by double hunt; no external filter suppresses it in the base layer.

## Locked Doctrine

- Signals are not removed because another CG exists.
- Signals are not removed because time feels weak.
- Signals are not removed because stop distance is large.
- True invalidation is removal of asymmetry by both-symbol hunt.
- Raw signal validity and trading quality are different concepts.

## Implementation Consequences

- Build signal lifecycle states.
- Do not suppress confirmed signals before statistics.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
