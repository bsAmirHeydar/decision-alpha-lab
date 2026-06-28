# Phoenix Flag Counting Acceptance Matrix

This folder documents Level 16 acceptance runs for `FlagCountingPhoenixExperiment.mq5`.

Level 16 is implemented by:

```text
FP_AcceptanceTypes.mqh
FP_AcceptanceRules.mqh
FP_AcceptanceAudit.mqh
FP_AcceptanceEngine.mqh
```

It runs after Level 15 postflight and before `FP_SUMMARY`.

## Modes

```text
observe     default, report gates without forcing baseline numbers
baseline    capture actual counts as WARN rows for future case registration
regression  compare configured minimum expectations
release     strict operator review mode
```

## Output

Enable CSV:

```text
InpAcceptanceWriteCsv = true
```

Default output:

```text
MQL5/Files/FlagCountingPhoenix/latest_acceptance.csv
```

## Baseline policy

Do not invent expected counts. Run baseline mode on a pinned symbol/timeframe/date-range, export `latest_acceptance.csv`, then copy real counts into the case registry and validation expected inputs.
