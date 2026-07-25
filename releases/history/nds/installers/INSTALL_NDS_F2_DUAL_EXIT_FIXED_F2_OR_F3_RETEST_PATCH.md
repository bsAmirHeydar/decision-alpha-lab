# Install — NDS F2 Dual Exit Patch

Run from the repository root.

## Install

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Dual_Exit_Fixed_F2_or_F3_Retest_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Dual_Exit_Fixed_F2_or_F3_Retest_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected version:

```text
1.50
```

## Exit mode inputs

### Existing fixed exit

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END
```

The original F2 Leg2 endpoint is attached as broker TP.

### Dynamic F3 flag-retest exit

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_F3_FLAG_RETEST
InpF2BTF3ExitCorrectionTicks = 1.0
InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true
```

The original F2 Leg2 remains the RR reference. The order is sent with no TP; after exact F2 confirmation and a correction away, TP is armed at the F2-confirm/F3-Leg1 node.

## Recommended test model

```text
Every tick based on real ticks
```

## QA

```powershell
python tools/flag_counting/nds_f2_dual_exit_contract_qa.py
python tools/flag_counting/nds_f2_waist_break_point2_contract_qa.py
python tools/flag_counting/nds_f2_rr_parallel_context_contract_qa.py
python tools/flag_counting/nds_f2_overlap_wider_rr_reprice_contract_qa.py
python tools/flag_counting/nds_f2_waist_backtest_contract_qa.py
```
