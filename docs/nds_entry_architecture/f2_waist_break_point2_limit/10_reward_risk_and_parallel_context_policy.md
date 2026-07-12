# 10 — Reward/Risk and Parallel Context Policy

## 1. Purpose

This extension adds two independent controls to the canonical F2 Waist-Break Point-2 setup:

1. a minimum reward-to-risk eligibility filter;
2. explicit permission for independent same-direction and opposite-direction contexts.

Neither control changes the anatomical definition of the setup.

## 2. Reward/Risk contract

The ratio is calculated only after Entry, Stop and Target have been normalized to the symbol's executable tick size:

```text
Risk Distance   = abs(Entry - Stop)
Reward Distance = abs(Target - Entry)
Reward/Risk     = Reward Distance / Risk Distance
```

Default policy:

```text
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTMinimumRewardRisk = 1.0
```

Acceptance rule:

```text
Reward/Risk >= configured minimum → eligible
Reward/Risk < configured minimum  → reject
```

The ratio is a pure price-distance ratio. It does not add spread, commission or slippage to the threshold. Those remain part of the Strategy Tester execution result.

## 3. Context identity

A context is not merely a direction. It is the exact F2 body version identified by:

- symbol and timeframe;
- direction;
- scale L;
- direct parent F1 waist time;
- F2 origin time;
- F2 waist time;
- F2 Leg2 time and price.

This produces a deterministic `setup_hash`. Two opportunities are independent contexts only when their hashes differ.

The one-attempt registry continues to block a duplicate order from the same context.

## 4. Same-direction parallel contexts

Default:

```text
InpF2BTAllowSameDirectionMultipleContexts = true
```

When enabled, a new bullish setup may be submitted while another bullish order or position from a different context exists. The bearish side is symmetric.

When disabled, the first active exposure in that direction blocks later contexts until it is removed or closed.

## 5. Opposite-direction hedge contexts

Default:

```text
InpF2BTAllowOppositeDirectionHedge = true
```

When enabled, a bullish context and a bearish context may coexist. Each retains its own Entry, Stop and Target.

When disabled, any active opposite-direction managed exposure blocks the new setup.

## 6. MT5 account-mode boundary

Independent same-symbol contexts require:

```text
ACCOUNT_MARGIN_MODE_RETAIL_HEDGING
```

On a netting or exchange account, MT5 merges or nets same-symbol positions. That destroys independent per-context Stop/Target ownership. Therefore:

```text
First managed exposure → allowed
Second same-symbol context → blocked on non-hedging accounts
```

The strategy does not silently emulate hedging on a netting account.

## 7. Optional portfolio cap

```text
InpF2BTMaxConcurrentManagedExposures = 0
```

`0` means no strategy-level numerical cap. Positive values set a hard maximum across managed pending orders and positions on the current symbol.

## 8. Pending-order lifecycle under parallel contexts

Each pending order is evaluated independently. If its own F2 Leg2 target is touched before fill, only that pending order is cancelled. Other contexts remain active.

## 9. Deterministic selection order

When several new contexts become observable on the same closed bar, they are processed in this order:

1. newest observability bar;
2. newest F2 Leg2;
3. newest F2 origin;
4. smaller scale L;
5. larger event id.

This ordering matters only when a concurrency switch or maximum-exposure cap blocks some candidates.
