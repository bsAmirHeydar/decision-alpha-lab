---
type: architecture-entry
product: gartal terminal
status: active
language: en
tags:
  - gartal-terminal
  - architecture
  - mt5
  - news-terminal
  - forex-factory
---

# Gartal Terminal — Architecture Start

This note is the engineering entry point for building **gartal terminal** as a sellable MT5 macro-news terminal.

The product must behave like a professional economic calendar overlay:

- render today's scheduled events on the chart;
- display event time, impact color, currency, title, forecast, previous, actual, and status;
- support sudden high-impact items such as political speeches or breaking remarks when the data source exposes them;
- draw future events on the chart timeline before price reaches those times;
- provide a luxury dashboard with all filters editable from the chart;
- support configurable broker GMT offset and automatic detection;
- provide multiple alert modes without creating duplicate alerts;
- remain maintainable when the Forex Factory HTML changes.

## Read Order

1. [[architecture/00_ARCHITECTURE_INDEX|Architecture Index]]
2. [[architecture/01_system_architecture|System Architecture]]
3. [[architecture/02_mql5_module_contracts|MQL5 Module Contracts]]
4. [[architecture/03_data_pipeline_and_source_strategy|Data Pipeline & Source Strategy]]
5. [[architecture/04_forex_factory_parsing_contract|Forex Factory Parsing Contract]]
6. [[architecture/05_time_and_gmt_architecture|Time & Broker GMT Architecture]]
7. [[architecture/06_ui_runtime_filter_architecture|UI Runtime Filter Architecture]]
8. [[architecture/07_alert_state_machine|Alert State Machine]]
9. [[architecture/08_chart_rendering_object_model|Chart Rendering Object Model]]
10. [[architecture/09_error_cache_resilience_architecture|Error, Cache & Resilience Architecture]]
11. [[architecture/10_engineering_execution_order|Engineering Execution Order]]

## Architecture Rule

The indicator must not become a monolithic `.mq5` file.

`GartalTerminal.mq5` is only the orchestrator. Every product capability must live behind one of these module boundaries:

```text
Inputs -> Source Client -> Parser -> Normalizer -> Store -> Filter -> Renderer -> Alert Engine
```

Any feature that crosses these boundaries directly is considered architectural debt.

## Target Product Feel

The UX target is not a raw calendar table. The product must feel like a **terminal**:

- glass/dark dashboard surfaces;
- impact-coded rows;
- compact and expanded row modes;
- next-event emphasis;
- bottom future timeline strip;
- chart event markers with clean labels;
- one-click dashboard toggles;
- graceful failure display when source/cache is unavailable;
- zero noisy object flickering.

## Implementation Bias

Build from stable contracts first, not from UI first.

The correct order is:

1. compile-safe contracts;
2. sample-data pipeline;
3. source adapter;
4. parser;
5. broker-time normalization;
6. filter engine;
7. dashboard;
8. timeline;
9. alerts;
10. cache;
11. packaging/licensing.
