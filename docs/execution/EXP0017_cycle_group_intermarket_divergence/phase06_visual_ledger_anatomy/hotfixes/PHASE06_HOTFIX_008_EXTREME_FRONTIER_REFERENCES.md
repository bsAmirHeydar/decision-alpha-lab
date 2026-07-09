# Phase 06 Hotfix008 — Extreme Frontier References

## Problem

Protected-reference retirement was not enough.

It only knew how to retire a reference after the system had already created a protected/clean-side lifecycle record. But the real structural problem is more primitive:

> If a high or low has already been swept by a later completed candle/cycle, that high or low must not be used again as a divergence reference.

A stale level can be visually seductive because price may still cross it again later, but it is no longer a fresh hunt reference. It has already been consumed.

## New doctrine

The system must not treat every previous cycle high/low as equally usable.

For each CG and current observation, previous references are filtered into a moving frontier:

### High-side frontier

A previous high is valid only if it is higher than every later completed previous-cycle high between that reference and the current observation.

If a later cycle already made an equal or higher high, the older high is internal and stale.

### Low-side frontier

A previous low is valid only if it is lower than every later completed previous-cycle low between that reference and the current observation.

If a later cycle already made an equal or lower low, the older low is internal and stale.

## Backward scan

References arrive oldest to newest. Hotfix008 walks them in the opposite direction:

```text
newest previous cycle -> older previous cycles
```

During this walk it stores:

```text
later_symbol_a_max_high
later_symbol_b_max_high
later_symbol_a_min_low
later_symbol_b_min_low
```

Then each candidate is classified:

```text
candidate_high is valid if candidate_high > later_max_high
candidate_low  is valid if candidate_low  < later_min_low
```

Equality consumes the level:

```text
candidate_high <= later_max_high => stale high
candidate_low  >= later_min_low  => stale low
```

## Why this fixes the issue

When a low has already been hit, any older/equal/higher internal low behind it must stop participating in divergence.

When a high has already been hit, any older/equal/lower internal high behind it must stop participating in divergence.

The robot now compares current behavior only against the active extreme frontier, not against all old historical levels.

## What remains unchanged

This patch does not add:

- orders
- risk
- targets
- statistics
- AI
- CG ranking
- strategy optimization

It only changes reference eligibility before confirmation and drawing.
