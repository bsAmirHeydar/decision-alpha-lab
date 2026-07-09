# Stage 05 — Luxury Dashboard UI Renderer

## Objective

Stage 05 upgrades `gartal terminal` from a technical chart overlay into a sellable macro-news terminal surface. The dashboard becomes the product's primary operating panel: it communicates source health, broker-time alignment, next-event risk, red-event urgency, today metrics, active filters, and the upcoming news tape.

## Scope

This stage implements the visual dashboard layer only. It does not mutate runtime filters yet. Clickable filter behavior is reserved for Stage 06.

## Engineering Principle

The dashboard must consume already-normalized state. It must not parse news, sort events, infer timezone, or decide canonical truth. Its only responsibilities are:

```text
GT_NewsStore + GT_FilterState + GT_RuntimeState + GT_Config
        -> dashboard objects
        -> live countdown repaint
        -> operator diagnostics
```

## Delivered Modules

- `GartalNewsDashboardTheme.mqh`
- `GartalNewsDashboard.mqh`
- Stage 05 inputs in `GartalNewsInputs.mqh`
- Stage 05 dashboard runtime diagnostics in `GartalNewsTypes.mqh`
- timer-driven countdown repaint in `GT_UpdateCountdowns()`

## Dashboard Sections

1. Brand header
2. Health badge
3. Source and GMT strip
4. Next event card
5. Next red-event card
6. Impact metrics
7. Filter preview badges
8. Upcoming mini tape
9. Event table
10. Debug footer

## Non-Goals

- No Forex Factory live adapter
- No dashboard filter toggles
- No alert state-machine completion
- No licensing
- No drag/drop dashboard movement

## Handoff

Stage 06 will reuse the object namespace and badge layout to turn the filter preview into actual runtime controls.
