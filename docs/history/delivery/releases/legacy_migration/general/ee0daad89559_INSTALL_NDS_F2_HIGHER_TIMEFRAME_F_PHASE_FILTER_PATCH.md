# Install — NDS F2 Higher-Timeframe F-Phase Filter

Run from the repository root.

## Install

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Higher_Timeframe_F_Phase_Filter_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Higher_Timeframe_F_Phase_Filter_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected expert version:

```text
1.60
```

## Default tester inputs

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

## Expected directional behavior

```text
H1 bullish F → new Buy only
H1 bearish F → new Sell only
H1 Hook/ND or unresolved → no new entry
```

Existing positions are not closed by the filter. Pending orders that no longer match the gate are cancelled by default.

## Validation command

```powershell
python tools/flag_counting/nds_f2_htf_f_phase_filter_contract_qa.py
```
