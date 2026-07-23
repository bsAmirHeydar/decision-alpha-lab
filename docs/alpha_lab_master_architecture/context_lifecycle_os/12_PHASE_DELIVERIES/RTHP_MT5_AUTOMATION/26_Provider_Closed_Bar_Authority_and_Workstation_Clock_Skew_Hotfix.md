---
title: Provider Closed-Bar Authority and Workstation Clock-Skew Hotfix
status: implemented-and-regression-tested
version: 1.0.2
updated: 2026-07-23
tags: [rthp, mt5, m1, closed-bar, clock-skew, hotfix]
---

# Provider Closed-Bar Authority and Workstation Clock-Skew Hotfix

## Incident

The direct MetaTrader 5 probe returned valid rows from `copy_rates_from_pos(symbol, TIMEFRAME_M1, 1, count)`, while the adapter still raised `MT5_NO_CLOSED_M1_BAR` after bounded history synchronization retries.

## Root cause

Adapter version 1.0.1 correctly requested position one but then compared each returned bar-open timestamp with the workstation wall clock. A terminal, broker feed, or workstation clock-offset disagreement could therefore cause a valid provider-closed bar to be reclassified as not closed.

That second classification was invalid. MetaTrader bar indexing already defines position zero as the current bar and position one as the immediately preceding bar. The RTHP adapter must use the provider index contract as the closed-bar authority for this probe rather than a separate workstation-clock judgment.

## Corrective behavior

1. Request only `TIMEFRAME_M1` bars beginning at position one.
2. Keep the bounded warm-up retry policy.
3. Treat valid timestamped rows returned from position one as closed by provider contract.
4. Compute the latest common acquisition end from the minimum provider-closed end across both symbols.
5. For explicit UTC ranges, cap the requested end at the provider-derived latest common closed end.
6. Do not cap automatic or explicit history with the workstation wall clock.
7. Continue to materialize each M1 bar as known only at its bar-close timestamp.
8. Continue to reject raw ticks, sub-M1 canonical inputs, the position-zero forming bar, synthetic tick reconstruction, and intrabar ordering inference.

## Regression coverage

The regression suite includes:

- bounded history warm-up retry;
- explicit use of position one;
- a workstation clock deliberately behind provider bar timestamps;
- provider-derived automatic range resolution;
- the full RTHP MT5, Train Activation, AI Input, Context, onboarding, ACL-02, and ACL-03 relevant suite.

## Authority boundary

This hotfix changes only the context-owned RTHP MT5 adapter, its registration, tests, and documentation. It does not modify the central Engine or Canonical RTHP Context and does not create Entry, Treatment, Execution, order, or capital authority.
