# Hotfix009 Validation Plan

## Preconditions

- Open SPXUSD M1 and NDXUSD M1.
- Attach the expert to only one of them.
- Use the same two symbols in `InpSymbolA` and `InpSymbolB`.
- Keep `InpEnableExtremeFrontierReferenceFilter=true`.
- Keep `InpClearPhase06ObjectsOnInit=true`.
- Enable historical backfill for the screenshot window.

## Test 1 — baseline compile

Compile:

```text
EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Expected:

```text
0 errors
0 warnings
version 1.09
```

## Test 2 — non-host stale-object cleanup

1. Run the old build and leave its lines on both charts.
2. Compile and attach version 1.09 only on the host chart.
3. Inspect Object List on both charts.

Expected:

- old `EXP0017_P06_` objects are removed on both charts;
- only signals reconstructed by version 1.09 remain;
- no unrelated manual objects are deleted.

## Test 3 — local frontier asymmetry

Use a case where the selected reference is frontier-valid on one symbol and non-frontier on the other. This can be exposed by temporarily setting:

```text
InpRequireSymbolLocalFrontierForBothSymbols=false
```

Expected:

- pair-level signal behavior follows the input;
- the frontier-valid symbol may draw;
- the non-frontier symbol must not draw a local price leg;
- no stale clean-side companion line appears on the second chart.

Restore strict mode after the test:

```text
InpRequireSymbolLocalFrontierForBothSymbols=true
```

## Test 4 — strict dual-chart mode

With strict mode enabled, identify a valid divergence where both reference sides remain frontier-valid.

Expected:

- both charts receive their own symbol-local leg;
- hunter and clean roles correspond to the same signal ID;
- line times refer to the same reference/current-cycle event;
- prices use each chart's own symbol scale.

## Test 5 — reverse host chart

1. Remove the expert from SPXUSD.
2. Attach it to NDXUSD with the same inputs.

Expected:

The accepted signal set and symbol-local drawing set are unchanged. Host selection must not alter frontier eligibility.

## Test 6 — historical backfill

Restart with two trading days of backfill.

Expected:

- stale internal references are absent from both charts;
- non-host chart object count does not include remnants from the previous build;
- draw cap and first-visual retention still work.

## Test 7 — runtime regression

Verify:

- closed-candle refresh continues;
- ledger writes remain deduplicated;
- no orders are sent;
- no panel/text objects appear in minimal mode;
- no new journal cleanup warning appears under normal conditions.
