# M0008 F2 MQL5 Implementation

## Module

```text
mql5/Include/M0008/
mql5/Experts/M0008/M0008_FlagCountingF2.mq5
```

M0008 depends on M0007:

```mql5
#include <M0007/DAL_M0007F1Detector.mqh>
```

The dependency is intentional. F2 cannot be evaluated without parent F1 internal `2`.

## Expert

```text
M0008_FlagCountingF2.mq5
```

The expert is visual/research only. It does not place trades.

## Main inputs

```text
InpRequireParentF1Confirmed
InpAllowWaistBreakBranch
InpRequireBranch12ForF2
InpRequireLeg2RebreakForConfirm
InpScanBullishF2
InpScanBearishF2
```

## Output on chart

The renderer draws:

```text
F2 path body
F2 label
1 and 2 labels
```

The branch type is logged. Optional `InpShowWaistBreakTag` can mark the waist-break branch with `WB`.

## Research use

Use M0008 to audit whether continuation counts after F1 create better continuation windows than F1 alone.

Recommended first settings:

```text
InpRequireParentF1Confirmed = true
InpAllowWaistBreakBranch = true
InpRequireBranch12ForF2 = true
InpRequireLeg2RebreakForConfirm = true
InpDrawOnlyConfirmed = false
```
