# Hotfix008 Validation Plan

## Test 1 — consumed low must not redraw

1. Find a low reference used by the old build.
2. Verify that a later completed cycle made an equal/lower low before the current signal.
3. Attach the new EA.
4. The old stale low should no longer produce a divergence line.

## Test 2 — active lower frontier can still draw

1. Find the lowest unbroken previous low in the same trading day.
2. If current price sweeps it in one symbol and not the other, it may produce BUY divergence.
3. Older internal lows that are not frontier should remain suppressed.

## Test 3 — consumed high must not redraw

1. Find a high reference used by the old build.
2. Verify that a later completed cycle made an equal/higher high before current.
3. The stale high should not produce a SELL divergence line.

## Test 4 — active higher frontier can still draw

1. Find the highest unbroken previous high in the same trading day.
2. If current price sweeps it in one symbol and not the other, it may produce SELL divergence.

## Test 5 — historical backfill

Historical visual backfill must respect the same frontier logic. The chart should not be flooded by old internal references.

## Object-list expectation

In minimal mode, only these should normally appear:

```text
EXP0017_P06_*_origin_to_destination_*
EXP0017_P06_*_origin_to_destination_*_shadow
```

No text labels should appear unless Full Audit mode is intentionally selected.
