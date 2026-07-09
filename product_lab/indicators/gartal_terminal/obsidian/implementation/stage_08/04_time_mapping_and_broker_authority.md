# 04 — Time Mapping and Broker Authority

Stage 08 parser must never render source time directly.

Canonical route:

```text
XML date/time
  -> source datetime
  -> GT_SourceToBrokerTime()
  -> event.time_broker
  -> timeline/dashboard/alerts
```

`event.time_broker` remains the only authority for downstream modules.

## Validation

Compare at least three known high-impact events against the Forex Factory calendar display and broker chart time before product release.
