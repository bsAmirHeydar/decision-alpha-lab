# Install — NDS F2 Waist Limit Backtest Patch

## Install from repository root

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Waist_Limit_Backtest_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Waist_Limit_Backtest_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5
```

## First test settings

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTEntryOffsetPoints = 1
InpF2BTMaxSetupAgeBars = 1
InpF2BTOneAttemptPerF2 = true
InpF2BTResetUsedSetupsOnInit = true
```

## Expected startup line

```text
NDS_F2_BT_INIT status=ready version=NDS-F2-BACKTEST-01
```

## QA

```powershell
python .\tools\flag_counting\nds_f2_waist_backtest_contract_qa.py
python .\tools\flag_counting\nds_lightweight_backtest_contract_qa.py
python .\tools\flag_counting\nds_hook_trade_contract_qa.py
python .\tools\engineering\validate_alpha_lab_policy.py
python .\tools\engineering\check_mql5_compatibility.py
```

## Staging and commit

Use the exact command supplied with the patch delivery.
