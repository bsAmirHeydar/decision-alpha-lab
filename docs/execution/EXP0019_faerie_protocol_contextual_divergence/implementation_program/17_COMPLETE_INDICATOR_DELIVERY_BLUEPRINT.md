---
title: "Complete Indicator Delivery Blueprint"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Complete Indicator Delivery Blueprint

## Product objective

Deliver a complete multi-symbol Faerie Protocol indicator suitable for historical study, live discretionary use, debugging, and semantic parity verification with future EAs.

## Indicator build layers

```text
Layer 1 — Product shell and lifecycle
Layer 2 — Semantic snapshot/event subscription
Layer 3 — Projection model and object identity
Layer 4 — Session/reference/hunt/signal/WW visuals
Layer 5 — Panel, filters, modes, alerts, export
Layer 6 — replay, restart, performance, multi-chart release
```

## Screen composition

### Chart canvas

- Session boxes for A/L/N.
- Week separators/ranges.
- Reference high/low lines and labels.
- Hunter/Protected markers.
- Relation connector and confirmation marker.
- Suppression/neutralization overlays.
- Entry eligibility or quota-winner badge.

### Context panel

- Pair and instance identity.
- NY date/session/week and DST state.
- Host confirmation timeframe.
- Data health for both symbols.
- Active WW direction, source, age, and state.
- Session quota state and first-signal winner.
- Last confirmed signals with relation/direction/reason.
- Open-policy warning for live quota consumption.

### Filter controls

- Mode: Audit, Trading Clean, WW Focus, Relation Focus, Diagnostic.
- Relation toggles: AL, AN, LN, NA, NL, NN, WW.
- Direction toggles.
- Lifecycle-state toggles.
- Session/reference/label/history visibility.
- Panel page and compact/expanded state.

## Rendering contract

The indicator receives immutable snapshots and semantic events. It creates a `ProjectionRecord` for each visible semantic entity. Projection records contain geometry/style/object IDs but never alter signal state.

## Complete indicator acceptance scenarios

1. Attach to Symbol A; both symbols synchronize and all enabled contexts render.
2. Attach a second instance with a different configuration; no object or alert collision occurs.
3. Change chart timeframe; detection ledger remains identical while geometry reprojects.
4. Restart terminal; semantic IDs and projection inventory rebuild identically.
5. Repair missing history; affected windows re-evaluate with data-revision evidence.
6. Generate a signal opposed to WW; raw signal remains visible with suppression style.
7. Generate several same-session signals; earliest M1 Hunt winner is marked and later signals remain visible.
8. Rebuild history; no stale popup/push/email alerts are emitted.
9. Switch filters/modes; only projection state changes.
10. Export ledger; all fields reconcile with indicator visuals and engine events.

## Release artifacts

- Compiled `.ex5` and source patch.
- Default `.set` profiles for Audit, Trading Clean, WW Focus, and Diagnostic.
- User guide and input reference.
- Golden replay fixture set.
- MetaEditor logs and Strategy Tester reports.
- Performance and object inventory report.
- Known limitations and rollback instructions.
