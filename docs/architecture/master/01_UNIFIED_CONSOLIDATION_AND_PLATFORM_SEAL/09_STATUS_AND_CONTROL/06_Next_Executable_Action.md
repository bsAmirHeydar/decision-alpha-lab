---
id: UCPS-FDC2715C3BC7
title: "Next Executable Action"
type: action
status: active
domain: unified-consolidation-platform-seal
version: 1.1.0
created: 2026-07-23
updated: 2026-07-27
tags:
  - consolidation
  - platform-seal
---
# Next Executable Action

## Action

Execute `UC04-W1 — Deterministic MQL5 Formatting Primitive`.

## First bounded delivery

The W1 patch must create:

1. a repository-wide inventory of numeric and structured formatting implementations and consumers;
2. source digest and exact-output fixture freeze;
3. a canonical primitive with explicit precision, decimal, sign, null and locale contracts;
4. byte-exact differential and metamorphic tests;
5. a logic-preservation certificate;
6. a bounded consumer cutover plan and rollback proof;
7. an updated capability migration ledger row;
8. W1 QA, release and handoff controls.

## Explicit exclusions

W1 does not consolidate clocks, sessions, state streams, reference lifecycles, chart-object ownership, order-capable code or trading semantics. It does not delete existing helpers.

## Completion signal

W1 may close only when the canonical primitive is equivalent on the accepted fixture corpus, all migrated consumers pass, legacy-use counts are explicit and no deletion authority is exercised.
