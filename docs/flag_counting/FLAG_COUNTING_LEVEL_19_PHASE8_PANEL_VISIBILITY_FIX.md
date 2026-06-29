# Flag Counting Level 19 — Phase 8 Panel Visibility Fix

## Purpose

Phase 8 fixes the dashboard visibility issue observed on chart screenshots where only the small minimize buttons were visible and the panel body was not readable.

The root cause is usually old saved EA inputs keeping a right-corner layout active while the new panel code expects a left-upper layout. In MetaTrader, saved input sets can persist even after defaults are changed in code.

## Fix

Phase 8 adds an explicit left-corner override:

```text
InpStateGatePanelForceLeftUpper = true
```

This input has priority over older right-corner settings. The corner priority is now:

```text
ForceLeftUpper
then ForceRightUpper
then PanelCorner
```

Default behavior:

```text
InpStateGatePanelCorner          = CORNER_LEFT_UPPER
InpStateGatePanelForceRightUpper = false
InpStateGatePanelForceLeftUpper  = true
InpStateGatePanelX               = 16
InpStateGatePanelY               = 24
```

## Visual improvements

The panel background was also made more visible:

- body background changed from pure black to dark slate
- panel border and title border are brighter
- object z-order is explicitly set for background, labels, and buttons

## Locked boundaries

This phase does not change:

- Node Engine
- Hook / ND Engine
- Flag Body
- Internal Count
- F1 / F2 / F3 lifecycle
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License

Only the Level 19 panel placement/visibility shell is touched.

## What to check after applying

After applying and compiling, check the EA inputs:

```text
InpStateGatePanelForceLeftUpper  = true
InpStateGatePanelForceRightUpper = false
InpStateGatePanelCorner          = CORNER_LEFT_UPPER
```

If a saved `.set` file overrides the inputs, load defaults or manually set the three values above.
