# Phase 14 Validation Plan

## Static contract checks

- Protected symbol remains the default trade leg.
- Only `cg_3m` defaults enabled.
- ATR(14) × 1.0 remains the default target.
- Stop-risk-multiple target is independently selectable.
- Fixed monetary risk is the default volume model.
- Hedging defaults enabled and can be disabled.
- SELL stop includes current spread when enabled.
- Risk-capped volume is rounded down and rechecked against budget.
- Executed-signal visuals own prefix `EXP0017_P14_`.
- `CTrade` exists only in the order router.

## MetaEditor compile gate

Compile:

```text
EXP0017_CG_Raw_Execution_Backtest.mq5
```

Required result:

```text
0 errors, 0 warnings
```

## Strategy Tester scenarios

### A — fixed-risk CG3

- `cg_3m=true`, all others false;
- fixed risk 100;
- verify every projected stop loss is `<= 100` in the audit;
- verify selected volume is one broker step below the first volume that would breach 100, unless capped by broker maximum.

### B — sell spread stop

- verify SELL SL equals candle high + point buffer + entry quote spread;
- disable `InpAddSpreadToSellStop` and verify the spread term disappears.

### C — ATR and R target parity

- run ATR target with configurable multiplier;
- run stop-risk target with 1R and 2R;
- verify target distance against audit geometry.

### D — hedge switch

- hedging enabled: allow opposite independent positions on a hedging account;
- hedging disabled: reject an opposite owned position on the same symbol;
- verify same-direction behavior follows `InpPositionPolicy`.

### E — visuals

- verify only accepted trades draw;
- verify symbol-local divergence prices are placed only on matching charts;
- verify entry, SL, and TP levels appear only on the trade-symbol chart;
- verify disabling visual input creates no `EXP0017_P14_` objects.

### F — minimum volume

- configure a risk budget below broker minimum-lot stop loss;
- verify fixed-risk sizing rejects rather than exceeding the budget.

## Acceptance

Acceptance requires MetaEditor compilation, passing static tests, and visual/audit reconciliation of at least one BUY and one SELL under both target models.

## One-shot entitlement gate

The release is blocked unless a persistent divergence observed on several lower-timeframe candles produces at most one execution opportunity. Same-day restart must reconstruct the consumed key. Planning or transport failure must not cause a later retry. Full matrix: [[PHASE14_ONE_SHOT_VALIDATION_PLAN]].
