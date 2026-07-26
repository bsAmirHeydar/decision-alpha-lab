# Flag Counting Level 21 — Paper Intent / No Order

## Purpose

Level 21 converts a ready Level 20 Entry Bridge row into a paper intent seed.

This is still not execution.

It does not send orders.

It does not create broker requests.

It does not size volume.

It does not open positions.

## Hard boundary

Level 21 does not modify:

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
paper intent only
no order
no broker request
no real execution
```

## New output

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level21_paper_intents.csv
```

## New inputs

```text
InpLevel21PaperIntentEnabled = true
InpLevel21PaperIntentExportCsv = true
InpLevel21PaperIntentPrintSummary = false
InpLevel21PaperIntentRequireEntryBridgeReady = true
InpLevel21PaperIntentRequireDirectionalGeometry = true
InpLevel21PaperIntentExpiryBars = 20
InpLevel21PaperIntentFolder = "FlagCountingPhoenix"
```

## Source

Level 21 rebuilds the current Level 20 Entry Bridge row from the same inputs:

```text
rates
events
hooks
timebase report
render report
validation report
Level 20 config
```

Then it decides whether that bridge row can seed a paper intent.

## Intent fields

The output row records:

```text
intent_id
intent_key
allowed / blocked
intent_status
block_reason
source_bridge_key
source kind
source id
source level
source L
direction
entry price
stop price
target price
risk distance
reward distance
RR-like
entry / stop / target anchor ids
entry / stop / target anchor kinds
geometry status
lifecycle seed status
expiry bars
execution status
```

## Directional geometry

If enabled, Level 21 requires directional geometry:

For bullish intent:

```text
stop < entry < target
```

For bearish intent:

```text
target < entry < stop
```

If geometry fails, the row is blocked:

```text
PAPER_INTENT_BLOCKED_DIRECTIONAL_GEOMETRY
```

## Intent statuses

```text
PAPER_INTENT_ALLOWED_RESEARCH_ONLY
PAPER_INTENT_BLOCKED_ENTRY_BRIDGE_NOT_READY
PAPER_INTENT_BLOCKED_NO_DIRECTION
PAPER_INTENT_BLOCKED_NO_ENTRY_PRICE
PAPER_INTENT_BLOCKED_NO_STOP_PRICE
PAPER_INTENT_BLOCKED_NO_TARGET_PRICE
PAPER_INTENT_BLOCKED_ZERO_RISK
PAPER_INTENT_BLOCKED_ZERO_REWARD
PAPER_INTENT_BLOCKED_DIRECTIONAL_GEOMETRY
```

## Lifecycle seed status

Level 21 only seeds an intent.

It does not manage lifecycle yet.

The lifecycle seed can be:

```text
PAPER_INTENT_SEEDED_NOT_EXECUTED
PAPER_INTENT_BLOCKED_NOT_SEEDED
```

## Execution status

Every row explicitly remains non-executable:

```text
REAL_EXECUTION_DISABLED_LEVEL21_PAPER_INTENT_ONLY
```

## Relationship to Level 20

Level 20 answers:

```text
Do we have entry / invalidation / destination anchors?
```

Level 21 answers:

```text
Can those anchors seed a paper intent?
```

## Next correct layer

The next layer should be:

```text
Level 22 — Paper Intent Ledger / Intent History
```

or, if we want to move faster:

```text
Level 22 — Paper Lifecycle Close-Only
```

That next layer should track pending / touched / target / stop / expired states, still without broker orders.
