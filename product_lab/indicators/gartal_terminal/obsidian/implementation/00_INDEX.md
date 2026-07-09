# Gartal Terminal — Implementation Index

## Current coding path

```text
Stage 01 — Compile-Safe Core Skeleton              DONE
Stage 02 — News Event Data Model + Sample Pipeline DONE
Stage 03 — Broker GMT / Time Normalization Engine  DONE
Stage 04 — Chart Timeline Renderer                 DONE
Stage 05 — Luxury Dashboard UI Renderer             NEXT
Stage 06 — Runtime Filter Engine
Stage 07 — Alert Engine + State Machine
Stage 08 — Forex Factory Client + HTML Parser
Stage 09 — Cache / Fallback / Resilience Layer
Stage 10 — Product Hardening + Packaging
```

## Stage notes

- [[stage_01_compile_safe_core_skeleton]]
- [[stage_02_event_data_model_sample_pipeline]]
- [[stage_03_broker_gmt_time_normalization]]
- [[stage_04_chart_timeline_renderer]]

## Stage folders

- [[stage_01/00_STAGE_01_INDEX]]
- [[stage_02/00_STAGE_02_INDEX]]
- [[stage_03/00_STAGE_03_INDEX]]
- [[stage_04/00_STAGE_04_INDEX]]

## Engineering doctrine

Each stage must produce a compile-oriented increment, update the Obsidian implementation map, and leave a narrow handoff contract for the next stage.

- [[stage_04_chart_timeline_renderer]] — Chart timeline renderer, labels, zones, projection, and cleanup.

- [[stage_05_luxury_dashboard_ui_renderer]] — Luxury terminal dashboard, next-event cards, metrics, health strip, filter preview, and live countdown surface.
