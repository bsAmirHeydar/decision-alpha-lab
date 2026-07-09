# Stage 03 Index — Broker GMT / Time Normalization

## Read order

1. [[01_time_authority_contract]]
2. [[02_broker_gmt_detection]]
3. [[03_source_utc_broker_conversion]]
4. [[04_date_window_model]]
5. [[05_sample_time_modes]]
6. [[06_dashboard_time_diagnostics]]
7. [[07_validation_checklist]]
8. [[08_handoff_to_stage_04]]

## Stage status

```text
Stage: 03
Name: Broker GMT / Time Normalization Engine
Coding status: implemented as MQL5 scaffold/core
External source status: not active yet
Primary risk: broker GMT mismatch and DST assumptions
Next stage: Chart Timeline Renderer
```

## Core files

```text
mql5/include/GartalNewsTime.mqh
mql5/include/GartalNewsInputs.mqh
mql5/include/GartalNewsTypes.mqh
mql5/include/GartalNewsStore.mqh
mql5/include/GartalNewsSampleData.mqh
mql5/include/GartalNewsDashboard.mqh
mql5/include/GartalNewsTimeline.mqh
```
