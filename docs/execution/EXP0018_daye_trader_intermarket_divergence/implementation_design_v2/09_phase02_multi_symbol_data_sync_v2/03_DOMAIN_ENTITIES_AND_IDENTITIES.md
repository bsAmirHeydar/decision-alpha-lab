---
id: EXP0018-P02-ENTITIES
title: "P02 Domain Entities and Identities"
type: contract
status: active
project: EXP0018
---
# موجودیت‌ها و هویت‌ها

## Symbol Descriptor

هویت broker symbol و canonical symbol را جدا نگه می‌دارد. `NDXUSD.a` می‌تواند broker symbol باشد و `NDX` canonical ID باقی بماند.

## Symbol Bar

یک bar نمادمحلی با:

- broker open time
- UTC event time
- New York event time
- close availability time
- OHLC/volume/spread
- completeness
- replay-safety

## Synchronized Pair

کلید:

```text
EXP0018|P02|<TIMEFRAME>|<EVENT_TIME_UTC>|<CANONICAL_A>|<CANONICAL_B>
```

Pair فقط وقتی وجود دارد که هر دو bar exact timestamp یکسان داشته باشند.
