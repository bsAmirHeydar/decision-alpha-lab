# EXP0017 Chapter 11 — Cycle Group Independence and Daily Reset

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

CGs, directions, and daily fields are independent in the base layer; previous days do not carry decision authority.

## Locked Doctrine

- Buy and sell are both valid research families.
- CGs do not validate or cancel each other before statistics.
- No confluence assumption exists before testing.
- Every day is independent from previous days for live decision.

## Implementation Consequences

- Implement same-day decision memory and research memory separately.
- Do not carry references from prior days into live signal construction.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
