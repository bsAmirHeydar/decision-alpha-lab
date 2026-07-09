# 02 — Cycle Group Calendar

## 1. Purpose

The cycle calendar converts broker server time into New York trading-day coordinates, then assigns each closed chart candle to one or more cycle groups.

Every supported cycle group starts at the same anchor:

```text
18:00 New York time
```

The current trading day ends at:

```text
17:00 New York time, next calendar day
```

The active analysis window is therefore:

```text
18:00 <= NY time < 17:00 next day
```

This is 1380 minutes.

## 2. Time conversion contract

MQL5 server time is broker time. The EA must map broker time to New York time.

Baseline inputs:

```text
input int InpBrokerUtcOffsetHours = 3;
input int InpNewYorkUtcOffsetHours = -4;
```

Recommended derived conversion:

```text
broker_to_utc = broker_time - InpBrokerUtcOffsetHours
ny_time       = utc_time + InpNewYorkUtcOffsetHours
```

Because New York alternates between UTC-5 and UTC-4 depending on daylight saving time, the expert should expose `InpNewYorkUtcOffsetHours` as an input rather than hardcoding it.

Recommended operational defaults:

| Season | New York offset | Broker default | Broker minus NY |
|---|---:|---:|---:|
| NY daylight time | UTC-4 | UTC+3 | 7 hours |
| NY standard time | UTC-5 | UTC+3 | 8 hours |

The user requested broker default UTC+3, so `InpBrokerUtcOffsetHours = 3` is the baseline default.

## 3. Trading-day key

For a New York timestamp, the trading-day key is not the calendar date directly.

Rules:

```text
If NY time >= 18:00:
    trading_day_key = NY calendar date of timestamp
Else:
    trading_day_key = NY calendar date of timestamp - 1 day
```

Example:

```text
2026-07-09 18:10 NY => trading day 2026-07-09
2026-07-10 02:30 NY => trading day 2026-07-09
2026-07-10 16:59 NY => trading day 2026-07-09
2026-07-10 17:05 NY => outside trading day / post-session boundary
```

## 4. Minute offset from day start

Once the trading-day start is known:

```text
minutes_from_day_start = floor((ny_time - trading_day_start_18_00) / 60)
```

Valid range:

```text
0 <= minutes_from_day_start < 1380
```

If outside that range, no new signal should be generated.

## 5. Cycle index

For a cycle group duration `D` minutes:

```text
cycle_index = floor(minutes_from_day_start / D)
cycle_start_offset = cycle_index * D
cycle_end_offset = min((cycle_index + 1) * D, 1380)
```

Cycle start/end in NY time:

```text
cycle_start = trading_day_start + cycle_start_offset minutes
cycle_end   = trading_day_start + cycle_end_offset minutes
```

## 6. Incomplete final cycles

Because the trading day is 1380 minutes, some cycle durations do not divide the day evenly.

For those groups, the final cycle is incomplete and ends at 17:00 NY.

Example for `cg_720m`:

```text
Cycle 0: 18:00–05:59  => 720 minutes
Cycle 1: 06:00–16:59  => 660 minutes, incomplete final cycle
```

The final cycle is still valid. It can detect and trade divergence, but target time remains the end of that cycle, which is 17:00 NY.

## 7. Full cycle group table

| CG | Duration | Cycles per 23h day | Final cycle status |
|---|---:|---:|---|
| cg_3m | 3 | 460 | complete |
| cg_5m | 5 | 276 | complete |
| cg_9m | 9 | 154 | incomplete final cycle |
| cg_10m | 10 | 138 | complete |
| cg_15m | 15 | 92 | complete |
| cg_18m | 18 | 77 | incomplete final cycle |
| cg_20m | 20 | 69 | complete |
| cg_24m | 24 | 58 | incomplete final cycle |
| cg_30m | 30 | 46 | complete |
| cg_40m | 40 | 35 | incomplete final cycle |
| cg_45m | 45 | 31 | incomplete final cycle |
| cg_60m | 60 | 23 | complete |
| cg_72m | 72 | 20 | incomplete final cycle |
| cg_90m | 90 | 16 | incomplete final cycle |
| cg_120m | 120 | 12 | incomplete final cycle |
| cg_150m | 150 | 10 | incomplete final cycle |
| cg_180m | 180 | 8 | incomplete final cycle |
| cg_240m | 240 | 6 | incomplete final cycle |
| cg_300m | 300 | 5 | incomplete final cycle |
| cg_360m | 360 | 4 | incomplete final cycle |
| cg_720m | 720 | 2 | incomplete final cycle |

`Cycles per 23h day` means the count of cycle slots created by ceiling division:

```text
ceil(1380 / duration)
```

## 8. Reference availability

The first cycle of any CG has no previous completed cycle.

Baseline reference rule:

```text
current_cycle_index must be >= 1
reference_cycle_index = current_cycle_index - 1
```

Therefore, no divergence can be created in cycle 0 for that CG.

## 9. Multi-CG concurrency

A single chart candle can belong to one active cycle in every enabled cycle group.

Therefore one closed candle may produce multiple CG signals:

```text
cg_5m bullish divergence
cg_30m bearish divergence
cg_180m bullish divergence
...
```

The EA must treat them as independent signal channels. Each CG has its own:

- trade enabled flag;
- draw enabled flag;
- draw color;
- reference cycle;
- duplicate prevention key;
- cycle-end exit schedule.

## 10. Calendar module responsibilities

The `CycleCalendar` module should provide at least:

```text
bool IsInsideTradingDay(datetime broker_time)
bool BuildCycleContext(datetime broker_time, int duration_minutes, CycleContext &out)
datetime TradingDayStartNY(datetime ny_time)
datetime TradingDayEndNY(datetime ny_time)
int MinutesFromDayStart(datetime ny_time)
int CycleIndex(int minutes_from_start, int duration)
datetime CycleStartBroker(CycleContext ctx)
datetime CycleEndBroker(CycleContext ctx)
```

The rest of the strategy should not perform raw timezone arithmetic.

