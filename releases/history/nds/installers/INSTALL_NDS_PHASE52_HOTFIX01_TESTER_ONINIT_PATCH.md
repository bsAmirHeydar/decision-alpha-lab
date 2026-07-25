# Install — NDS Phase 52 Hotfix 01 Strategy Tester OnInit

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_Phase52_Hotfix01_Tester_OnInit_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_Phase52_Hotfix01_Tester_OnInit_Patch.zip" `
  -Force
```

Compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Expected version:

```text
18.41
```

For Strategy Tester keep:

```text
InpLicenseAllowStrategyTesterBypass = true
InpLicenseAllowOptimizationBypass = true
InpPrintLicenseTesterBypass = true
```

Expected Journal line:

```text
FP_LICENSE status=tester_bypass context=visual_strategy_tester live_license_enforcement=unchanged
```

The live order switches remain independent:

```text
InpNDSHookTradeEnabled
InpNDSHookTradeSendLiveOrders
```

The license bypass only permits tester initialization. It does not itself enable
trade generation or order sending.

## QA

```powershell
python tools/flag_counting/nds_tester_oninit_contract_qa.py --root .
python tools/flag_counting/nds_hook_trade_contract_qa.py --root .
python tools/flag_counting/nds_entry_contract_qa.py --root .
python tools/flag_counting/nds_hook_contract_qa.py --root .
python tools/engineering/validate_alpha_lab_policy.py .
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
python docs/ai_algorithm_engineering_os/tools/validate_vault.py docs/ai_algorithm_engineering_os
```
