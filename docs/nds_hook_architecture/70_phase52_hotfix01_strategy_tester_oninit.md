---
title: Phase 52 Hotfix 01 - Strategy Tester OnInit License Gate
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Hotfix 01 — Strategy Tester OnInit License Gate

## Symptom

```text
tester stopped because OnInit returns non-zero code 1
```

## Root cause

`OnInit()` had one failure return: the offline license gate. The gate was
hard-coded enabled, account-bound, server-bound, password-bound, expiry-bound,
and hidden-gate-bound. Default tester inputs contain no signed token, so token
parsing failed and `INIT_FAILED` was returned before `FP_Run()`.

## Change

The EA now detects tester authority through MQL runtime properties and supports
an explicit tester/optimization bypass. The bypass is evaluated before the
signed live-license path and produces a complete positive runtime report for
downstream safety gates.

## Non-change

- no Hook rule changed;
- no limit-entry rule changed;
- no F123 exit rule changed;
- no live license rule was weakened;
- no order-send input default changed.

## Version

```text
FlagCountingPhoenixExperiment.mq5 = 18.41
```
