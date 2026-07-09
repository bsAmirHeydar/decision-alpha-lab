# Live Countdown Repaint

`GT_UpdateCountdowns()` now repaints the dashboard on timer. This keeps the next-event countdown alive without forcing a full timeline redraw every timer tick.

## Performance Rule

The dashboard is lightweight object mutation. The timeline remains heavier and only redraws on refresh, chart change, or explicit full redraw.
