# Gartal Terminal — Stage 02 Core Specification

## Stage

`Stage 02 — News Event Data Model + Sample Data Pipeline`

## Objective

Create a production-shaped internal event model before implementing the external Forex Factory adapter.

## Scope

### In scope

- canonical `GT_NewsEvent` expansion;
- central `GT_NewsStore` metrics;
- deterministic full-day sample tape;
- same-minute event sorting;
- speech/holiday/tentative/breaking classification;
- upcoming/active/released/expired status lifecycle;
- visible count and next-event index;
- dashboard and timeline consumption of store metrics.

### Out of scope

- real Forex Factory HTML parser;
- cache layer;
- final luxury dashboard interaction;
- production alert state machine;
- release packaging.

## Acceptance criteria

1. Sample mode loads a non-empty event tape.
2. Events are sorted by broker time and impact priority.
3. Store metrics match the loaded event mix.
4. Event visibility is controlled by configured filters.
5. The dashboard displays Stage 02 lifecycle counts.
6. The timeline displays an upcoming event tape.
7. Stage 03 can work on time normalization without changing the event contract.
