# NDS F2 Overlap-Wider and Minimum-RR Entry Repricing — Audit Report

## Scope

This patch modifies only the dedicated lightweight F2 Waist-Break Point-2 Strategy Tester profile.

It preserves the canonical setup:

```text
Complete unconfirmed F2 two-leg body
→ Point 1 = F2 Waist
→ pending Point 2 beyond the Waist
→ Stop behind direct parent F1 Waist
→ Target at F2 Leg2 endpoint
```

No Hook, Zone, F3, CG, AI, renderer, CSV, timer, or runtime print path is added.

## Requested decisions implemented

### 1. Near-identical overlapping trades

Same-direction setups are compared by their final executable stop corridors:

```text
Stop Corridor = interval between Entry and Stop
Width = abs(Entry - Stop)
Overlap % = intersection length / narrower corridor width × 100
```

Default contract:

```text
Overlap deduplication = enabled
Threshold = 80%
Winner = wider final executable stop corridor
```

The threshold is an input. Setting it to `70.0` makes the merge rule more aggressive.

Opposite-direction contexts are excluded from this deduplication rule so the explicit hedge policy remains intact.

### 2. Wider-context arbitration

- Same-bar candidates are all built before any order is sent.
- When overlap is at or above the threshold, the narrower candidate is suppressed.
- Equal widths keep the earlier deterministic candidate to avoid churn.
- A wider new setup replaces a narrower still-pending order.
- An already-filled overlapping position is not closed or replaced.

### 3. Minimum-RR entry repricing

The existing structural Stop and Target remain fixed.

If the initial limit behind F2 Waist is below the configured minimum RR, only Entry is moved farther behind the Waist toward Stop:

```text
Entry* = (Target + MinimumRR × Stop) / (1 + MinimumRR)
```

- Bullish setup: round Entry down to tick.
- Bearish setup: round Entry up to tick.
- This rounding is toward Stop and therefore cannot reduce RR below the request.
- Final geometry, broker stop-distance rules, true limit-order geometry, and final RR are revalidated.
- If no broker-valid adjusted limit exists, the setup is rejected.

Defaults:

```text
Use minimum RR filter = true
Adjust Entry to minimum RR = true
Minimum RR = 1.0
```

## New inputs

```text
InpF2BTAdjustEntryToMinimumRewardRisk = true
InpF2BTUseStopSpaceOverlapDeduplication = true
InpF2BTStopSpaceOverlapThresholdPercent = 80.0
```

Existing inputs remain authoritative:

```text
InpF2BTMinimumRewardRisk
InpF2BTAllowOppositeDirectionHedge
InpF2BTAllowSameDirectionMultipleContexts
InpF2BTMaxConcurrentManagedExposures
```

## Execution ordering

```text
Build structural setup
→ normalize Stop / Target / structural Entry
→ reprice Entry when RR is insufficient
→ recompute final executable RR
→ same-bar stop-corridor arbitration
→ inspect existing pending/positions
→ apply effective exposure policy after planned replacements
→ OrderCheck
→ delete narrower replacement pendings
→ OrderCheck again
→ OrderSend
```

## Safety boundaries

- Existing live positions are never closed for wider-context replacement.
- Exact-context one-attempt identity remains active.
- Opposite-direction hedge contexts are not merged by same-direction overlap logic.
- Netting-account restrictions remain unchanged except that a wider pending may replace a narrower pending before fill.
- Stop and Target are never moved to manufacture RR.
- No market-order fallback is introduced.

## Versions

```text
Expert version: 1.40
Trade contract: NDS-F2-WAIST-BREAK-05
Schema: nds_f2_waist_break_point2_v5
```

## Validation completed

```text
NDS F2 Point-2 contract QA: PASS
NDS F2 fast backtest QA: PASS
NDS F2 RR / parallel-context QA: PASS
NDS F2 overlap-wider / RR-reprice QA: PASS
Engineering policy: 0 errors, 0 warnings
MQL5 compatibility: 0 errors, 0 warnings
Repository layout: 0 missing directories
AI Engineering OS vault: 0 errors, 0 warnings
Changed MQL lexical balance: PASS
Changed include resolution: PASS
```

MetaEditor and Strategy Tester were not available in the patch-building environment. Final compilation and Real-Tick execution must be confirmed locally.
