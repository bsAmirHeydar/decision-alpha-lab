# EXP0017 Chapter 03 — Hunt Doctrine and Reference Validity

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

A hunt is a high/low touch or break of a reference level; close beyond the level is not required.

## Locked Doctrine

- High hunt: current high >= reference high.
- Low hunt: current low <= reference low.
- Equality counts as a hunt.
- Close beyond the level is not required.
- If both symbols hunt their corresponding references, divergence is invalid.

## Implementation Consequences

- Use OHLC high/low data, not close-only logic.
- Separate intrabar hunt occurrence from final close confirmation.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
