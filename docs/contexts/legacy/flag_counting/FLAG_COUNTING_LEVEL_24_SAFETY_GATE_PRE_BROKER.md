# Flag Counting Level 24 — Safety Gate / Pre-Broker Guard

## Purpose

Level 24 adds a pre-broker safety gate after the Level 23 close-only paper performance layer.

This is still not execution.

It does not send orders.

It does not create broker requests.

It does not calculate volume or account risk.

The goal is to decide whether the system is allowed to move to a future dry-run broker layer.

## Hard boundary

Level 24 does not modify:

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
safety gate only
no order
no broker request
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level24_safety_gate.csv
```

## New inputs

```text
InpLevel24SafetyGateEnabled = true
InpLevel24SafetyGateExportCsv = true
InpLevel24SafetyGatePrintSummary = false
InpLevel24SafetyGateManualArm = false
InpLevel24SafetyGateRealExecutionEnabled = false
InpLevel24SafetyGateRequireLicenseOk = true
InpLevel24SafetyGateRequireSymbolAllowed = true
InpLevel24SafetyGateRequireTimeframeAllowed = true
InpLevel24SafetyGateRequireSpreadOk = true
InpLevel24SafetyGateRequirePerformanceOk = false
InpLevel24SafetyGateRequireManualArm = false
InpLevel24SafetyGateRequireRealExecutionDisabled = true
InpLevel24SafetyGateAllowedSymbols = "*"
InpLevel24SafetyGateAllowedTimeframes = "*"
InpLevel24SafetyGateMaxSpreadPoints = 0
InpLevel24SafetyGateMinResolvedSamples = 30
InpLevel24SafetyGateMinHitRateLike = 0.50
InpLevel24SafetyGateMinAvgRLike = 0.00
InpLevel24SafetyGateFolder = "FlagCountingPhoenix"
```

## Checks

The safety gate evaluates:

```text
license_ok
symbol_allowed
timeframe_allowed
spread_ok
paper_performance_ok
manual_arm_ok
real_execution_disabled_ok
```

## Default behavior

By default, real execution is disabled:

```text
InpLevel24SafetyGateRealExecutionEnabled = false
```

Manual arm is also disabled:

```text
InpLevel24SafetyGateManualArm = false
```

However, manual arm is not required by default at this layer:

```text
InpLevel24SafetyGateRequireManualArm = false
```

This keeps Level 24 usable as a diagnostic safety report without blocking all research runs.

## Performance gate

Performance gating is available but disabled by default:

```text
InpLevel24SafetyGateRequirePerformanceOk = false
```

When enabled, Level 24 requires:

```text
resolved samples >= InpLevel24SafetyGateMinResolvedSamples
hit-rate-like >= InpLevel24SafetyGateMinHitRateLike
avg R-like >= InpLevel24SafetyGateMinAvgRLike
```

The performance values come from Level 23 runtime counters.

## Spread gate

If:

```text
InpLevel24SafetyGateMaxSpreadPoints <= 0
```

spread filtering is disabled.

If it is positive, the current symbol spread must be less than or equal to the configured maximum.

## Allow lists

Allowed symbols and timeframes support:

```text
*
```

or comma / semicolon / pipe / space separated values.

Examples:

```text
GOLD*,XAUUSD,EURUSD
PERIOD_M1,PERIOD_M5,PERIOD_H1
```

## Gate statuses

```text
SAFETY_GATE_PASSED_RESEARCH_ONLY
SAFETY_GATE_BLOCKED
```

## Block reasons

```text
BLOCK_LICENSE_NOT_OK
BLOCK_SYMBOL_NOT_ALLOWED
BLOCK_TIMEFRAME_NOT_ALLOWED
BLOCK_SPREAD_TOO_WIDE
BLOCK_PAPER_PERFORMANCE_NOT_OK
BLOCK_MANUAL_ARM_OFF
BLOCK_REAL_EXECUTION_ENABLED_INSIDE_SAFETY_GATE
```

## Next step field

If passed:

```text
NEXT_LEVEL_25_BROKER_DRY_RUN_ONLY
```

If blocked:

```text
NEXT_FIX_BLOCK_REASON_BEFORE_BROKER_DRY_RUN
```

## Relationship to previous levels

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
What is the performance-style summary?
```

Level 24 answers:

```text
Is the research stack safe enough to move to a future dry-run broker request layer?
```

## Next correct layer

The next layer should be:

```text
Level 25 — Broker Dry Run Only
```

Level 25 should still not send orders. It should only build a hypothetical request row:

```text
request_type
symbol
direction
entry
sl
tp
magic
comment
dry_run_only = true
```
