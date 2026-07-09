---
title: Gartal Terminal — Stage 02 Event Data Model + Sample Pipeline
type: implementation-master-note
stage: 02
status: implemented
---

# Stage 02 — Event Data Model + Sample Data Pipeline

Stage 02 upgrades `gartal terminal` from a compile-safe shell into a deterministic news-event engine.

The product still runs in sample mode by default. This is deliberate. The core product should prove that event modeling, sorting, status handling, impact classification, symbol relevance, dashboard metrics, and timeline consumption work before the fragile external HTML parser is attached.

## Engineering target

```text
Input settings
  -> sample event generation
  -> canonical GT_NewsEvent rows
  -> GT_NewsStore finalization
  -> sorted event tape
  -> status lifecycle
  -> metrics and next-event pointers
  -> dashboard/timeline/alerts consume one shared truth
```

## Added modules

```text
GartalNewsStore.mqh
GartalNewsSampleData.mqh
```

## Updated modules

```text
GartalTerminal.mq5
GartalNewsTypes.mqh
GartalNewsUtils.mqh
GartalNewsInputs.mqh
GartalNewsTime.mqh
GartalNewsParser.mqh
GartalNewsDashboard.mqh
GartalNewsTimeline.mqh
```

## Stage 02 doctrine

- No rendering module owns event truth.
- No alert module owns event truth.
- No parser module owns event truth after parsing.
- All modules consume `GT_NewsEvent` and `GT_NewsStore`.
- External source risk is postponed until the internal model is stable.

## Obsidian map

See [[stage_02/00_STAGE_02_INDEX]].
