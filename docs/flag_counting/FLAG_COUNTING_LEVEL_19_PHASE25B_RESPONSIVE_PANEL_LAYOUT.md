# Flag Counting Level 19 — Phase 25B Responsive Panel Layout

This patch redesigns the State Gate panel layout so it adapts better to different chart resolutions and monitor sizes.

## What changed

- The panel now reads the chart pixel width and height at runtime.
- Width is chosen responsively instead of staying fixed.
- Font size and row height are reduced automatically on smaller charts.
- The panel position is clamped inside the visible chart area.
- The content switches between roomy, compact, and ultra-compact rendering modes.
- Rally and Hook preview rows are reduced automatically on smaller screens.
- Section buttons remain intact:
  - main minimize button
  - per-timeframe collapse button
  - Rally collapse button
  - Hook collapse button

## Goal

Keep the dashboard readable on:

- lower-resolution monitors
- smaller chart windows
- different DPI / monitor configurations
- larger monitors where more detail can still be shown

## Rendering modes

The panel now chooses among these display styles automatically:

- **Roomy**: larger charts, more preview rows
- **Compact**: moderate charts, one preview row per Rally/Hook section
- **Ultra-compact**: small charts, summary-first view and no preview rows

## Safety

This patch only changes the panel rendering layer.

It does **not** modify:

- ND / Hook counting logic
- F-count logic
- State Gate decision logic
- paper trading logic
- lifecycle logic
- execution logic
- licensing
