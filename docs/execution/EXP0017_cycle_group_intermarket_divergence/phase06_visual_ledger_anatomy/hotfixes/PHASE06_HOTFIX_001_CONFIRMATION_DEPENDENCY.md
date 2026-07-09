# Phase 06 Hotfix 001 — Confirmation Dependency Restore

## Root Cause

Phase 06 is not a standalone anatomy layer. It is intentionally built on top of the Phase 05 confirmation and invalidation layer.

The Phase 06 modules use Phase 05 confirmation symbols, especially:

```text
SCGCFinalSignal
SCGCConfirmationConfig
CCGC_ConfirmationField
CGC_STATUS_CONFIRMED_TRADEABLE
CGC_STATUS_INVALIDATED_DOUBLE_HUNT
CGC_DIRECTION_BUY
CGC_DIRECTION_SELL
CGC_SIDE_HIGH
CGC_SIDE_LOW
```

When MetaEditor cannot find `CGC_Types.mqh` or `CGC_ConfirmationField.mqh`, every downstream reference to these types becomes unknown. The many `declaration without type`, `& comma expected`, and `undeclared identifier` errors are therefore cascade errors.

## Correction

This patch restores the Phase 05 confirmation dependency files into:

```text
MQL5/Include/IntermarketDivergenceExecution/CG/
```

The restored files are:

```text
CGC_Types.mqh
CGC_ConfirmationField.mqh
CGC_Display.mqh
CGC_Engine.mqh
```

## Implementation Principle

Phase 06 should continue to reuse Phase 05 final-signal anatomy rather than duplicating confirmation types inside `CGV_*` files.

That preserves the dependency chain:

```text
Phase 01 Time Anatomy
  -> Phase 02 Reference Field
  -> Phase 03 Hunt Anatomy
  -> Phase 04 Divergence Anatomy
  -> Phase 05 Confirmation / Invalidation
  -> Phase 06 Visual Ledger
```

## Expected Effect

After this patch, the missing include errors for `CGC_Types.mqh` and `CGC_ConfirmationField.mqh` should disappear. The dependent type errors in `CGV_Ledger.mqh`, `CGV_Drawing.mqh`, `CGV_Display.mqh`, and `CGV_Engine.mqh` should also disappear if previous Phase 01 through Phase 04 include files are already installed.

## No Strategy Change

This hotfix does not add trading, risk, target, statistics, AI, or filtering. It only restores compile dependencies for Phase 06.
