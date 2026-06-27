# 05 Visualization README

This package defines chart rendering.

Visualization exists to inspect logic. It must not replace logic.

## Files

- `VISUAL_CONTRACT.md`
- `LABEL_STACKING.md`
- `OBJECT_NAMING_AND_LAYERS.md`
- `DEBUG_VIEWS.md`

## Visual Goal

Show all logically emitted structures clearly enough to audit them, without making line width or arbitrary hiding change meaning.

## Critical Rule

The renderer may only draw objects emitted by the engine.

If something is missing or wrong, fix engine emissions first.
