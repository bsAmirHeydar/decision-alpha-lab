# NDS F2 Higher-Timeframe F-Phase Filter — Audit Report

## Patch identity

```text
Patch: NDS-F2-HTF-F-PHASE-FILTER-01
Expert: NDSF2WaistLimitBacktest.mq5
Expert version: 1.60
Trade contract: NDS-F2-WAIST-BREAK-07
Schema: nds_f2_waist_break_point2_v7
Date: 2026-07-12
```

## Requested behavior

The entry-timeframe F2 Waist-Break Point-2 setup must be directionally authorized by a higher-timeframe canonical structural phase.

```text
HTF bullish F → Buy only
HTF bearish F → Sell only
HTF Hook/ND → no new trade
```

The default higher timeframe is H1.

## Implemented architecture

A dedicated module was added:

```text
FP_NDSF2HigherTimeframePhaseFilter.mqh
```

Its pipeline is:

```text
closed HTF bars
→ canonical Phoenix node/F1/F2/F3/Hook detection
→ latest canonical F selection
→ latest Hook/ND selection
→ F-versus-Hook phase arbitration
→ allowed entry direction
```

The lower-timeframe setup detector remains the lightweight F1/F2-only engine. The full F/Hook pass is isolated to the configured higher timeframe and cached by the higher-timeframe open-bar timestamp.

## Phase arbitration

The filter selects the latest visible canonical F event by:

1. latest observable anatomy timestamp;
2. final canonical rank;
3. ownership rank;
4. F level;
5. scale;
6. event id.

It then compares the latest visible Hook/ND timestamp:

```text
Hook/ND time >= F time → Hook/ND phase → gate closed
F time > Hook/ND time → F phase → direction inherited from F
```

Equal-time evidence is fail-closed.

## Entry authorization

The trade core now receives two explicit values:

```text
entry_direction_gate_open
allowed_entry_direction
```

Candidate F2 setups are rejected before setup construction when:

- the HTF gate is closed;
- the candidate direction differs from the HTF F direction.

The HTF gate is upstream of RR repricing, overlap arbitration, hedge policy and broker submission.

## Pending-order reconciliation

Default:

```text
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

Behavior:

- bullish HTF F cancels managed Sell pending orders;
- bearish HTF F cancels managed Buy pending orders;
- Hook/ND, no-F, ambiguous or data-not-ready cancels all managed pending orders.

Open positions are not force-closed. They retain their original Stop and selected fixed-F2 or F3-retest exit mode.

## Dynamic-exit continuity

When an open position uses the dynamic F3-retest exit, the lower-timeframe F2 stream continues to run even if the HTF gate later closes. This preserves confirmation-node discovery and exit management while still preventing new entries.

## Inputs

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

The first version deliberately keeps the internal HTF history and scale profile fixed:

```text
requested closed bars = 900
minimum closed bars = 180
scales = 2, 3, 5, 8, 13
max events = 2400
max hooks = 2400
```

This avoids adding unnecessary optimization dimensions before profiling evidence exists.

## Closed-bar and leakage contract

- The live HTF candle is excluded.
- The snapshot updates only on a new HTF bar.
- Missing HTF history blocks entries and retries on later lower-timeframe cycles.
- No future F or Hook information is consulted.

## Performance impact

Entry-timeframe runtime remains:

```text
new LTF bar → lightweight canonical F1/F2 detector
```

Higher-timeframe runtime is:

```text
new H1 bar only → full canonical F/Hook classifier
```

There are no new runtime prints, CSV files, chart objects, timers or per-tick structural scans.

## Unchanged contracts

The patch does not change:

- F2 Point-2 Entry geometry;
- F1-waist Stop;
- fixed F2-end exit;
- dynamic F3-retest exit;
- minimum RR and Entry repricing;
- stop-corridor overlap and wider winner;
- same-direction multiple-context policy;
- hedge account requirements;
- position sizing.

## Validation completed

```text
NDS F2 HTF F-phase contract QA: PASS
NDS F2 dual-exit regression QA: PASS
NDS F2 overlap/RR regression QA: PASS
NDS F2 parallel-context regression QA: PASS
NDS F2 fast-backtest regression QA: PASS
NDS F2 Point-2 regression QA: PASS
Engineering policy: 0 errors, 0 warnings
MQL5 compatibility: 0 errors, 0 warnings
Repository layout: 0 missing directories
AI Engineering OS vault: 0 errors, 0 warnings
Python syntax: PASS
MQL lexical balance: PASS
Changed-file include resolution: PASS
New-document links: PASS
```

## Compile limitation

MetaEditor is not installed in the patch-build environment. Final compilation and Strategy Tester execution must be confirmed locally.
