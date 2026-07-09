# Vertical Lines

## Purpose

Vertical lines show the exact broker-time release location of each visible event.

## Visual Rules

| Event type | Style | Width | Color source |
|---|---:|---:|---|
| Breaking | Solid | 2 | Red |
| High impact | Solid | 2 | Impact color |
| Medium impact | Dash | 1 | Impact color |
| Low / holiday | Dot | 1 | Impact color |
| Released / expired | Dot | 1 | Dim gray |

## Tooltip

Each line carries a tooltip-style text payload with currency, impact, event kind, broker time, UTC time, and values.
