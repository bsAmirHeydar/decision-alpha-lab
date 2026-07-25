# Install — NDS F2 Canonical Frequency Recovery Patch

## Scope

This is a root-relative cumulative hotfix over the latest F2 `v1.90` patch chain. It upgrades the expert to `2.00` and the trade contract to `NDS-F2-WAIST-BREAK-11`.

## Install

From the repository root in PowerShell:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Canonical_Frequency_Recovery_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Canonical_Frequency_Recovery_Patch.zip" `
  -Force
```

## Compile target

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Required tester account mode

The defaults allow hedge and same-direction parallel contexts. Use an MT5 hedging account. With the default fail-fast input, a netting account returns `INIT_PARAMETERS_INCORRECT`.

To intentionally run a netting/single-context diagnostic, disable the parallel capabilities or explicitly disable the fail-fast input.

## Recommended baseline

```text
InpF2BTProfile = FAST
InpF2BTMaxSetupAgeBars = -1
InpF2BTConsumeAttemptOnlyOnFill = true
InpF2BTRequireCanonicalF3SpawnForLocalExit = true
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTAdjustEntryToMinimumRewardRisk = true
InpF2BTMinimumRewardRisk = 1.0
InpF2BTUseStopSpaceOverlapDeduplication = true
InpF2BTStopSpaceOverlapThresholdPercent = 80.0
InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
InpF2BTRequireHedgingAccountForParallelContexts = true
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
InpF2BTEnableFunnelDiagnostics = false
```

For final validation:

```text
Model = Every tick based on real ticks
```

## Diagnostics

To inspect where candidates are being rejected without restoring runtime prints:

```text
InpF2BTEnableFunnelDiagnostics = true
```

One CSV row is written on deinitialization to MT5 Common Files. Keep it disabled for normal speed tests.

## Validation commands

```powershell
python .\tools\engineering\check_mql5_compatibility.py
python .\tools\engineering\validate_alpha_lab_policy.py
python .\tools\engineering\audit_repository_layout.py
python .\tools\flag_counting\static_qa.py
python .\tools\flag_counting\nds_f2_canonical_frequency_recovery_contract_qa.py
python .\tools\flag_counting\nds_f2_waist_break_point2_contract_qa.py
python .\tools\flag_counting\nds_f2_htf_f_phase_filter_contract_qa.py
python .\tools\flag_counting\nds_f2_htf_f1_to_f2_window_contract_qa.py
python .\tools\flag_counting\nds_f2_dual_exit_contract_qa.py
python .\tools\flag_counting\nds_f2_per_trade_f3_exit_contract_qa.py
python .\tools\flag_counting\nds_f2_higher_timeframe_f3_exit_contract_qa.py
```
