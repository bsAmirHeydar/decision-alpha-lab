# Stage 06 Validation Checklist

## Manual MetaTrader Checks

- Attach indicator with sample data enabled.
- Confirm dashboard renders expanded filter rows.
- Click `RED` and confirm red events disappear/reappear.
- Click `ORANGE` and confirm medium events disappear/reappear.
- Click `USD` and confirm USD events disappear/reappear.
- Click `RED ONLY` and confirm only high-impact events remain.
- Click `ALL IMP` and confirm all impact severities return.
- Click `ALL CCY` and confirm all currency chips are active.
- Click `RESET` and confirm boot input defaults are restored.
- Confirm timeline vertical lines sync with dashboard rows.
- Confirm no stale GT objects remain after repeated toggling.

## Compile Checks

- `GartalTerminal.mq5` compiles.
- `GartalNewsFilters.mqh` is included before dashboard.
- No duplicate function names.
