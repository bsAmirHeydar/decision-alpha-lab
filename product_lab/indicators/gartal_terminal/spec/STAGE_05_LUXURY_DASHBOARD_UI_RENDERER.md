# STAGE 05 — Luxury Dashboard UI Renderer Specification

## Objective

Build the commercial dashboard surface for `gartal terminal`. This stage transforms the product from a diagnostic chart renderer into a premium macro terminal.

## Non-Goals

- No Forex Factory adapter implementation.
- No filter click mutation.
- No final alert state-machine expansion.
- No license enforcement.

## Inputs Added

```text
InpDashboardMode
InpDashboardWidth
InpDashboardRowHeight
InpDashboardShowHeader
InpDashboardShowNextCard
InpDashboardShowHighCard
InpDashboardShowMetrics
InpDashboardShowFilterBar
InpDashboardShowHealthBar
InpDashboardShowEventTable
InpDashboardShowMiniTape
InpDashboardLuxuryTheme
InpDashboardBgColor
InpDashboardPanelColor
InpDashboardBorderColor
InpDashboardTextColor
InpDashboardMutedColor
InpDashboardAccentColor
```

## New Module

### GartalNewsDashboardTheme.mqh

Owns dashboard mode names, theme colors, health badge semantics, dashboard height calculation, countdown formatting, and table row formatting.

## Updated Module

### GartalNewsDashboard.mqh

Now renders:

- premium header
- health badge
- source/GMT strip
- next event card
- next red-event card
- impact metric cards
- filter preview badges
- mini upcoming tape
- structured event table
- debug footer

## Runtime Diagnostics

`GT_RuntimeState` now tracks:

```text
dashboard_last_objects
dashboard_last_rows
dashboard_last_cards
dashboard_last_render_at
dashboard_last_render_summary
```

## Success Criteria

- Dashboard remains stable across timer ticks.
- Countdown updates without full timeline redraw.
- The UI communicates source status and broker-time status clearly.
- Next and next-red cards use store pointers only.
- Stage 04 timeline behavior remains unchanged.
