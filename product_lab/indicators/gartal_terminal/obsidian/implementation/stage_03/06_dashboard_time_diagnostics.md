# 06 — Dashboard Time Diagnostics

## Visible diagnostics

When `InpShowTimeDebug=true`, the dashboard exposes:

- effective broker GMT
- detected broker GMT
- broker GMT mode
- source time mode
- sample time mode
- confidence score
- broker date window
- server / UTC snapshots

## Design doctrine

A commercial indicator must not hide time uncertainty. The user must be able to see whether the indicator is running on auto GMT, manual GMT, or hybrid fallback.

## UX goal

The time block should be visible enough for trust, but not dominant. In later UI stages this becomes a compact diagnostic chip.
