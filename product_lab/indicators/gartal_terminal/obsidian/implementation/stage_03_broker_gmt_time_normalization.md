# Stage 03 — Broker GMT / Time Normalization Engine

## Purpose

Stage 03 turns `gartal terminal` from a visually rendered sample calendar into a time-correct news terminal. The product must place every event on the chart at the broker-time location where the trader actually sees candles. This stage defines and implements the canonical conversion path between source time, UTC time, and broker time.

## Final Contract

```text
source calendar time -> UTC -> broker time -> chart object time -> alert schedule
```

Every downstream system must consume `event.time_broker` only:

- dashboard rows
- vertical chart lines
- bottom timeline
- next-event countdown
- alert thresholds
- future filter engine
- cache replay

`event.time_source` and `event.time_utc` are kept for audit/debugging, not rendering authority.

## What changed in code

- `GT_Config` now contains canonical offset fields in seconds.
- `GT_RuntimeState` now contains broker/server/UTC diagnostic snapshots.
- `GartalNewsTime.mqh` now owns all source/UTC/broker conversion.
- `GartalNewsStore.mqh` now calls `GT_UpdateEventTimeFields()` when an event is inserted.
- `GartalNewsSampleData.mqh` can anchor sample events in broker, source, or UTC time.
- Dashboard and timeline now display effective broker GMT, detected GMT, source mode, and date window.

## User-facing inputs

```text
InpBrokerGMTMode          0 Auto, 1 Manual, 2 Hybrid
InpAutoDetectBrokerGMT    legacy compatibility toggle
InpBrokerGMTOffsetHours   manual broker offset hours
InpBrokerGMTOffsetMinutes manual broker offset minutes
InpSourceTimeMode         0 UTC, 1 Broker, 2 Manual Source GMT
InpSourceGMTOffsetHours   source offset hours when manual source mode is used
InpSourceGMTOffsetMinutes source offset minutes when manual source mode is used
InpTimeShiftMinutes       emergency correction after normalization
InpSampleTimeMode         0 Broker, 1 Source, 2 UTC
InpShowTimeDebug          shows diagnostic time row in dashboard
```

## Execution position

Stage 03 sits before real Forex Factory parsing because source integration is worthless unless the conversion contract is stable. The future parser will emit source timestamps; this stage converts them safely into broker chart timestamps.

## Handoff to Stage 04

Stage 04 must treat time as solved. It should not introduce new conversion logic. It should only render objects using `event.time_broker` and should use `event.day_offset`, `event.minute_of_day`, and `store.window_from_broker/window_to_broker` for placement and cleanup.
