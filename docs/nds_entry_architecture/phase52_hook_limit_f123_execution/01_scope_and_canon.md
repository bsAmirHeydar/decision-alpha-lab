---
title: Phase 52 Scope and Canon
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Scope and Canon

## Accepted source families

A sequence may enter this profile only when it is already a canonical valid Hook and belongs to at least one of these families:

- `HH`: valid Hook-after-Hook child;
- `F3H`: valid Hook after an opposing F3;
- `F3H+HH`: dual-qualified Hook satisfying both contracts.

The parent companion of an HH chain is context only. It is never promoted into a separate entry source.

## Eligibility gate

```text
sequence.valid = true
sequence.valid_hook_family = true
sequence.hook_failed = false
family ∈ {HH, F3H, F3H+HH}
cycle closed when RequireClosedHook = true
resolve_price > 0
origin/death boundary > 0
```

Generic Hooks, research-only geometric candidates, invalid companions, and raw display objects are excluded.

## Direction contract

For this execution profile only:

```text
positive Hook → bullish trade → Buy Limit
negative Hook → bearish trade → Sell Limit
```

This is an explicit Phase 52 execution contract. It does not silently modify the general Phase 51 direction-policy scaffold.

## Selection policy

When the strategy is idle, the most recently resolved eligible Hook is selected. If that Hook has already consumed its one allowed attempt, the engine does not fall back to an older stale Hook.

## Non-goals

Phase 52 does not define:

- the universal NDS Zone boundary model;
- multi-zone ranking;
- simultaneous portfolio execution;
- scale-in or partial entry;
- fixed take-profit logic;
- re-entry on the same Hook after cancellation or stop-out.
