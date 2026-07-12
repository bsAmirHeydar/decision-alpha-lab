# Install — NDS F2 Overlap-Wider and RR Reprice Patch

## Apply from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Overlap_Wider_RR_Reprice_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Overlap_Wider_RR_Reprice_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected source version:

```text
1.40
```

## Recommended test inputs

```text
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTAdjustEntryToMinimumRewardRisk = true
InpF2BTMinimumRewardRisk = 1.0

InpF2BTUseStopSpaceOverlapDeduplication = true
InpF2BTStopSpaceOverlapThresholdPercent = 80.0

InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
```

To merge more aggressively, change the overlap threshold to `70.0`.

Use `Every tick based on real ticks` for final execution verification.

## Contract checks

```powershell
python tools/flag_counting/nds_f2_waist_break_point2_contract_qa.py
python tools/flag_counting/nds_f2_waist_backtest_contract_qa.py
python tools/flag_counting/nds_f2_rr_parallel_context_contract_qa.py
python tools/flag_counting/nds_f2_overlap_wider_rr_reprice_contract_qa.py
```

## Commit

```powershell
git add -- `
  "INSTALL_NDS_F2_OVERLAP_WIDER_RR_REPRICE_PATCH.md" `
  "NDS_F2_OVERLAP_WIDER_RR_REPRICE_AUDIT_REPORT.md" `
  "NDS_F2_OVERLAP_WIDER_RR_REPRICE_MANIFEST.json" `
  "docs/flag_counting/README.md" `
  "docs/nds_entry_architecture/README.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/README.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/01_canonical_setup_contract.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/03_execution_state_machine.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/05_lifecycle_and_edge_cases.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/08_operator_guide.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/10_reward_risk_and_parallel_context_policy.md" `
  "docs/nds_entry_architecture/f2_waist_break_point2_limit/11_overlap_arbitration_and_rr_entry_repricing.md" `
  "docs/obsidian_hook/00_mocs/NDS_ENTRY_EXECUTION_MOC.md" `
  "docs/obsidian_hook/08_entry_execution/NDS F2 RR Hedge and Parallel Contexts.md" `
  "docs/obsidian_hook/08_entry_execution/NDS F2 Overlap Wider and RR Repricing.md" `
  "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh" `
  "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh" `
  "tools/flag_counting/nds_f2_waist_break_point2_contract_qa.py" `
  "tools/flag_counting/nds_f2_rr_parallel_context_contract_qa.py" `
  "tools/flag_counting/nds_f2_overlap_wider_rr_reprice_contract_qa.py"

git commit `
  -m "feat(nds): prefer wider overlapping F2 contexts" `
  -m "Deduplicate near-identical same-direction F2 Point-2 setups by configurable executable stop-corridor overlap, keep or replace with the wider context, and reprice sub-threshold pending entries toward the fixed F1-waist stop so final tick-normalized reward-to-risk meets the configured minimum."
```
