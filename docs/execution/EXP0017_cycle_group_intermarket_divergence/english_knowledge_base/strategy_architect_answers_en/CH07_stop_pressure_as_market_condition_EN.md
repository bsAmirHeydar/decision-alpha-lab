# EXP0017 Chapter 07 — Time Validity, Cash Session, and Stop Pressure

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

All times are valid before statistics; the 09:30–16:00 New York cash session is a hypothesis, not a hard rule.

## Locked Doctrine

- Cash session may produce stronger statistics but is not a pre-test filter.
- No sub-session split is mandatory in the base version.
- News is not a base filter.
- Stop-size pressure across CGs is a market condition worth recording.

## Implementation Consequences

- Record session state from day one.
- Do not block non-cash-session signals.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
