# EXP0017 Chapter 15 — Statistical Reporting and Metric Language

> English knowledge-base version of the Strategy Architect doctrine. This document preserves the base doctrine while making the project readable for English implementation, review, collaboration, and future modeling.

## Metric / Field Catalog

| Field | Meaning |
|---|---|
| `primary_sample_flag` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `cg_type` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `risk_reward` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `pip_outcome` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `daily_range_normalized_pip` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |
| `signal_frequency` | Must be preserved when relevant so the future statistical layer can rank and compare signal families. |

## Storage Principle

If a field may later explain win rate, expectancy, stop behavior, overlap behavior, or model quality, it should be recorded from the beginning even if it is not used immediately.
