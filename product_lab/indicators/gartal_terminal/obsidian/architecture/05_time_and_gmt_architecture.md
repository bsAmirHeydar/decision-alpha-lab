---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - broker-gmt
  - time-normalization
  - mt5
---

# 05 — Time & Broker GMT Architecture

## Goal

Every event must appear at the correct broker-chart time.

The product must support:

- manual broker GMT offset input;
- automatic broker GMT detection;
- source timezone normalization;
- chart-time rendering;
- dashboard display consistency;
- future timeline projection.

## Time Concepts

| Concept | Meaning | Owner |
|---|---|---|
| Source Time | Time shown by source calendar | Parser |
| Source GMT Offset | Offset assumed for source display | Config / Source Client |
| UTC Time | Canonical global event time | Time Normalizer |
| Broker Time | Time used by MT5 chart | Time Normalizer |
| Local Time | User PC time | diagnostics only |
| Display Time | What dashboard shows | Renderer config |

## Canonical Conversion

```text
source_time + source_gmt_offset -> utc_time
utc_time + broker_gmt_offset -> broker_time
```

## Broker GMT Manual Mode

Inputs:

```text
InpAutoDetectBrokerGMT = false
InpBrokerGMTOffsetHours = +3
```

The normalizer uses the manual offset directly:

```text
broker_time = utc_time + InpBrokerGMTOffsetHours
```

## Broker GMT Auto Mode

Inputs:

```text
InpAutoDetectBrokerGMT = true
```

Auto detection compares:

```text
TimeTradeServer() - TimeGMT()
```

This returns approximate broker offset in seconds.

Pseudo:

```cpp
int GT_DetectBrokerGmtOffsetMinutes()
{
   datetime server = TimeTradeServer();
   datetime gmt = TimeGMT();
   int diff_seconds = (int)(server - gmt);
   return (int)MathRound(diff_seconds / 60.0);
}
```

## DST Risk

Broker offsets may change due to daylight saving time.

Therefore:

- auto-detect should run on init;
- auto-detect should refresh at least once daily;
- dashboard diagnostics should show detected broker GMT;
- manual override must be available.

## Source Timezone Risk

Forex Factory can display times according to site/session settings.

The architecture must not assume source timezone invisibly. It must expose:

```text
InpSourceGMTOffsetHours
InpSourceTimeMode
```

Potential modes:

| Mode | Meaning |
|---|---|
| `SOURCE_TIME_UTC` | Source payload is UTC. |
| `SOURCE_TIME_CONFIGURED_OFFSET` | Source payload uses `InpSourceGMTOffsetHours`. |
| `SOURCE_TIME_SITE_PROFILE` | Future mode if adapter can enforce site timezone. |

## Today Window

The date window should be computed in broker time, not local PC time.

Default:

```text
broker_day_start = today 00:00 broker time
broker_day_end = today 23:59:59 broker time
```

For source fetching, this window may need conversion back to source day.

## Timeline Projection

Vertical event lines use `event.time_broker`.

Bottom strip uses the same broker time but maps it to chart pixel range.

## Display Diagnostics

Dashboard must show:

```text
Broker GMT: Auto +03:00
Source GMT: Configured +00:00
Last Sync: 14:23 broker
Next Event: 15:30 broker
```

## Time Failure Modes

| Failure | Cause | Required Behavior |
|---|---|---|
| News appears shifted | wrong source or broker offset | show GMT diagnostics; allow manual override |
| Today events missing near midnight | local day used instead of broker day | compute window in broker time |
| DST shift | broker changed offset | daily auto-detect refresh |
| Tentative event receives fake precision | source lacks exact time | mark tentative and render differently |

## Acceptance Gate

Time architecture is accepted when:

- sample UTC event renders at expected broker chart time;
- manual GMT offset overrides auto mode;
- auto mode displays detected offset;
- dashboard and chart line show the same time;
- events around midnight do not disappear incorrectly.
