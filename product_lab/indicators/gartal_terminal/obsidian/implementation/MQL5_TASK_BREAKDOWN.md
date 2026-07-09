---
type: engineering-task-breakdown
product: gartal terminal
status: planned
language: en
---

# MQL5 Task Breakdown — gartal terminal

## Main Indicator

### `GartalTerminal.mq5`

Responsibilities:

- declare indicator metadata
- initialize modules
- call fetch/parse/update pipeline on timer
- route chart events to dashboard
- cleanup chart objects

Must not contain:

- HTML parsing logic
- visual row layout internals
- alert channel internals
- source-specific assumptions

## Include Modules

### `GartalNewsTypes.mqh`

Tasks:

- [ ] add canonical enums
- [ ] add event struct
- [ ] add raw payload struct
- [ ] add runtime config struct
- [ ] add source status struct
- [ ] add alert stage struct

### `GartalNewsInputs.mqh`

Tasks:

- [ ] map MT5 inputs into runtime config
- [ ] support dashboard overrides
- [ ] expose active config getters
- [ ] add default presets

### `GartalNewsCalendarClient.mqh`

Tasks:

- [ ] source mode router
- [ ] sample raw provider
- [ ] WebRequest provider
- [ ] local cache provider
- [ ] source diagnostics

### `GartalNewsParser.mqh`

Tasks:

- [ ] parse sample payload
- [ ] normalize source fields
- [ ] assign impact enum
- [ ] detect speech/holiday/tentative/breaking flags
- [ ] build stable event IDs
- [ ] store parser errors

### `GartalNewsDashboard.mqh`

Tasks:

- [ ] create panel objects
- [ ] create filter chips
- [ ] create event rows
- [ ] update next-event hero
- [ ] handle object click events
- [ ] throttle redraws

### `GartalNewsTimeline.mqh`

Tasks:

- [ ] draw vertical event lines
- [ ] draw compact labels
- [ ] draw bottom timeline markers
- [ ] draw pre/post risk zones
- [ ] cleanup stale objects

### `GartalNewsAlerts.mqh`

Tasks:

- [ ] evaluate alert stages
- [ ] create dedupe keys
- [ ] dispatch popup/sound/push/email
- [ ] manage alert cooldown
- [ ] show alert status in dashboard

## Compile Priority

1. `Types`
2. `Inputs`
3. `Parser` with sample events
4. `Dashboard` minimal view
5. `Timeline` minimal lines
6. `Alerts` minimal popup
7. `CalendarClient` WebRequest path
8. `Cache`
9. UI polish

## Object Cleanup Rule

All chart objects created by the product must start with:

```text
GT_
```

On init, deinit, timeframe change, and source refresh, stale objects must be removed by prefix.

