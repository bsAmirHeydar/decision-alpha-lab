# Install — NDS Phase 53 Lightweight Backtest Patch

## 1. Extract from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_Phase53_Lightweight_Backtest_Runtime_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_Phase53_Lightweight_Backtest_Runtime_Patch.zip" `
  -Force
```

## 2. Compile

Compile both files to validate the shared-core refactor:

```text
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

The first is the fast Strategy Tester executable. The second confirms that the production wrapper still compiles after shared-core extraction.

## 3. Strategy Tester selection

Select:

```text
NDSHookLimitF123Backtest
```

Recommended first run:

```text
InpBTProfile = FAST
InpBTTradeEnabled = true
InpBTSendTesterOrders = true
InpBTResetUsedSetupsOnInit = true
InpBTSkipHookRebuildWhilePositionOpen = true
InpBTPrintRunSummary = false
```

For production-context comparison:

```text
InpBTProfile = PARITY
```

## 4. Expected Journal initialization

```text
NDS_BT_INIT status=ready version=NDS-BACKTEST-01 profile=FAST ...
```

The session ends with an in-memory timing summary when `InpBTPrintSessionSummary=true`.

## 5. Static QA

```powershell
python tools/flag_counting/nds_lightweight_backtest_contract_qa.py
python tools/flag_counting/nds_hook_trade_contract_qa.py
python tools/flag_counting/nds_entry_contract_qa.py
python tools/flag_counting/nds_hook_contract_qa.py
python tools/flag_counting/nds_tester_oninit_contract_qa.py
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
python docs/ai_algorithm_engineering_os/tools/validate_vault.py
```

## 6. Commit

```powershell
git add -- `
  "docs/releases/legacy_migration/general/4637a70e30e0_INSTALL_NDS_PHASE53_LIGHTWEIGHT_BACKTEST_PATCH.md" `
  "docs/evidence/nds_phase_53_lightweight_backtest_runtime_audit/a5a07ff463b7_NDS_PHASE53_LIGHTWEIGHT_BACKTEST_AUDIT_REPORT.md" `
  "NDS_PHASE53_LIGHTWEIGHT_BACKTEST_MANIFEST.json" `
  "docs/flag_counting/README.md" `
  "docs/nds_entry_architecture/README.md" `
  "docs/nds_entry_architecture/phase53_lightweight_backtest" `
  "docs/nds_hook_architecture/71_phase53_lightweight_backtest_runtime.md" `
  "docs/nds_hook_architecture/README.md" `
  "docs/evidence/nds_entry_execution_moc/52823598bbb7_NDS_ENTRY_EXECUTION_MOC.md" `
  "docs/obsidian_hook/08_entry_execution/NDS Lightweight Backtest Runtime.md" `
  "docs/obsidian_hook/08_entry_execution/NDS Backtest Performance Profiles.md" `
  "docs/obsidian_hook/08_entry_execution/NDS Backtest Parity Contract.md" `
  "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestTypes.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02DetectionCore.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh" `
  "tools/flag_counting/nds_lightweight_backtest_contract_qa.py" `
  "tools/flag_counting/nds_entry_contract_qa.py" `
  "tools/flag_counting/nds_hook_trade_contract_qa.py"

git diff --cached --stat

git status

git commit `
  -m "perf(nds): add lightweight shared-core backtest runtime" `
  -m "Separate Strategy Tester execution from the production visual expert, extract shared Hook detection and trade execution cores, run once per new bar, add exposure-aware Hook-scan skipping, and provide FAST, PARITY, and CUSTOM backtest profiles with full QA and Obsidian documentation."

git push
```
