# NDS F2 Reward/Risk, Hedge and Parallel Contexts — Audit Report

## 1. Scope

This patch extends the dedicated lightweight F2 Waist-Break Point-2 Strategy Tester expert. It does not change the anatomical setup:

```text
complete unconfirmed F2 body
→ F2 Waist = Point 1
→ limit beyond F2 Waist = executable Point 2
→ Stop beyond direct parent F1 Waist
→ Target at F2 Leg2 endpoint
```

The extension adds:

1. configurable minimum Reward/Risk filtering;
2. opposite-direction hedge contexts;
3. same-direction independent contexts;
4. optional maximum concurrent managed exposures;
5. multi-pending target-consumption reconciliation;
6. account-mode protection for independent context ownership.

## 2. Reward/Risk contract

The filter uses normalized executable prices:

```text
risk_distance   = abs(entry - stop)
reward_distance = abs(target - entry)
reward_risk     = reward_distance / risk_distance
```

Inputs:

```text
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTMinimumRewardRisk = 1.0
```

A setup is rejected before volume calculation and `OrderCheck` when:

```text
reward_risk < configured minimum
```

The filter is based on structural price distance. Tester spread, commission and slippage remain reflected in realized results, not in this pre-trade ratio.

## 3. Context identity

A context is the exact F2 body version. Its hash includes:

- symbol;
- timeframe;
- direction;
- scale L;
- parent F1 waist time;
- F2 origin time;
- F2 waist time;
- F2 Leg2 time and price.

This provides two guarantees:

```text
same hash      → no duplicate submission
new body hash  → independent context
```

Broker comments now include a short hash suffix for tester traceability.

## 4. Parallel exposure policy

Inputs:

```text
InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
InpF2BTMaxConcurrentManagedExposures = 0
```

`0` means no strategy-level numerical cap.

### Same direction

When enabled, a new bullish context may coexist with existing bullish contexts. Bearish behavior is symmetric.

### Opposite direction

When enabled, bullish and bearish contexts may coexist as independent positions/orders.

### One-attempt rule

Parallel permission never disables one-attempt-per-context. The exact same F2 body hash cannot submit twice.

## 5. MT5 account-mode authority

Independent same-symbol Stop/Target ownership is only possible in:

```text
ACCOUNT_MARGIN_MODE_RETAIL_HEDGING
```

On netting or exchange accounts, a second same-symbol exposure is blocked. This is deliberate: silently allowing MT5 to merge positions would invalidate independent context accounting and could overwrite Stop/Target ownership.

## 6. Candidate processing

The previous single latest-candidate selector is retained as a compatibility wrapper, but executable processing now collects all eligible contexts.

Deterministic priority:

1. newest observability index;
2. newest Leg2 anchor;
3. newest origin anchor;
4. smaller scale L;
5. larger event id.

Priority affects outcomes only if concurrency is disabled or the configured cap is reached.

## 7. Pending lifecycle

The previous one-pending fast path was generalized:

- every managed pending order is checked independently;
- when its own TP/F2 Leg2 is consumed before fill, only that order is removed;
- other pending orders and positions remain active.

## 8. Performance contract

The expert still:

- runs only once per new bar;
- uses the F1/F2-only fast detector;
- excludes Hook, F3, Zone, CG, AI, renderer, CSV and timer paths;
- emits no custom `Print` or `PrintFormat` output.

When another context cannot legally be added—because the account is non-hedging, the cap is reached, or both parallel switches are disabled—the detector rebuild is skipped and the old ultra-light hold path is used.

When parallel contexts are possible, the detector must run once per new closed bar to discover new contexts while positions or pending orders exist.

## 9. Version changes

```text
Expert version: 1.20 → 1.30
Trade contract: NDS-F2-WAIST-BREAK-03 → NDS-F2-WAIST-BREAK-04
Schema: nds_f2_waist_break_point2_v3 → nds_f2_waist_break_point2_v4
```

## 10. Validation completed

```text
NDS F2 waist-break Point-2 contract QA: PASS
NDS F2 fast backtest contract QA: PASS
NDS F2 RR / parallel-context contract QA: PASS
Engineering policy: 0 errors, 0 warnings
MQL5 compatibility scan: 0 errors, 0 warnings
Repository layout: 0 missing directories
AI Engineering OS vault: 0 errors, 0 warnings
Python QA syntax: PASS
Local include resolution: PASS
MQL lexical balance: PASS
Runtime no-print/no-file/no-object guards: PASS
```

## 11. Validation not available in this environment

MetaEditor and MT5 Strategy Tester were not available. The user must confirm:

- `0 errors, 0 warnings` in MetaEditor;
- order coexistence on an MT5 hedging test account;
- second-exposure blocking on a netting test account;
- RR threshold boundaries at `0.99`, `1.00`, and `1.01`-like geometries;
- per-order SL/TP ownership under same-direction and opposite-direction concurrency.
