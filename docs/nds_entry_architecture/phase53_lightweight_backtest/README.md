# Phase 53 — Lightweight NDS Backtest Runtime

This package isolates the executable NDS strategy from the production visual expert.

## Runtime contract

```text
Canonical closed bars
→ canonical F/Rally detector
→ detection-only Hook Phase 02 ownership snapshot
→ valid F3H / HH selection
→ limit entry at Hook terminal
→ one managed exposure
→ same-direction post-entry F1-F2-F3 exit
```

The rules are shared with the production expert. Only the orchestration path changes.

## Files

- `01_scope_and_non_goals.md`
- `02_runtime_pipeline.md`
- `03_shared_core_parity_contract.md`
- `04_performance_profiles.md`
- `05_exposure_aware_fast_path.md`
- `06_operator_guide_fa.md`
- `07_validation_matrix.md`
- `08_benchmark_method.md`

## Executable

```text
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
```

## Core modules

```text
FP_HookPhase02DetectionCore.mqh
FP_NDSHookTradeExecutionCore.mqh
FP_NDSBacktestTypes.mqh
FP_NDSBacktestEngine.mqh
```
