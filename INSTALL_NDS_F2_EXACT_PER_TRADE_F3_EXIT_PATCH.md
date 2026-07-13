# Install — NDS F2 Exact Per-Trade F3 Exit Patch

## Install

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath ".\NDS_F2_Exact_Per_Trade_F3_Exit_Patch.zip" `
  -DestinationPath "." `
  -Force

Remove-Item `
  -LiteralPath ".\NDS_F2_Exact_Per_Trade_F3_Exit_Patch.zip" `
  -Force
```

## Compile

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

Expected version:

```text
1.70
```

## Test profile

```text
InpF2BTExitMode = FP_NDS_F2_EXIT_F3_FLAG_RETEST
Model = Every tick based on real ticks
```

Keep the existing RR, overlap, hedge, parallel-context, and H1 filter inputs as required by the test.

## Acceptance checks

For two simultaneous positions, verify that each position:

1. remains bound to its own order/position identity;
2. reconstructs its own source F2 sequence;
3. accepts only the direct child F3 of that source F2;
4. waits for the Waist of that same child F3;
5. receives TP at the Leg1 of that same child F3;
6. never receives the target of another position.

Fixed F2-target mode must remain unchanged.
