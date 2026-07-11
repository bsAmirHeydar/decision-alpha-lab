---
type: strategy-factory-document
status: canonical
title: "Leakage and Contamination Audit"
tags:
  - strategy-factory
---

# Leakage and Contamination Audit

Leakage is tested structurally, not inferred from suspiciously high performance.

## Leakage classes

Future bars, completed-session aggregates, eventual object validity, outcome-derived ranks, full-history normalization, target encoding outside train, overlapping labels across folds, duplicate events across files, and human relabeling after outcomes.

## Detection

Feature-level known time, forbidden-name lists, schema lineage, fold purge audit, train-only transformers, source code review, and synthetic tests that shift outcomes while preserving inputs. Any unexplained predictive power after label permutation triggers quarantine.

## Contamination by selection

Choosing symbols, periods, sessions, or model settings after examining the same OOS period contaminates it even if code is causal. The trial registry and confirmation freeze handle this non-code leakage.

