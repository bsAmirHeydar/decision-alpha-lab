# STAGE 03 — Broker GMT / Time Normalization Engine

## Scope

This stage implements the canonical time normalization layer for gartal terminal.

## Inputs

- `InpBrokerGMTMode`
- `InpAutoDetectBrokerGMT`
- `InpBrokerGMTOffsetHours`
- `InpBrokerGMTOffsetMinutes`
- `InpSourceTimeMode`
- `InpSourceGMTOffsetHours`
- `InpSourceGMTOffsetMinutes`
- `InpTimeShiftMinutes`
- `InpSampleTimeMode`
- `InpShowTimeDebug`

## Core API

```text
GT_NormalizeConfigTime()
GT_DetectBrokerGmtOffsetSeconds()
GT_UtcToBrokerTime()
GT_BrokerToUtcTime()
GT_SourceToBrokerTime()
GT_BrokerToSourceTime()
GT_ConfiguredSampleBrokerTime()
GT_UpdateEventTimeFields()
GT_ConfigWindowFromBroker()
GT_ConfigWindowToBroker()
```

## Non-goals

- no Forex Factory parser yet
- no interactive dashboard filter mutation yet
- no advanced DST database
- no external timezone service

## Acceptance

The terminal must place sample events using broker-time authority and expose enough diagnostics for a user to verify the time configuration visually.
