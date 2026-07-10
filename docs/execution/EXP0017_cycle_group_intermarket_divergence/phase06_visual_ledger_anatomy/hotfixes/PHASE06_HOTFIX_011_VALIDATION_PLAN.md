# Hotfix011 Validation Plan

## Required configuration

```text
InpSymbolA = SPXUSD
InpSymbolB = NDXUSD
InpRequireM1History = true
InpEnableExtremeFrontierReferenceFilter = true
InpRequireSymbolLocalFrontierForBothSymbols = true
InpSuppressNonFrontierReferenceSignals = true
InpDrawOnBothInputSymbolCharts = true
InpClearPhase06ObjectsOnInit = true
InpEnableHistoricalVisualBackfill = true
```

Run the EA only on SPXUSD. Keep NDXUSD open without a second EA instance.

## Test 1 — NDX high consumed before current cycle

1. Select an NDX reference high.
2. Confirm that a later M1 bar before the current cycle touches or exceeds it.
3. Create a later one-sided state that would previously draw from that old NDX high.

Expected:

- NDX high is classified stale;
- strict pair signal is suppressed;
- no corresponding SPX or NDX line is drawn.

## Test 2 — NDX low consumed before current cycle

Repeat Test 1 for a reference low.

Expected:

- equality or lower price consumes the NDX low;
- no pair signal or chart leg survives.

## Test 3 — SPX fresh, NDX stale

Create a case where SPX path remains below its old high but NDX path already touched its corresponding high.

Expected:

```text
SPX local high freshness = true
NDX local high freshness = false
pair high freshness = false
```

Neither chart may draw.

## Test 4 — symbol-order invariance

Run the same data twice:

```text
A=SPXUSD, B=NDXUSD
A=NDXUSD, B=SPXUSD
```

Expected: after normalizing names, the accepted/rejected reference set is identical.

## Test 5 — anchor parity

For one accepted signal, inspect the exact M1 timestamp of the local reference extreme and current-cycle extreme on both charts.

Expected: each line endpoint equals the timestamps stored by the detection layer. No foreign-chart re-query drift is allowed.

## Test 6 — cleanup

1. Leave old `EXP0017_P06_*` objects on both charts.
2. Remove and reattach the EA.

Expected:

- all owned objects are removed on both charts before replay;
- only Hotfix011-authorized lines reappear;
- manual drawings remain.

## Automated checks

Run:

```powershell
python research/exp0017_phase06/tests/test_hotfix011_raw_path_freshness.py -v
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
python docs/ai_algorithm_engineering_os/tools/validate_vault.py
```

MetaEditor compilation remains mandatory:

```text
0 errors, 0 warnings
```
