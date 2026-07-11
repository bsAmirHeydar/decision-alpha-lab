---
title: "MQL5 API Reference"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Aggregate include

```mql5
#include <AlphaLab\StrategyFactory\Market\SF03_AllMarket.mqh>
```

## Typical composition

```mql5
CSF03MarketServiceBundle services;

SF03_ClockConfig clock;
clock.mode = SF03_CLOCK_SERVER_FIXED_OFFSET;
clock.broker_utc_offset_minutes = 120;
clock.broker_timezone_id = "broker_fixed";
clock.source_clock_id = "terminal";

string error = "";
services.Initialize(runtime_config, clock, error);
services.Start(error);
services.Market().RegisterSeries("#NQ", 60, error);
```

## Read state

```mql5
MqlTick tick;
services.Market().LatestTick("#NQ", tick, error);

SF01_BarRecord bar;
services.Market().LatestClosedBar("#NQ", 60, bar, error);

SF02_SymbolSpec spec;
services.Specs().Get("#NQ", spec, error);
```

## Synchronization

Create one `SF03_SyncRequirement` per required series, then call `EvaluateSynchronization`.

## Sessions

Add `SF03_SessionDefinition` records to `CSF03SessionSchedule`; resolve against a UTC timestamp and the shared time kernel.

## Testing

Use `CSF03FixtureMarketSource` to inject ticks, bars, and symbol specifications without terminal access.

## Authority warning

These APIs expose market and metadata truth only. They do not create candidates, size positions, or send orders.
