# Install — NDS F2 Fast Exact Backtest Hotfix

## Apply

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Fast_Exact_Backtest_Hotfix_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Fast_Exact_Backtest_Hotfix_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected expert version:

```text
1.10
```

## First test inputs

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTMaxSetupAgeBars = 0
InpF2BTEntryOffsetTicks = 1
InpF2BTOneAttemptPerF2 = true
InpF2BTResetUsedSetupsOnInit = true
InpF2BTFixedVolume = 0.01
```

The expert intentionally emits no custom runtime prints. Inspect Strategy Tester Orders, Deals and Results for actual execution.
