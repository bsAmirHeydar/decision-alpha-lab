# Stage 06 — Runtime Filter Engine

## Purpose

Stage 06 turns the Stage 05 dashboard from a luxury read-only surface into an interactive runtime control panel. The user can now click dashboard chips to mutate the in-memory filter state and force the chart timeline and dashboard to repaint immediately.

The stage deliberately does **not** persist filter changes to inputs. Inputs remain the boot preset. Runtime clicks are session-level overrides.

## Implementation Boundary

Stage 06 owns:

- dashboard object click routing;
- impact toggles;
- special-event toggles;
- currency toggles;
- utility presets;
- filter diagnostics;
- store metrics refresh after every filter mutation;
- dashboard/timeline repaint after every accepted click.

Stage 06 does not own:

- Forex Factory parsing;
- alert delivery internals;
- cache/fallback;
- licensing;
- persistent settings storage.

## Runtime Contract

```text
Input Preset -> GT_Config -> GT_FilterState -> Dashboard Click -> Filter Mutation -> Store Metrics -> Timeline/Dashboard Repaint
```

`GT_Config` is immutable after initialization. `GT_FilterState` is mutable.

## New Module

```text
mql5/include/GartalNewsFilters.mqh
```

Responsibilities:

- normalize currency CSV;
- add/remove CSV symbols safely;
- handle impact button clicks;
- handle special button clicks;
- handle currency chip clicks;
- handle utility preset clicks;
- write runtime diagnostics.

## New Inputs

```text
InpDashboardEnableClickFilters
InpDashboardCurrencyToggles
InpDashboardShowCurrencyButtons
InpDashboardShowFilterUtilities
InpDashboardClickRepaintsTimeline
```

## Dashboard Controls

### Impact Controls

- `RED ON/OFF`
- `ORANGE ON/OFF`
- `YELLOW ON/OFF`
- `HOL ON/OFF`

### Special Controls

- `SPEECH ON/OFF`
- `BREAK ON/OFF`
- `TENT ON/OFF`
- `PAST ON/OFF`
- `SYMBOL ON/OFF`

### Currency Controls

- USD
- EUR
- GBP
- JPY
- CHF
- CAD
- AUD
- NZD
- CNY

### Utility Controls

- `RED ONLY`
- `ALL IMP`
- `ALL CCY`
- `RESET`

## Redraw Contract

After a filter mutation:

1. `GT_UpdateStoreMetrics(g_store, g_filters)` recalculates visible count and next-event pointers.
2. `GT_RedrawAll()` repaints timeline and dashboard.
3. Runtime diagnostics store the last click object and filter summary.

## Safety Rules

- The dashboard never edits the store directly.
- A click must only mutate `GT_FilterState`.
- Empty currency filters are allowed at runtime because the user may intentionally hide all currencies.
- Reset restores boot-time input defaults.
- All chart object names stay inside the `GT_DASH_` namespace.

## Handoff to Stage 07

Stage 07 should read `filters.alerts_enabled` and the current visibility filters before firing alerts. The alert engine must not fire alerts for events hidden by runtime filters.
