# EXP0017 Phase 06 Hotfix 001 — Confirmation Dependency Restore

This patch restores the Phase 05 confirmation include files required by Phase 06 Visual Ledger.

## Problem

Phase 06 files compile against confirmation-layer types and field builders:

- `SCGCFinalSignal`
- `SCGCConfirmationConfig`
- `CCGC_ConfirmationField`
- `CGC_STATUS_CONFIRMED_TRADEABLE`
- `CGC_STATUS_INVALIDATED_DOUBLE_HUNT`
- `CGC_DIRECTION_BUY`
- `CGC_DIRECTION_SELL`
- `CGC_SIDE_HIGH`
- `CGC_SIDE_LOW`

Those symbols live in the Phase 05 include files. If the Phase 05 include files are not present inside the terminal `MQL5\Include\IntermarketDivergenceExecution\CG` folder, MetaEditor reports missing include errors first and then cascades into many false type errors.

## Fix

This hotfix adds the missing Phase 05 confirmation includes into the same include folder used by Phase 06.

## No Logic Change

This patch does not change the Phase 06 visual-ledger logic. It only restores required dependency files.

## Files

- `mql5/Include/IntermarketDivergenceExecution/CG/CGC_Types.mqh`
- `mql5/Include/IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh`
- `mql5/Include/IntermarketDivergenceExecution/CG/CGC_Display.mqh`
- `mql5/Include/IntermarketDivergenceExecution/CG/CGC_Engine.mqh`
