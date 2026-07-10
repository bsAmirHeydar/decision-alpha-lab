# Phase 06 Hotfix010 — Validation Plan

## Required default inputs

```text
InpSymbolA = SPXUSD
InpSymbolB = NDXUSD
InpRequireM1History = true
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpSuppressNonFrontierReferenceSignals = true
InpEnableHistoricalVisualBackfill = true
InpClearPhase06ObjectsOnInit = true
InpDrawOnBothInputSymbolCharts = true
```

Run the expert only on `SPXUSD`. Keep `NDXUSD` open without a second expert instance.

## Test 1 — cold non-host history

1. Close the NDX chart and clear/reload symbol history if practical.
2. Attach the expert to SPX.
3. Observe the journal during initial loading.

Expected:

```text
historical backfill waiting for complete M1 coverage on both configured symbols
```

No partial backfill should be finalized. Once NDX history becomes complete, the expert should clear owned objects and perform one authoritative replay.

## Test 2 — chart parity

After backfill completes:

1. choose several visible SPX divergence lines;
2. locate their NDX companion legs by reference time and destination time;
3. verify that every displayed pair uses the same CG, reference cycle, side, and confirmation observation;
4. verify that no line exists only because NDX history was partial.

Expected:

- strict accepted signals draw on both charts;
- rejected stale references draw on neither chart;
- attaching the expert to SPX does not weaken NDX rules.

## Test 3 — consumed NDX high

Construct or locate a case where:

1. an older NDX reference high exists;
2. a later completed cycle makes an equal or higher NDX high;
3. a still later current cycle appears to produce one-sided behavior against the old pair.

Expected:

- the old NDX high is non-frontier;
- the pair signal is suppressed in strict mode;
- neither SPX nor NDX receives a divergence line from that reference.

## Test 4 — consumed NDX low

Repeat Test 3 for an older NDX low followed by an equal or lower later low.

Expected:

- the old NDX low is suppressed;
- no pair signal and no chart line are created.

## Test 5 — missing intervening interval

Temporarily create a history gap or test while NDX history is still loading.

Expected:

```text
missing newer cycle => older references remain unproven
```

The classifier must not skip the gap and must not promote older levels to fresh frontier status.

## Test 6 — exclusive boundary

Inspect a reference or current interval whose extreme occurs close to the next minute boundary.

Expected:

- price aggregation excludes the bar opening exactly at the interval end;
- exact origin/destination timestamps also exclude that next-interval bar;
- price and visual timestamp describe the same interval.

## Test 7 — reattach reconstruction

1. leave old Phase 06 objects on both charts;
2. reattach version 1.10;
3. wait for the dual-symbol preflight and replay.

Expected:

- all `EXP0017_P06_` objects are cleared before replay;
- unrelated manual drawings remain untouched;
- the rebuilt NDX chart contains no remnants from previous versions.

## Compile gate

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Required MetaEditor result:

```text
0 errors, 0 warnings
```

## Repository gates

Run:

```powershell
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
python docs/ai_algorithm_engineering_os/tools/validate_vault.py
```
