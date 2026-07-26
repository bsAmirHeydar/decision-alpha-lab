# 02 — Authoritative Reuse Map

## End-to-end path

```text
FP_RunHookPhase02DetectionCore
→ FP_HookPhase02Sequence[]
→ FP_NDSStructureSnapshot
→ FP_NDSHookTradeSelectLatest
→ FP_NDSHook864CycleR1SequenceEligible
→ FP_NDSHookTradeBuildSetup
→ FP_NDSHookTradeSendLimit
→ broker-managed SL/TP
→ FP_NDSHookTradeExportReport
```

## Reused sequence fields

The profile reads these fields directly from `FP_HookPhase02Sequence`:

```text
sequence_id
direction
origin_time
origin_price
cycle_crown_time
cycle_crown_price
cycle_crown_valid
last_x_time
x_count
resolve_time
resolve_price
resolve_confirmed
retracement_ratio
death_boundary_price
state
valid
hook_failed
valid_hook_family
valid_after_hook
valid_after_opposing_f3
```

The Origin is not counted as X1. `x_count` retains the exact Hook Phase02 meaning. Phase 55 never attempts to infer the count from price turns.

## Reused execution modules

- `FP_NDSHookTradeFamilyAllowed`: HH/F3H authority.
- `FP_NDSHookTradeNormalizePrice`: symbol tick normalization.
- `FP_NDSHookTradeComputeVolume`: fixed volume or risk-cash sizing.
- `FP_NDSHookTradeCountManagedOrders/Positions`: exposure ownership.
- `FP_NDSHookTradeAcquireEntryLock`: terminal-wide compare-and-swap lock.
- `FP_NDSHookTradeSetupUsed/MarkSetupUsed`: persistent one-attempt identity.
- `FP_NDSHookTradeCancelDeadPending`: structural invalidation.
- `FP_NDSHookTradeCanSend`: terminal/account/symbol order capabilities.
- `FP_NDSHookTradeSendLimit`: broker request and retcode verification.
- `FP_NDSHookTradeFinalizeReport`: profile-specific evidence.

## Deliberately untouched modules

Hook Phase01/02 detection rules and all F lifecycle detectors remain semantically unchanged. The new adapter is included below those layers and cannot mutate their state.

## Shared-core parity

Both the central EA and lightweight tester call `FP_RunNDSHookTradeExecutionCore`. The old `FP_RunNDSHookLimitF123ExecutionCore` symbol remains as a compatibility wrapper. This avoids a production/tester fork and keeps the existing Phase 52 API stable.
