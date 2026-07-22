---
title: RTHP MT5 Automation — Test Strategy, Acceptance Matrix, and Definition of Done
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, testing, acceptance, definition-of-done]
---

# Test Strategy, Acceptance Matrix, and Definition of Done

## Unit tests

- terminal locator precedence;
- connection-health classification;
- symbol alias resolution;
- symbol ambiguity rejection;
- UTC/M1 normalization;
- OHLC validation;
- incomplete-bar exclusion;
- M1 touch interval semantics;
- gap taxonomy;
- hash and run-ID determinism.

## Contract tests

- MetaTrader adapter schema;
- M1 source schema;
- symbol metadata schema;
- source-binding schema;
- quality-report schema;
- run-config schema;
- no-trade capability manifest.

## Integration tests

- fake MT5 provider to complete source freeze;
- two-symbol history with DST transitions;
- holiday and early-close cases;
- differing symbol sessions;
- missing and conflicting chunks;
- restart/resume;
- M1-to-RTHP materialization;
- one-shot smoke train;
- immutable run verification.

## Parity and regression

- existing RTHP Context tests remain unchanged and pass;
- existing AI-input tests pass;
- existing train-activation tests pass;
- central-engine snapshot unchanged;
- canonical Context snapshot unchanged.

## Definition of done

The delivery is complete when:

1. the operator can select only two valid symbols;
2. the terminal and common M1 history are resolved automatically;
3. sub-M1 data is never requested for canonical mode;
4. quality gates classify all gaps;
5. immutable source artifacts and binding are produced;
6. RTHP Train Activation completes automatically;
7. run verification passes;
8. no central engine or canonical Context file changed;
9. no trading authority exists.
