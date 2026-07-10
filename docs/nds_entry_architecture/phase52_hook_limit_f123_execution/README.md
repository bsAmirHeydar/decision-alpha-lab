---
title: NDS Phase 52 Hook Limit and F123 Exit
status: implemented_opt_in
version: 1.0.0
updated: 2026-07-10
---
# NDS Phase 52 — Hook Limit Entry and Same-Direction F123 Exit

## Purpose

Phase 52 adds a narrow executable NDS profile on top of the Phase 51 no-send transition scaffold.

```text
Valid Hook-after-Hook or Hook-after-opposing-F3
→ limit order at the Hook terminal
→ one managed exposure globally
→ wait for a new same-direction F1 → F2 → F3 chain
→ close the position at market when that F3 completes
→ return to idle
```

The profile does **not** claim to solve the general Zone Canon. It implements the explicit Hook-terminal execution instruction for the two currently valid Hook families.

## Authority boundary

Two independent inputs are required before a broker request can be submitted:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

Both default to `false`.

## Reading order

1. [[01_scope_and_canon]]
2. [[02_limit_entry_geometry]]
3. [[03_single_exposure_state_machine]]
4. [[04_same_direction_f123_exit]]
5. [[05_order_lifecycle_and_recovery]]
6. [[06_inputs_and_operator_profiles]]
7. [[07_validation_matrix]]
8. [[08_persian_operator_guide]]

## MQL5 modules

```text
FP_NDSHookTradeTypes.mqh
FP_NDSHookTradeRules.mqh
FP_NDSHookTradeExport.mqh
FP_NDSHookTradeEngine.mqh
```

## Audit output

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_limit_f123_trade_ledger.csv
```
