# Stage 05 Validation Checklist

## MetaEditor

- `GartalTerminal.mq5` compiles.
- No duplicate function definitions.
- `GartalNewsDashboardTheme.mqh` is included before `GartalNewsDashboard.mqh`.

## Visual

- Dashboard appears at configured corner and position.
- Width input changes panel width.
- Header and health badge render.
- Next-event countdown updates on timer.
- Next red card appears in PRO mode.
- Metrics match store counters.
- Filter preview reflects input defaults.
- Event table rows do not overlap.

## Regression

- Stage 04 timeline still renders.
- Stage 03 time debug still appears.
- Stage 02 sample events still feed the store.
