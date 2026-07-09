# EXP0017 Chapter 19 — Direction Conflict and Cycle Independence

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

Buy and sell divergences, same-direction clusters, opposite-direction clusters, CGs, and internal cycles remain independent before statistics.

## Locked Doctrine

- High-hunt asymmetry produces sell divergence.
- Low-hunt asymmetry produces buy divergence.
- Late entry and large stop are not base filters.
- Post-confirmation invalidation is recorded as later invalidation, not proof the original signal was never valid.
- Signal count does not change validity.

## Implementation Consequences

- Record conflict clusters instead of resolving them manually.
- Do not force non-divergence behavior into the divergence dataset.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
