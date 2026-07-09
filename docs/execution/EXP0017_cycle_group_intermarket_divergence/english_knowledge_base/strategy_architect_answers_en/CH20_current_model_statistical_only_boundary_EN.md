# EXP0017 Chapter 20 — Version Governance and Strategy Non-Mutation

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

The current version is statistical-only and cannot change strategy; future versions may optimize only after statistical review and explicit promotion.

## Locked Doctrine

- Repeated questions map back to existing doctrine.
- The current model collects and reports statistics only.
- Future optimization may be allowed in later versions.
- The strategy architect decides after statistics.
- CG overlap may become a major modeling complexity source.

## Implementation Consequences

- Separate base version from optimized versions.
- Prevent premature optimization from contaminating raw statistics.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
