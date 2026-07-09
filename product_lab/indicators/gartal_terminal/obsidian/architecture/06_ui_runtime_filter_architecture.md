---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - ui
  - dashboard
  - filters
  - runtime-config
---

# 06 — UI Runtime Filter Architecture

## Goal

The dashboard must act as the product control center.

Users should not need to reopen MT5 indicator inputs to change common filters.

## UI Philosophy

The dashboard is a terminal surface, not a settings dump.

Design goals:

- one-glance event awareness;
- one-click filter toggles;
- clear next-event emphasis;
- visible alert status;
- broker/source status always visible;
- premium dark/glass styling;
- no object flicker.

## Dashboard Zones

```text
+------------------------------------------------+
| Brand / Status / Time / Source Health          |
+------------------------------------------------+
| Currency Toggles: USD EUR GBP JPY CHF CAD ...  |
+------------------------------------------------+
| Impact Toggles: Red Orange Yellow Speech ...   |
+------------------------------------------------+
| Alert Controls: Popup Sound Push Email         |
+------------------------------------------------+
| Event Rows                                     |
| 15:30 USD RED Non-Farm Employment Change       |
| 17:00 USD RED Fed Chair Speaks                 |
+------------------------------------------------+
| Footer: Next Event / Refresh / Cache / GMT     |
+------------------------------------------------+
```

## Runtime Filter State

Runtime dashboard filters are separate from input config.

```cpp
struct GT_FilterState
{
   string currencies_csv;
   bool show_low;
   bool show_medium;
   bool show_high;
   bool show_holiday;
   bool show_speech;
   bool show_tentative;
   bool show_breaking;
   bool only_symbol;
   bool alerts_enabled;
};
```

## Click Routing

Each clickable object must encode action:

```text
GT_DASH_BTN_CUR_USD
GT_DASH_BTN_IMPACT_HIGH
GT_DASH_BTN_SPEECH
GT_DASH_BTN_ALERT_POPUP
GT_DASH_BTN_REFRESH
GT_DASH_BTN_COMPACT
```

Click handler:

```text
object name -> action -> mutate GT_FilterState -> recompute visible view -> rerender
```

## Filter Semantics

An event is visible if:

```text
currency_pass && impact_pass && flag_pass && date_window_pass && symbol_pass
```

### Currency Pass

```text
show event if event.currency is enabled in runtime filter
```

### Impact Pass

```text
high events require show_high
medium events require show_medium
low events require show_low
holiday events require show_holiday
```

### Speech/Breaking Pass

Speech and breaking are overlays, not standalone currencies.

A high-impact speech requires:

```text
show_high == true AND show_speech == true
```

Breaking event requires:

```text
show_breaking == true
```

Impact filter still applies unless product mode explicitly overrides it.

## Symbol-Aware Mode

If enabled, symbol detection extracts currencies from chart symbol.

Examples:

| Symbol | Relevant Currencies |
|---|---|
| EURUSD | EUR, USD |
| GBPJPY | GBP, JPY |
| XAUUSD | USD |
| US30 | USD |
| BTCUSD | USD, BTC if supported later |

For gold, no XAU economic calendar is needed. XAUUSD should default to USD macro relevance.

## Row Density Modes

| Mode | Purpose |
|---|---|
| Compact | time, currency, impact, short title |
| Normal | plus forecast/previous/actual |
| Full | plus countdown, flags, source status |

## Visual State Rules

| Event State | UI Treatment |
|---|---|
| Past | dimmed |
| Next | highlighted border/glow |
| High Impact | red dot/stripe |
| Medium Impact | orange dot/stripe |
| Low Impact | yellow dot/stripe |
| Speech | microphone/speech marker text |
| Breaking | red pulse / `BREAKING` tag |
| Tentative | dashed time / `TENTATIVE` tag |
| Released | actual value visible and row status changed |

## Rerender Strategy

Dashboard should avoid full object churn.

Recommended method:

1. compute visible rows;
2. compute row fingerprints;
3. update changed rows;
4. hide unused row slots;
5. recreate only when layout mode changes.

## Acceptance Gate

UI architecture is accepted when:

- every filter can be toggled from dashboard;
- toggles affect dashboard and timeline together;
- no source fetch is required for simple filter changes;
- next event is highlighted;
- alert enable/disable is visible;
- source/GMT diagnostics are always visible.
