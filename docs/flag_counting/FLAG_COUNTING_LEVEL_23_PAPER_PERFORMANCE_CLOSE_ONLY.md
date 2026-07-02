# Flag Counting Level 23 — Paper Performance Close-Only

## Purpose

Level 23 summarizes the close-only paper lifecycle produced by Level 22.

Level 22 reconstructs a single paper lifecycle from the current paper intent.

Level 23 converts that lifecycle into performance-style research metrics.

This is still not execution.

It does not send orders.

It does not create broker requests.

It does not calculate volume or account risk.

## Hard boundary

Level 23 does not modify:

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
close-only paper performance
no order
no broker request
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level23_paper_performance.csv
```

## New inputs

```text
InpLevel23PaperPerformanceEnabled = true
InpLevel23PaperPerformanceExportCsv = true
InpLevel23PaperPerformancePrintSummary = false
InpLevel23PaperPerformanceCountBlockedSamples = true
InpLevel23PaperPerformanceCountOpenSamples = true
InpLevel23PaperPerformanceCountExpiredAsResolved = true
InpLevel23PaperPerformanceFolder = "FlagCountingPhoenix"
```

## What it measures

The summary row includes:

```text
current lifecycle id
current lifecycle status
current outcome class
current R-like
current bars elapsed
sample total
counted total
duplicate total
blocked count
tracked count
entered count
target count
stop count
expired count
open count
ambiguous count
resolved count
win-like count
loss-like count
neutral-like count
hit-rate-like
loss-rate-like
avg R-like
best R-like
worst R-like
sum R-like
```

## Outcome classes

```text
OUTCOME_BLOCKED
OUTCOME_TARGET
OUTCOME_STOP
OUTCOME_AMBIGUOUS
OUTCOME_EXPIRED_BEFORE_ENTRY
OUTCOME_EXPIRED_AFTER_ENTRY
OUTCOME_OPEN
OUTCOME_PENDING
OUTCOME_ENTERED_OPEN
OUTCOME_OTHER
```

## Duplicate handling

The EA can recalculate the same lifecycle many times on the same bar.

Level 23 builds a sample key from:

```text
lifecycle id
lifecycle status
entry time
exit time
exit close
R-like result
```

If the same sample repeats, it increments duplicate count and does not double-count performance.

## R-like metrics

Level 23 uses the close-only realized R-like value from Level 22.

The result is research-only.

It is not account PnL.

It is not broker PnL.

It is not a real trade result.

## Relationship to earlier levels

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
What would the close-only lifecycle state be?
```

Level 23 answers:

```text
What is the performance-style summary of those lifecycle results?
```

## Next correct layer

The next layer should be:

```text
Level 24 — Safety Gate
```

Level 24 should not execute either. It should define hard gates before any future broker dry run:

```text
license ok
symbol allowed
timeframe allowed
spread ok
paper performance ok
manual arm ok
real execution disabled
```
