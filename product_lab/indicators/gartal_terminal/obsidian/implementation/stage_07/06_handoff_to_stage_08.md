# 06 — Handoff to Stage 08

Stage 08 can now focus on source ingestion.

The Forex Factory parser must fill these fields correctly:

```text
time_source
time_utc
time_broker
currency
impact
title
actual
forecast
previous
is_tentative
is_speech
is_holiday
is_breaking
source
raw_hash
```

Once parser output enters the store, Stage 07 alert behavior should work without parser-specific changes.
