---
title: "Indicator Input Groups and Configuration Plan"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Indicator Input Groups and Configuration Plan

## Input groups

### Identity and symbols

- Context instance name.
- Symbol A and Symbol B.
- Symbol-role display labels.
- Optional automatic pair resolution.

### Time and windows

- New York timezone policy version.
- A/L/N session definitions from frozen registry.
- Confirmation timeframe (`PERIOD_CURRENT` resolved at init or explicit timeframe).
- Calendar-day N lookback depth.
- Weekly lookback depth.

### Relation enablement

- Enable AL, AN, LN, NA, NL, NN, WW independently.
- Direction filter: both/bullish/bearish.
- Historical display depth per relation family.

### Visuals

- Indicator mode: Audit/Trading/WW/Relation/Diagnostic.
- Session boxes, reference lines, hunt markers, connectors, labels, panel.
- Color/style/thickness registry override policy.
- Object cleanup behavior.
- Maximum displayed historical objects.

### Alerts and exports

- Enable popup/sound/push/email.
- Alert states and relation filters.
- Export mode/path/flush interval.
- Suppress historical rebuild alerts by default.

### Performance

- Timer interval.
- Maximum M1 backfill batch.
- Checkpoint interval.
- Render batch size.
- Diagnostic telemetry level.

## Configuration hashing

Behavior-bearing fields must enter the context/config hash. Pure presentation fields enter a separate projection hash. This distinction allows a style change without generating new signal IDs while ensuring relation/time/confirmation changes create a new semantic epoch.

## Reinitialization policy

| Input change | Required action |
|---|---|
| symbol/time/session/relation/confirmation | full semantic reinitialize |
| calendar/weekly depth | bounded backfill and semantic rebuild |
| visual style/filter | projection-only rebuild |
| alert/export policy | router reconfigure; signal IDs unchanged |
| performance batch/timer | runtime reconfigure; semantic IDs unchanged |
