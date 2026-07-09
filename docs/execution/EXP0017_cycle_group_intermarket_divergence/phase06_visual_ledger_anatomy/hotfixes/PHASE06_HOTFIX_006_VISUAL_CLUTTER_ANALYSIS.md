# EXP0017 Phase 06 Hotfix006 — Minimal Line-Only Visual Mode

## Problem Observed

The screenshot showed a dense horizontal band of white labels around price, obscuring candles and making the geometric divergence structure unreadable. This means the previous visual layer was optimized for audit text rather than chart geometry.

## Clutter Sources

1. `OBJ_TEXT` labels for every CG and state.
2. Historical backfill producing many repeated labels.
3. Full-audit defaults being forced on by `InpForceAllVisualObjectsOn`.
4. Invalidated double-hunt states being shown together with confirmed divergences.
5. Multiple CGs generating overlapping visual annotations at the same market zone.

## Fix

Hotfix006 changes the visual priority order:

```text
1. Main divergence legs
2. Optional markers
3. Optional structural timing lines
4. Optional audit guides
5. Optional text labels only in full audit mode
```

Text is now last, not first.

## Current Minimal Output

The expected chart should show colored divergence lines only. For confirmed buy divergences, lines use buy color. For confirmed sell divergences, lines use sell color. Invalidated lines are off unless explicitly enabled or full audit mode is selected.
