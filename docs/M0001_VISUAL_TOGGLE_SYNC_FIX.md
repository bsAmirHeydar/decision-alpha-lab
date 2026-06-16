# M0001 Visual Toggle Sync Fix

## Problem

The chart can still show objects after manual visual toggles are set to `false` when:

1. `InpViewPreset` is not `0`; presets intentionally turn layers on.
2. Old objects from previous prefixes remain on the chart.
3. Strategy Tester keeps drawing previous objects until the EA deletes them.

## Fix

The Expert now has hard visual controls:

```text
InpRenderVisualObjects
InpForceFlatCustomMode
InpCleanAllM0001Objects
```

Recommended blank chart:

```text
InpRenderVisualObjects = false
InpCleanAllM0001Objects = true
```

Recommended manual/custom mode:

```text
InpRenderVisualObjects = true
InpForceFlatCustomMode = true
InpViewPreset = 0
```

Preset mode:

```text
InpRenderVisualObjects = true
InpForceFlatCustomMode = false
InpViewPreset = 1..12
```

## Important rule

Manual toggles are only fully manual when:

```text
InpViewPreset = 0
```

or:

```text
InpForceFlatCustomMode = true
```

If `InpViewPreset` is 10, 11, or 12, it will draw preset layers even when the individual toggles are false.
