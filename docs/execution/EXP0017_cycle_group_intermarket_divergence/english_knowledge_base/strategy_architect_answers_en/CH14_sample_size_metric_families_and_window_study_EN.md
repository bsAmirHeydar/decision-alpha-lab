# EXP0017 Chapter 14 — Statistical Testing and Performance Metrics

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Metric / Field Catalog

| Field | Meaning |
|---|---|
| `win_rate` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `stop_rate` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `expectancy` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `r_outcome` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `pip_outcome` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `max_intraday_reward` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `stop_streak` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |

## Storage Principle

If a field may later explain win rate, expectancy, stop behavior, overlap behavior, or model quality, it should be recorded from the beginning even if it is not used immediately.
