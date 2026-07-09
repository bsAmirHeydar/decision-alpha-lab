---
type: sprint-roadmap
product: gartal terminal
status: planned
language: en
---

# Phase 11 — Next Build Sprints

## Sprint Strategy

The build must move from stable skeleton to visible product fast. Do not start with the hardest live-source parsing problem. First make the terminal visually and architecturally correct with sample data, then connect the real adapter.

## Sprint 01 — Compile-Safe Product Skeleton

### Goal

Make `GartalTerminal.mq5` compile with sample data and a minimal visible dashboard.

### Tasks

- [ ] Validate include paths.
- [ ] Fix any MQL5 syntax issues in scaffold modules.
- [ ] Implement sample event array.
- [ ] Render event count and next event.
- [ ] Clean all `GT_` objects on init/deinit.

### Done

A chart can load the indicator and show a minimal `gartal terminal` panel without internet.

## Sprint 02 — Dashboard Filter Controls

### Goal

Make dashboard filters interactive.

### Tasks

- [ ] Add currency chip buttons.
- [ ] Add impact chip buttons.
- [ ] Add event-type chip buttons.
- [ ] Handle `OnChartEvent` clicks.
- [ ] Rebuild visible event set after toggles.

### Done

User can hide/show USD, EUR, high/medium/low, speeches, and breaking events from the chart.

## Sprint 03 — Chart Timeline

### Goal

Draw future news on the chart.

### Tasks

- [ ] Draw vertical lines by `broker_time`.
- [ ] Draw compact labels.
- [ ] Draw bottom timeline strip.
- [ ] Add risk windows before/after news.
- [ ] Handle timeframe changes cleanly.

### Done

All selected events until end of day are visible ahead of price action.

## Sprint 04 — Broker GMT Engine

### Goal

Make time conversion transparent and debuggable.

### Tasks

- [ ] Add manual GMT offset.
- [ ] Add auto-detection diagnostic.
- [ ] Display active offset in dashboard.
- [ ] Test around midnight.
- [ ] Test with sample events across time zones.

### Done

User can trust why an event is plotted at a specific broker-chart time.

## Sprint 05 — Alert Engine

### Goal

Add staged alerts without spam.

### Tasks

- [ ] Add alert stages.
- [ ] Add event-stage dedupe keys.
- [ ] Add popup/sound/push/email flags.
- [ ] Add dashboard alert toggles.
- [ ] Add test alert action.

### Done

Enabled alerts fire once per event stage and respect dashboard filters.

## Sprint 06 — Forex Factory Adapter

### Goal

Connect the real source through the isolated calendar adapter.

### Tasks

- [ ] Implement WebRequest fetch.
- [ ] Add source diagnostics.
- [ ] Implement raw payload capture.
- [ ] Implement parser fixtures.
- [ ] Convert raw payload to normalized events.

### Done

Live events flow into the same dashboard/timeline/alert pipeline as sample events.

## Sprint 07 — Cache & Failover

### Goal

Keep the product useful when source access fails.

### Tasks

- [ ] Save raw payload cache.
- [ ] Load cache on failure.
- [ ] Display cache age.
- [ ] Add stale-cache warning.
- [ ] Add manual refresh button.

### Done

Network/source failure does not make the terminal blank or misleading.

## Sprint 08 — Luxury UI Pass

### Goal

Move from functional dashboard to premium sellable interface.

### Tasks

- [ ] Add refined spacing and typography ratios.
- [ ] Add premium color theme.
- [ ] Add compact/full mode polish.
- [ ] Add next-event hero panel polish.
- [ ] Add table row hierarchy.
- [ ] Add edge-case label compression.

### Done

The product looks good enough for screenshots, marketing, and beta users.

## Sprint 09 — Package & Beta Release

### Goal

Create a distributable beta build.

### Tasks

- [ ] Compile `.ex5`.
- [ ] Prepare release folder.
- [ ] Add quick-start docs.
- [ ] Add WebRequest setup guide.
- [ ] Add known-issues file.
- [ ] Add versioned changelog.

### Done

A beta user can install and understand the product without developer help.

## Recommended Next Action

Start with Sprint 01 and force a compile. Any architecture that does not compile is still fiction.

