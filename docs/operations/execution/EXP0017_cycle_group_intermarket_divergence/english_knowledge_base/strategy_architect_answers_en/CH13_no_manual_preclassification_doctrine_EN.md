# EXP0017 Chapter 13 — Statistical Uncertainty and No Manual Quality Doctrine

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

Before statistical testing, most quality claims are unknown and must remain unknown.

## Locked Doctrine

- No directional quality is assumed.
- No symbol-role quality is assumed.
- No time-window quality is assumed.
- No reference-distance quality is assumed.
- Future ideas are stored as backlog, not base rules.

## Implementation Consequences

- Design the dataset to preserve raw variation.
- Avoid preclassification that contaminates the sample.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
