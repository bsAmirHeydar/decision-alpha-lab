# Install — NDS F2 Higher-Timeframe F3 Exit Patch

## Apply

Extract the patch at the repository root with overwrite enabled.

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Higher_Timeframe_F3_Exit_Patch.zip" `
  -DestinationPath "." `
  -Force
```

## Compile

Compile:

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Activate the new mode

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST
InpF2BTF3ExitHigherTimeframe = PERIOD_H1
```

The exit timeframe must be strictly higher than the chart timeframe.

## Recommended Strategy Tester model

```text
Every tick based on real ticks
```

## Expected behavior

```text
Entry and SL remain unchanged.
Minimum RR remains based on original lower-timeframe F2 Leg2.
No initial broker TP is sent.
The position waits for the first eligible same-direction canonical HTF F3.
After the Waist of that same F3 exists, TP is armed at its exact Leg1 endpoint.
Each position ticket is managed independently.
```

## Run contract QA

```powershell
python tools/flag_counting/nds_f2_higher_timeframe_f3_exit_contract_qa.py
```

Run all F2 regression checks:

```powershell
Get-ChildItem "tools/flag_counting/nds_f2_*contract_qa.py" | ForEach-Object {
  python $_.FullName
}
```
