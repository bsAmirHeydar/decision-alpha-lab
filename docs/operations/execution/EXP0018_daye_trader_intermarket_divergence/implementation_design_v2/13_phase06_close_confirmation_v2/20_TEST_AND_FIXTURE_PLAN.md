---
id: EXP0018-P06-TESTS
title: "P06 Test and Fixture Plan"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Required scenarios

- A-only HIGH survives through close;
- B-only LOW survives through close;
- one-sided becomes BOTH;
- one-sided becomes NONE;
- source unavailable at close;
- source not available through close;
- role changes;
- host identity mismatch;
- missed close;
- simultaneous HIGH and LOW;
- multiple relationships in one candle;
- duplicate callback;
- fresh attach baseline;
- restart before close;
- result identity determinism.

Embedded MQL5 tests cover pure outcomes. Python fixtures independently validate the outcome table and authority boundaries.
