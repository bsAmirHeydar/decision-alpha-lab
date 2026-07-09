# 03 — Filter-Aware Alerts

`InpAlertRespectRuntimeFilters=true` means the alert engine uses `GT_EventPassesFilters` before considering the event.

## Practical result

- Disable `USD` chip → USD alerts stop.
- Disable `RED` → high-impact alerts stop.
- Disable `SPEECH` → speech alerts stop.
- Click `ALERTS OFF` → the whole alert engine pauses.

This makes the dashboard a live control surface, not only a visual panel.
