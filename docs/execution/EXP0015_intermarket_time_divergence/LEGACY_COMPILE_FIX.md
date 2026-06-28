# EXP0015 Legacy Compile Fix

This patch fixes compile errors triggered by the deprecated expert:

- `mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5`
- `mql5/Include/IntermarketDivergence/DAL_IMDReferenceLevels.mqh`

## Cause

The project had two EXP0015 API generations mixed together:

1. The current simple candle/session engine uses `IMD_*` types:
   - `IMD_LevelFamily`
   - `IMD_TriggerMode`
   - `IMD_Event`

2. The deprecated SPX/NDX expert and old reference-level module used older `DAL_IMD*` names:
   - `DAL_IMDLevelSide`
   - `DAL_IMDLevelSource`
   - `DAL_IMDTriggerMode`
   - `DAL_IMDReferenceLevel`

MetaEditor therefore reported errors such as `declaration without type`, `side - comma expected`, and undeclared `IMD_LEVEL_HIGH` or `IMD_LEVEL_L_NODE`.

## What the fix does

- Adds compile-compatible aliases and compatibility structs in `DAL_IMDTypes.mqh`.
- Extends `IMD_LevelFamily` with legacy node/day enum values so older inputs compile.
- Keeps the simple EXP0015 engine deterministic.
- Replaces the deprecated `IMD001_SPX_NDX_TimeDivergence.mq5` with a compile-safe legacy wrapper that uses the canonical candle/session engine.
- Leaves the canonical EXP0015 expert as:
  - `mql5/Experts/IntermarketDivergence/IMD001_CandleSessionDivergence.mq5`

## Recommended compile target

Use this file for current EXP0015 work:

```text
mql5/Experts/IntermarketDivergence/IMD001_CandleSessionDivergence.mq5
```

The old SPX/NDX file is now only a compatibility wrapper.

## Important limitation

The legacy wrapper does not restore the old structural-node divergence engine. If `IMD_LEVEL_L_NODE` is selected, the simple level engine falls back to a rolling-lookback proxy so old `.set` files do not break compilation.

For the STC SMT strategy, compile this separate expert instead:

```text
mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5
```
