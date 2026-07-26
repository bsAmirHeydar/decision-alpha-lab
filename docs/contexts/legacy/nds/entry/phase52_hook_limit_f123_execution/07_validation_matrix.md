---
title: Phase 52 Validation Matrix
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Validation Matrix

## Static contract tests

| ID | Expected contract |
|---|---|
| P52-SRC-01 | only HH/F3H/F3H+HH are eligible |
| P52-ENT-01 | positive Hook produces Buy Limit at terminal |
| P52-ENT-02 | negative Hook produces Sell Limit at terminal |
| P52-RSK-01 | SL lies beyond Hook death/origin |
| P52-TGT-01 | attached TP is zero |
| P52-ONE-01 | magic-wide pending/position count blocks another setup |
| P52-ONE-02 | compare-and-swap entry lock exists |
| P52-ONE-03 | duplicate pending orders are reconciled |
| P52-EXIT-01 | exit direction equals position direction |
| P52-EXIT-02 | explicit F1 and F2 evidence exists in F3 sequence |
| P52-EXIT-03 | strict mode requires F1/F2 after broker open time |
| P52-EXIT-04 | close is by position ticket and verified |
| P52-SAFE-01 | both live-authority inputs default false |
| P52-AUD-01 | every state writes the trade ledger |

## MetaEditor tests

1. Compile `FlagCountingPhoenixExperiment.mq5` with `0 errors, 0 warnings`.
2. Load on a test symbol with Phase 52 disabled; verify no order action.
3. Enable decision audit only; verify `PAPER_LIMIT` and no broker order.
4. Enable live on demo; verify one pending limit only.
5. Open a second chart with the same magic; verify no second pending order.
6. Fill the limit; verify stray pending orders are removed.
7. Form an opposite-direction F123; verify position remains open.
8. Form a same-direction F123 whose F1 began before fill; verify strict mode rejects it.
9. Form a full same-direction F123 after fill; verify close request and ticket disappearance.
10. Restart EA with the same Hook; verify one-attempt persistence blocks re-entry.

## Regression tests

- Hook rendering remains unchanged.
- Hook Phase02 validity counts remain unchanged.
- Phase 51 no-send command preview remains no-send.
- Generic Levels 20–30 broker-preview modules are not promoted into this strategy.
- With Phase 52 disabled, broker state is untouched.
