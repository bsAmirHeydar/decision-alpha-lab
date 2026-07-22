# Install — NDS F2 RR, Hedge and Parallel Contexts Patch

## Apply from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_RR_Hedge_Parallel_Contexts_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_RR_Hedge_Parallel_Contexts_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected source version:

```text
1.30
```

## Recommended first tester configuration

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true

InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTMinimumRewardRisk = 1.0

InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
InpF2BTMaxConcurrentManagedExposures = 0

InpF2BTOneAttemptPerF2Body = true
InpF2BTCancelPendingIfTargetTouchedBeforeFill = true
InpF2BTEntryBehindF2WaistTicks = 1
InpF2BTStopBehindF1WaistTicks = 1
```

Use an MT5 hedging account to test independent simultaneous same-symbol contexts. A netting account intentionally blocks the second managed exposure.

## QA

```powershell
python tools/flag_counting/nds_f2_waist_break_point2_contract_qa.py
python tools/flag_counting/nds_f2_waist_backtest_contract_qa.py
python tools/flag_counting/nds_f2_rr_parallel_context_contract_qa.py
python tools/engineering/validate_alpha_lab_policy.py
python tools/engineering/check_mql5_compatibility.py
python tools/engineering/audit_repository_layout.py
```

## Commit

```powershell
git add -- `
  "docs/releases/legacy_migration/general/190d82ab6c56_INSTALL_NDS_F2_RR_HEDGE_PARALLEL_CONTEXTS_PATCH.md" `
  "NDS_F2_RR_HEDGE_PARALLEL_CONTEXTS_AUDIT_REPORT.md" `
  "NDS_F2_RR_HEDGE_PARALLEL_CONTEXTS_MANIFEST.json" `
  "docs/flag_counting/README.md" `
  "docs/nds_entry_architecture/README.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/README.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/01_canonical_setup_contract.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/03_execution_state_machine.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/05_lifecycle_and_edge_cases.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/08_operator_guide.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/10_reward_risk_and_parallel_context_policy.md" `
  "docs/evidence/nds_entry_execution_moc/52823598bbb7_NDS_ENTRY_EXECUTION_MOC.md" `
  "docs/obsidian_hook/08_entry_execution/NDS F2 Waist-Break Point2 Limit Setup.md" `
  "docs/obsidian_hook/08_entry_execution/NDS F2 RR Hedge and Parallel Contexts.md" `
  "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh" `
  "tools/flag_counting/nds_f2_waist_break_point2_contract_qa.py" `
  "tools/flag_counting/nds_f2_waist_backtest_contract_qa.py" `
  "tools/flag_counting/nds_f2_rr_parallel_context_contract_qa.py"

git commit `
  -m "feat(nds): add RR filter and parallel F2 contexts" `
  -m "Filter F2 Waist-Break Point2 setups by configurable normalized reward-to-risk with a default minimum of 1.0, allow independent opposite-direction hedge and same-direction contexts by default, preserve one-attempt-per-body identity, reconcile multiple pending targets independently, enforce MT5 hedging-account ownership for parallel same-symbol positions, and retain the lightweight no-print F1/F2-only runtime."
```
