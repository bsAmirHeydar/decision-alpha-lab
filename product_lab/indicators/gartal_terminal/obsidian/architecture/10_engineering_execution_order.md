---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - execution-order
  - build-plan
  - engineering
---

# 10 — Engineering Execution Order

## Objective

Convert architecture into a clean build sequence.

The sequence is designed to avoid the biggest MQL5 product failure: building UI first and then forcing data, time, filters, and alerts into a fragile monolith.

## Stage 0 — Architecture Freeze

Deliverables:

- architecture documents complete;
- module boundaries accepted;
- source strategy accepted;
- event struct accepted;
- dashboard behavior accepted.

Exit gate:

- no unresolved architectural contradiction;
- every subsystem has an owner module;
- acceptance gates are defined.

## Stage 1 — Compile-Safe Core Contracts

Implement:

- canonical enums;
- canonical structs;
- object prefix constants;
- config loader;
- sample data generator;
- event store clear/add/sort helpers.

Exit gate:

```text
GartalTerminal.mq5 compiles with sample data and no network.
```

## Stage 2 — Sample Pipeline

Implement:

- sample high/medium/low events;
- sample speech event;
- sample tentative event;
- sample breaking event;
- time normalization through the real normalizer;
- visible event view through the real filter engine.

Exit gate:

```text
Every renderer and alert module consumes the same sample event pipeline that real data will use.
```

## Stage 3 — Dashboard Shell

Implement:

- luxury dashboard container;
- header/status/footer;
- currency toggles;
- impact toggles;
- alert master toggle;
- compact event rows;
- next event highlight.

Exit gate:

```text
Dashboard filters mutate runtime filter state and rerender visible events without reopening MT5 inputs.
```

## Stage 4 — Timeline Renderer

Implement:

- vertical lines;
- impact-coded labels;
- bottom future timeline strip;
- stale object cleanup;
- no-flicker rerender policy.

Exit gate:

```text
Future events remain visible in the bottom timeline even if chart future space is limited.
```

## Stage 5 — Alert Engine

Implement:

- alert stage config;
- popup/sound/push/email channels;
- idempotency keys;
- dashboard alert state;
- release-time alert;
- actual-update alert skeleton.

Exit gate:

```text
Every alert stage fires once per event/channel and never repeats every timer tick.
```

## Stage 6 — Forex Factory Direct Adapter

Implement:

- WebRequest wrapper;
- configurable source URL;
- source status diagnostics;
- raw payload cache;
- parser extraction for current source markup;
- speech/breaking/tentative flags where available.

Exit gate:

```text
Live source fetch creates the same canonical event store as sample mode.
```

## Stage 7 — Cache & Resilience

Implement:

- cache save/load;
- fallback policy;
- stale cache warnings;
- retry backoff;
- no-alert-from-stale-cache default.

Exit gate:

```text
Network failure is visible, recoverable, and does not create false empty-day UI.
```

## Stage 8 — Product Polish

Implement:

- UI theme constants;
- row density modes;
- responsive spacing;
- chart-size reaction;
- dashboard collapse/expand;
- debug mode;
- customer-facing error text.

Exit gate:

```text
The product feels like a premium terminal, not a debug panel.
```

## Stage 9 — Packaging & Release

Implement:

- release script;
- customer install guide;
- versioned `.ex5` packaging path;
- changelog;
- QA checklist;
- licensing integration placeholder.

Exit gate:

```text
A tester can install and use the indicator from the release package without reading internal architecture docs.
```

## Stage 10 — Commercial Beta

Deliver:

- beta build;
- known limitations;
- tester instructions;
- feedback checklist;
- screenshots;
- sales description draft.

Exit gate:

```text
Product is ready for controlled external testing.
```

## Current Next Action

Start with Stage 1.

Do not touch live Forex Factory parsing yet.

The immediate coding task is:

```text
Create compile-safe core contracts + sample event pipeline.
```

## Definition of Done for First Code Patch

- `GartalTerminal.mq5` compiles;
- sample events exist;
- time normalizer runs;
- event store sorts;
- dashboard shows at least a simple event list;
- timeline draws at least high-impact vertical lines;
- no WebRequest required.
