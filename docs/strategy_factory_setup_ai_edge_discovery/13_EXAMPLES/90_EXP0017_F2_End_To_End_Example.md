---
id: SAED-FB176CA942
title: "Example — EXP0017 F2 Context End-to-End"
type: example
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - example
  - exp0017
---

# Example — EXP0017 F2 Context End-to-End

## 1. Context Input

```text
Bullish F2
+ higher-timeframe phase aligned
+ fresh protected reference
+ liquidity hunt complete
+ confirmation window open
```

## 2. Setup Archetypes

- immediate continuation;
- breakout expansion;
- waist pullback;
- point-2 retest;
- close confirmation/reclaim.

## 3. Initial Controlled Universe

Use one canonical structural stop/invalidator where possible to isolate Entry effects, then expand:

| Candidate | Profile | Entry | Exit |
|---|---|---|---|
| C01 | P1 | Market | fixed 1.2R |
| C02 | P1 | Waist Limit | fixed 1.2R |
| C03 | P2 | Breakout | structural destination |
| C04 | P2 | Point-2 Limit | structural destination |
| C05 | P3 | Breakout | structural trail |
| C06 | P4 | Market | open trail |
| C07 | P5 | Waist Limit | fixed 1.1R |
| C08 | P5 | Close Confirmation | fixed 1.1R |
| C09 | — | Skip | — |

## 4. Outcome Cube

For every F2 occurrence replay all compatible candidates with side-aware bid/ask, spread, commission, slippage, order expiry, Context expiry and path-accurate trail state.

## 5. Dataset

One row per occurrence/candidate, clustered by occurrence. Features include F lifecycle, HTF phase, hunt/reference geometry, volatility, session, spread, entry distance, stop distance, remaining confirmation time and Treatment descriptors.

## 6. Trainer Ladder

1. Manual policy.
2. Unconditional candidate means.
3. Trade/skip logistic model.
4. Fill model for limit candidates.
5. Net-R/quantile models.
6. Grouped ranker.
7. Treatment selector.
8. Survival/trail challenger.
9. Regime/multi-view challengers only if earned.

## 7. Anti-Overfit

Clustered walk-forward, purge/embargo, complete trial universe, matched non-F2/session-volatility nulls, direction/time shifts, cost/delay stress, best-F2-cluster removal, profile-specific tests and frozen paper challenge.

## 8. Policy

Manual eligibility can remain authoritative while AI ranks only allowed candidates. If OOD, small ranking margin, stale F2 or cost failure: fallback to Manual or Skip.

## 9. Success Definition

Success is not necessarily a promoted trade. A trustworthy result may show that only one profile works, that Manual is unbeatable, or that F2 carries no exploitation edge under executable costs.
