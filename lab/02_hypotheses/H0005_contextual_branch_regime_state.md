# H0005 — Contextual Branch Regime State

## Hypothesis

Branch behavior is not only a function of the immediately previous reversal/continuation label. A wider past-only context made of recent branch composition, run length, event spacing, pre-volatility, session, trend, and revisit state creates measurable branch-regime states.

## Base modules

- H0001/M0001: exact structural node events and RTV
- H0002/M0002: exact reversal/continuation labels
- H0003/M0003: volatility inertia/memory
- H0004/M0004: last-event branch-label inertia and run clustering

## Current implementation

Implemented as the contextual extension of M0004 build 1.02.

## Core test

When last branch and wider context disagree, compare:

```text
P(current label follows last branch)
P(current label follows wider context)
```

If wider context wins in disagreement cases and survives engineered nulls, branch-regime is contextual, not merely last-event Markov memory.
