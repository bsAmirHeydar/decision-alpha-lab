# Install NDS Hook 86.4 No-Trade Fix v1.1.0

## Dependency

The original NDS Hook 86.4 Cycle R1 v1.0.0 patch must already be installed.

## Repository QA

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
```

## Windows MetaEditor gate

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\compile_nds_hook_864_cycle_r1.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```

## MQL5 no-order contract test

Compile and execute:

```text
NDSHook864CycleR1ContractSelfTest
```

Expected Journal marker:

```text
NDS_HOOK_864_SELFTEST_PASS
```

## Strategy Tester

```text
Expert: NDSHookLimitF123Backtest
Runtime input: InpBTProfile = PARITY
Trade input: InpBTTradeProfile = HOOK_864_CYCLE_R1
Run summary: InpBTPrintRunSummary = true
Tester orders: InpBTSendTesterOrders = true
```

The v1.1 defaults already contain these values. Review `dominant_blocker` and the final `NDS_BT_SESSION` counters before changing any setup rule.

## Saved-log analysis

```powershell
python .\tools\flag_counting\analyze_nds_hook_864_tester_log.py .\path\to\tester.log
```

## Rollback

Stop the test, preserve the tester Journal and external evidence, cancel/reconcile any demo pending order, then revert the single v1.1 hotfix commit. Do not clear the one-attempt registry before reconciliation.
