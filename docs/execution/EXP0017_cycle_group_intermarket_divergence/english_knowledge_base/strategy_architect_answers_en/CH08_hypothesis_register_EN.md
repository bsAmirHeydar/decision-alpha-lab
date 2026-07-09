# EXP0017 Chapter 08 — Candle Close Confirmation and Trade Permission

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Hypothesis Register

| ID | Hypothesis / Claim | Current Status | Governance |
|---|---|---|---|
| H08-01 | Hunt can happen intrabar; confirmation waits for candle close. | Open until tested | Do not convert into a live rule before statistical review. |
| H08-02 | If both symbols have hunted by confirmation time, no trade exists. | Open until tested | Do not convert into a live rule before statistical review. |
| H08-03 | Temporal close is not a price filter. | Open until tested | Do not convert into a live rule before statistical review. |
| H08-04 | All confirmed signals should remain visible. | Open until tested | Do not convert into a live rule before statistical review. |

## Promotion Rule

A hypothesis becomes a strategy rule only after sufficient sample size, clean measurement, comparison against alternatives, and explicit strategy-architect approval.
