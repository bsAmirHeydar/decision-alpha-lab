---
id: UCPS-284DEA54A4DE
title: "Data Integrity, Known-Time and Leakage Controls"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Data Integrity, Known-Time and Leakage Controls

## Data integrity

Every observation has source identity, event time, ingestion time, known time, revision state and quality flags. Source freezes and immutable batches prevent silent mutation.

## Leakage controls

Feature availability, label horizon, split embargo, cross-validation folds, final-test lock and post-selection exposure are machine-checked. A model cannot consume data not available at its decision time.

## Market edge cases

Closed-bar determination, DST, sessions, holidays, gaps, stale symbols, unsynchronized pairs, duplicate bars and feed revisions receive explicit fixtures.

## Fail-closed behavior

Missing simultaneous data cannot become a confirmed multi-symbol Context. Unknown clock semantics block materialization and training.
