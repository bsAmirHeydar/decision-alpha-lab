# NDS Phase 53 — Lightweight Backtest Runtime Audit Report

## Executive summary

The production `FlagCountingPhoenixExperiment` expert is an engineering and visualization host. Its runtime includes the canonical structural engine plus rendering, Hook phases 03–10, license checks, export, validation, release, ambiguity, acceptance, state-gate, paper lifecycle, broker rehearsal, normalization, and health pipelines. That architecture is appropriate for inspection but unnecessarily expensive for repeated Strategy Tester runs.

Phase 53 introduces a separate tester executable:

```text
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
```

The new executable preserves the current trading contract through shared cores and removes non-trading runtime work.

## Preserved executable contract

```text
valid Hook-after-Hook or Hook-after-F3
→ pending limit at raw Hook terminal
→ stop beyond Hook death/origin
→ one managed pending order or position
→ one attempt per Hook
→ wait for complete same-direction post-entry F1-F2-F3
→ close managed position by ticket
```

No entry, stop, single-exposure, or F123-exit rule was rewritten.

## Shared-core refactor

### Hook Phase 02

A new detection-only module now owns sequence construction and ownership annotation:

```text
FP_HookPhase02DetectionCore.mqh
```

The production `FP_HookPhase02Engine.mqh` delegates to this core and then applies optional rendering/export. The backtest runtime calls the core directly.

### Trade execution

The complete Phase 52 trade workflow was moved without semantic changes into:

```text
FP_NDSHookTradeExecutionCore.mqh
```

The production `FP_NDSHookTradeEngine.mqh` delegates to the core and then writes the optional lifecycle CSV. The backtest runtime calls the core directly and has no export sink.

A source-parity check verified that the extracted trade workflow is identical to the previous engine body after removing only CSV calls and renaming the core entry point.

## Removed runtime work

The lightweight call path does not load or execute:

- production license engine;
- chart renderer or object cleanup;
- chart-change events or timers;
- Hook phases 03–10;
- general Phase 51 Zone/Setup/Command preview pipeline;
- export, validation, release, interface, acceptance, ambiguity, and static-QA passes;
- Level 19–30 state, paper, safety, broker dry-run, validator, ledger, adapter, and lifecycle passes;
- final decision, CSV normalization, and runtime-health consolidations.

## Performance controls

### Once per new bar

The structural pipeline is gated by the current open-bar time. Multiple ticks inside the same bar do not trigger rescans.

### No duplicate Phase 01 pass

Hook Phase 02 builds its required node source internally. The backtest executable therefore does not execute a separate Phase 01 runtime pass.

### Exposure-aware fast path

When a managed position is open, the strategy needs only F events for the F123 exit. Hook reconstruction is skipped and the stale Hook snapshot is cleared. Pending orders do not use this fast path because Hook death cancellation must remain active.

### Profiles

| Profile | Bars | Scales | Purpose |
|---|---:|---|---|
| FAST | 1,200 | 2, 3, 5, 8 | rapid iteration and sweeps |
| PARITY | 5,000 | 2, 3, 5, 8, 13, 21, 34, 55 | production-context comparison |
| CUSTOM | operator-defined | operator-defined | controlled experiments |

FAST uses the same formulas and state machine over a bounded context. It can differ when a required parent structure lies outside 1,200 bars or on scales 13–55. PARITY is the acceptance profile.

## Determinism and safety

- The tester executable is rejected outside Strategy Tester by default.
- Optional non-tester dry-run forces `send_live_orders=false`.
- The one-attempt registry resets on initialization by default, preventing contamination between test runs.
- Trade CSV, Hook CSV, rendering, and periodic summaries are disabled by default.
- Actual Strategy Tester orders remain controlled by `InpBTSendTesterOrders`.

## Files added

```text
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
mql5/Include/FlagCountingPhoenix/FP_NDSBacktestTypes.mqh
mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02DetectionCore.mqh
mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh
tools/flag_counting/nds_lightweight_backtest_contract_qa.py
```

## Files refactored

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh
tools/flag_counting/nds_entry_contract_qa.py
tools/flag_counting/nds_hook_trade_contract_qa.py
```

## Validation performed

- lightweight backtest contract QA: 54 checks passed;
- Phase 52 trade contract QA: passed after shared-core path update;
- Phase 51 entry contract QA: passed after shared Hook-core path update;
- NDS Hook contract QA: passed;
- Strategy Tester OnInit contract QA: passed;
- engineering policy: 0 errors, 0 warnings;
- MQL5 compatibility scan: 0 errors, 0 warnings;
- repository layout: 0 missing expected directories;
- AI Engineering OS vault: 0 errors, 0 warnings;
- changed MQL lexical balance: passed;
- include resolution from the new EA: 0 missing project includes;
- Python QA syntax: passed.

## Unavailable validation

MetaEditor and the MT5 Strategy Tester are not available in this environment. Final compilation and runtime performance must therefore be confirmed locally. No measured speedup percentage is claimed in this report.
