# EXP0017 Phase 06 Hotfix006 — Minimal Line-Only Visual Mode

## Purpose

This hotfix repairs the visual language after chart screenshots showed that text labels were dominating the chart while the actual divergence geometry was not readable. The new default is intentionally minimal: no chart comments, no chart panel, no text labels, no guide clutter, and no marker clutter. The chart should show only the divergence legs that connect the origin to the destination on each symbol-local chart.

## New Base Visual Doctrine

The visual layer must not explain the signal with text first. It must expose geometry first. The chart should answer one question visually: from which reference extreme to which current extreme did the divergence leg form?

## Default Behavior

- Visual mode: `CGV_VISUAL_MODE_MINIMAL_LINES_ONLY`
- Text labels: off
- Chart comments: off
- Print summary: off
- Markers: off
- Vertical lines: off
- Reference guides: off
- Clean stop guides: off
- Clean comparison guide clutter: off
- Confirmed divergences: on
- Invalidated double hunts: off by default because they are not divergence under the base doctrine
- Historical visual backfill: on
- Dual-symbol drawing: on

## What Remains on the Chart

For each confirmed divergence, the expert draws one symbol-local origin-to-destination leg on Symbol A and one symbol-local origin-to-destination leg on Symbol B.

For a sell divergence, the leg connects reference high to current high. For a buy divergence, the leg connects reference low to current low.

## Why Text Is Suppressed Defensively

Older `.set` files can preserve old input values. Therefore this hotfix adds a final text-suppression layer. If `InpSuppressAllTextObjects=true`, the code forces `draw_text_label=false` even if an old input set or an old force mode tries to turn labels back on. It can also delete existing Phase 06 text objects on initialization.

## Saved `.set` Protection

The visual mode is now the primary authority. If an older `.set` file still has `InpForceAllVisualObjectsOn=true`, it no longer overrides `CGV_VISUAL_MODE_MINIMAL_LINES_ONLY`. This prevents old full-audit settings from re-enabling labels, markers, verticals, and guides during the current line-only review stage.
