# 10 — Reward/Risk and Parallel Context Policy

## 1. Purpose

This layer controls three independent questions without changing F1/F2 anatomy:

1. what minimum executable Reward/Risk is required;
2. whether a sub-threshold setup should be rejected or repriced;
3. whether independent same-direction and opposite-direction contexts may coexist.

## 2. Reward/Risk contract

```text
Risk Distance   = abs(Entry - Stop)
Reward Distance = abs(Target - Entry)
Reward/Risk     = Reward Distance / Risk Distance
```

Defaults:

```text
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTAdjustEntryToMinimumRewardRisk = true
InpF2BTMinimumRewardRisk = 1.0
```

Stop and Target are structural authorities and are not moved. If the original limit behind the F2 Waist is below the threshold, only Entry is moved farther behind the Waist toward Stop.

The exact minimum-RR boundary is:

```text
Entry* = (Target + MinimumRR × Stop) / (1 + MinimumRR)
```

Bullish Entry is rounded down and bearish Entry is rounded up to the symbol tick. The result is verified again after normalization. If the price is not a valid limit or fails broker stop-distance rules, the setup is rejected.

## 3. Context identity

A context is the exact F2 body version identified by symbol, timeframe, direction, scale, parent F1 Waist, F2 Origin, F2 Waist and F2 Leg2 endpoint. This creates a deterministic `setup_hash`.

The hash prevents resubmitting the exact same context, but near-duplicate arbitration may also merge different hashes whose executable risk spaces are practically the same.

## 4. Same-direction parallel contexts

```text
InpF2BTAllowSameDirectionMultipleContexts = true
```

Independent same-direction contexts remain allowed when their stop corridors do not meet the duplicate-overlap threshold.

## 5. Opposite-direction hedge contexts

```text
InpF2BTAllowOppositeDirectionHedge = true
```

Bullish and bearish contexts may coexist. The overlap-deduplication rule is deliberately same-direction only and does not cancel an authorized hedge.

## 6. MT5 account-mode boundary

Independent same-symbol positions require `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING`. Netting and exchange accounts cannot preserve per-context Stop/Target ownership, so a second same-symbol exposure is blocked.

## 7. Optional portfolio cap

```text
InpF2BTMaxConcurrentManagedExposures = 0
```

Zero means no strategy-level numerical cap. A positive value caps managed pending orders and positions on the current symbol.

## 8. Interaction with wider-context arbitration

Overlap arbitration is evaluated before ordinary concurrency permission. Therefore a wider same-direction candidate can replace a narrower pending order even when same-direction multiple contexts are disabled or the account is netting. An open position is never replaced.
