---
title: Gartal Terminal — Stage 02 Index
type: implementation-index
stage: 02
status: implemented
---

# Stage 02 — Event Data Model + Sample Data Pipeline

Stage 02 turns the Stage 01 compile-safe shell into a deterministic news-event runtime. The terminal still does **not** depend on Forex Factory network parsing. Instead, it uses a production-shaped sample tape so every downstream layer can be built and tested before the external source is attached.

## Start here

1. [[01_event_schema_contract]]
2. [[02_store_lifecycle]]
3. [[03_sample_data_tape]]
4. [[04_sorting_status_metrics]]
5. [[05_filter_compatibility]]
6. [[06_validation_checklist]]
7. [[07_handoff_to_stage_03]]

## Implementation files

```text
mql5/GartalTerminal.mq5
mql5/include/GartalNewsTypes.mqh
mql5/include/GartalNewsUtils.mqh
mql5/include/GartalNewsInputs.mqh
mql5/include/GartalNewsTime.mqh
mql5/include/GartalNewsStore.mqh
mql5/include/GartalNewsSampleData.mqh
mql5/include/GartalNewsParser.mqh
mql5/include/GartalNewsDashboard.mqh
mql5/include/GartalNewsTimeline.mqh
```

## Completion definition

Stage 02 is complete when:

- the indicator compiles with sample mode enabled;
- the event store loads deterministic today-focused events;
- events carry status, kind, relevance, impact rank, minute-of-day, and date-window fields;
- dashboard counts and next-event pointers are computed by the store;
- the timeline can read a sorted upcoming event tape;
- later stages can build time normalization, UI, filters, alerts, parser, and cache on the same event contract.
