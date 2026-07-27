---
id: UCPS-E2B94F6170AD
title: "UC04-W1B Authority and Safety Boundary"
type: authority-record
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - w1b
  - safety
  - authority
---
# UC04-W1B Authority and Safety Boundary

## Explicitly permitted

- native compilation of frozen test and consumer sources in an isolated mirror;
- execution of one test-only script with live trading and DLL import disabled;
- immutable evidence capture under `.alpha/runs`;
- deterministic independent evidence review;
- generation of a cutover candidate outside production repository paths.

## Explicitly forbidden

- production include materialization in the tracked repository;
- modification of the ten consumer files;
- deletion of any local helper;
- changes to Entry, Treatment, Execution, Stop, Target, Risk, Context, feature, label, model, or Train semantics;
- order placement, position modification, network access, market-data dependence, chart-object mutation, or capital authority;
- automatic Git staging, commit, or push by the native runner;
- applying a generated candidate before post-cutover native qualification and final review.

## Exit status

The tooling delivery is accepted while native execution remains pending on the local Windows/MT5 host. W1B-Q therefore advances capability without claiming evidence that cannot be produced in the repository build environment.

## Navigation

- [[01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/15_UC04_W1B_NATIVE_QUALIFICATION/00_MOC|W1B records MOC]]
