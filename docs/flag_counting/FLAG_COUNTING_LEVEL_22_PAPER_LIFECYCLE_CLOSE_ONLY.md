# Flag Counting Level 22 — Paper Lifecycle Close-Only

## Purpose

Level 22 takes the Level 21 paper intent seed and reconstructs a close-only paper lifecycle.

This is not execution.

This is not a broker request.

This is not a paper order sent to a broker.

It is a CSV-only lifecycle reconstruction using closed-bar close prices.

## Hard boundary

Level 22 does not modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
F / Hook / Node detection logic
curve drawing logic
line drawing logic
RTV / zone objects
chart objects
license logic
broker logic
real execution logic
```

It remains:

```text
CSV-only
read-only
panel off
print silent by default
close-only
no order
no broker request
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level22_paper_lifecycle.csv
```

## New inputs

```text
InpLevel22PaperLifecycleEnabled = true
InpLevel22PaperLifecycleExportCsv = true
InpLevel22PaperLifecyclePrintSummary = false
InpLevel22PaperLifecycleRequireIntentAllowed = true
InpLevel22PaperLifecycleDefaultExpiryBars = 20
InpLevel22PaperLifecycleFolder = "FlagCountingPhoenix"
```

## Lifecycle statuses

```text
PAPER_LIFECYCLE_BLOCKED_INTENT_NOT_ALLOWED
PAPER_LIFECYCLE_BLOCKED_NO_DIRECTION
PAPER_LIFECYCLE_BLOCKED_MISSING_PRICE
PAPER_LIFECYCLE_BLOCKED_NO_BARS
PAPER_LIFECYCLE_PENDING
PAPER_LIFECYCLE_ENTERED_BY_CLOSE
PAPER_LIFECYCLE_HIT_TARGET_BY_CLOSE
PAPER_LIFECYCLE_HIT_STOP_BY_CLOSE
PAPER_LIFECYCLE_AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE
PAPER_LIFECYCLE_EXPIRED_BEFORE_ENTRY
PAPER_LIFECYCLE_EXPIRED_AFTER_ENTRY
PAPER_LIFECYCLE_OPEN_CLOSE_ONLY
```

## Close-only model

Level 22 deliberately ignores intrabar high/low.

It uses close price only.

For entry:

```text
bullish: close <= entry
bearish: close >= entry
```

For target:

```text
bullish: close >= target
bearish: close <= target
```

For stop:

```text
bullish: close <= stop
bearish: close >= stop
```

This is intentionally conservative and deterministic.

## Metrics

The output row includes:

```text
seed time
entry time
exit time
seed index
entry index
exit index
bars elapsed
expiry bars
entry close
exit close
best close
worst close
MFE close distance
MAE close distance
realized R-like
entry condition
exit condition
close-only path status
ambiguity status
```

## What Level 22 does not do

Level 22 does not:

```text
open a paper order
send an order
calculate lot size
calculate account risk
manage broker positions
modify chart objects
draw lifecycle markers
touch renderer logic
```

## Relationship to previous layers

Level 20 answers:

```text
Do we have entry / invalidation / destination anchors?
```

Level 21 answers:

```text
Can those anchors seed a paper intent?
```

Level 22 answers:

```text
What would the close-only lifecycle state be for that paper intent?
```

## Next correct layer

The next layer should be:

```text
Level 23 — Paper Performance
```

Level 23 should aggregate Level 22 lifecycle rows into performance-style metrics:

```text
target count
stop count
expired count
open count
ambiguous count
hit rate
avg R-like
best R-like
worst R-like
```
