---
title: RTHP MT5 Automation — Latest Closed M1 History Warm-up Hotfix
status: implemented
version: 1.0.1
updated: 2026-07-23
tags: [rthp, mt5, m1, hotfix, history-synchronization]
---

# Latest Closed M1 History Warm-up Hotfix

## Observed real-terminal failure

A real FxPro MT5 terminal exposed both requested symbols and returned closed M1 bars through `copy_rates_from_pos(symbol, TIMEFRAME_M1, 1, count)`, while the one-click adapter could still fail immediately after initialization with `MT5_NO_CLOSED_M1_BAR`.

## Root cause

The adapter queried position zero, which is the currently forming M1 bar, and performed no history warm-up retry before concluding that no closed bar existed. A terminal can expose the live bar before closed history is synchronized to the Python bridge.

## Corrected contract

1. Position zero is never used to establish the latest canonical closed M1 bar.
2. The adapter queries from position one, making the closed-bar boundary explicit.
3. The latest-bar probe uses the same bounded retry policy as historical range acquisition.
4. Every unsuccessful attempt records the returned row count and `last_error` evidence.
5. Failure remains fail-closed after the retry budget is exhausted.
6. No raw ticks, sub-M1 data, synthetic bars, trading authority, or Engine changes are introduced.

## Acceptance evidence

- Unit coverage proves position one is used.
- Unit coverage proves an empty warm-up response is retried and then succeeds.
- Existing M1-only and read-only boundaries remain unchanged.
