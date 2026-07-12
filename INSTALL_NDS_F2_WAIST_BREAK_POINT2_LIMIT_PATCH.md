# Install — NDS F2 Waist-Break Point-2 Limit Patch

## 1. Extract

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Waist_Break_Point2_Limit_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Waist_Break_Point2_Limit_Patch.zip" `
  -Force
```

## 2. Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## 3. Recommended first tester inputs

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTRequireF2SizeGate = false
InpF2BTOneAttemptPerF2Body = true
InpF2BTCancelPendingIfTargetTouchedBeforeFill = true
InpF2BTMaxSetupAgeBars = 0
InpF2BTEntryBehindF2WaistTicks = 1
InpF2BTStopBehindF1WaistTicks = 1
InpF2BTFixedVolume = 0.01
```

Use `Every tick based on real ticks` for execution validation.

## 4. Run QA

```powershell
python .\tools\flag_counting\nds_f2_waist_backtest_contract_qa.py
python .\tools\flag_counting\nds_f2_waist_break_point2_contract_qa.py
```

## 5. Expected semantics

```text
F2 body complete, not confirmed
→ limit behind F2 Waist
→ fill is Point 2
→ stop behind parent F1 Waist
→ target F2 Leg2
```
