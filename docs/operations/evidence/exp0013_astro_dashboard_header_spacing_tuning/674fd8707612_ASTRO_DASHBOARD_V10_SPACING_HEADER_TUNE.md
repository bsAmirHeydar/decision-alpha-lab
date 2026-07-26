# EXP0013 Astro Dashboard V10 - Header and spacing tuning

This patch refines the cockpit layout without changing the stable in-place update model from V9.

## Changes

- smaller and cleaner header title so the top line fits better
- larger buttons with smaller text so captions stay inside the buttons
- header status lines moved upward and compacted so the header is cleaner
- metric cards now reserve more width for the left label column
- value, bucket, and bar columns have more breathing room
- first-column overlap issues are reduced by a wider dynamic label width rule
- compact oscillator uses the same wider spacing logic

## Result

The dashboard should stay stable in place, but look cleaner and fit the top region better.
