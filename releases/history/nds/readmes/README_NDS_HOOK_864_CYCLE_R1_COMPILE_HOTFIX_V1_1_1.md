# NDS Hook 86.4 Cycle R1 — Compile Hotfix v1.1.1

This delta patch fixes the MetaEditor error caused by the stale identifier `FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT_READY` in `FP_NDSBacktestEngine.mqh`.

The canonical action is `FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT`, as defined in `FP_NDSHookTradeTypes.mqh` and emitted by `FP_NDSHookTradeExecutionCore.mqh`.

## Scope

- Replace the stale action alias with the canonical enum member.
- Add repository-wide trade-action identifier closure QA.
- Preserve all v1.1 setup, Phase04, first-arrival, execution, risk, and broker behavior unchanged.

## Dependency

Install after:

```text
decision-alpha-lab-nds-hook-864-cycle-r1-no-trade-fix-v1.1.0
```

## Repository QA

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
```

## MetaEditor gate

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\compile_nds_hook_864_cycle_r1.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```

MetaEditor execution remains external to the Linux QA environment.
