# EXP0017 Chapter 08 — Candle Close Confirmation and Trade Permission

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Core Thesis

A divergence becomes confirmed and tradeable only after the active chart timeframe candle closes with asymmetry still valid.

## Locked Doctrine

- Hunt can happen intrabar; confirmation waits for candle close.
- If both symbols have hunted by confirmation time, no trade exists.
- Temporal close is not a price filter.
- All confirmed signals should remain visible.

## Implementation Consequences

- The EA must use closed candle events as the final signal boundary.
- Do not execute on intrabar potential states.

## What This Chapter Does Not Allow

- It does not permit premature ranking.
- It does not permit untested filtering.
- It does not permit AI-driven mutation of the current strategy.
- It does not replace statistical testing with visual or emotional judgment.

## Required Traceability

Every code module that implements this doctrine should produce inspectable state: timestamps, cycle IDs, references, hunt states, divergence states, confirmation states, invalidation states, and report fields where relevant.
