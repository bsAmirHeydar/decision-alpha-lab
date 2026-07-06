---
type: architecture_note
id: HOOK-VAL-0003
title: Hook After Opposing F3 Architecture
domain: hook_validity
status: canonical_draft
related:
  - Opposing F3
  - Valid Hook
  - F3 Broad Reversal Environment
  - Hook Zone
---

# HOOK-VAL-0003 — Hook After Opposing F3 Architecture

## 1. Definition

A **Hook After Opposing F3** is a valid hook that appears after an F3 structure in the opposite direction.

Example:

- A bearish F3 prints.
- After that bearish F3, a bullish hook forms.
- The bullish hook becomes valid because it emerges after the opposing F3 environment.

The same logic applies in reverse:

- A bullish F3 prints.
- After that bullish F3, a bearish hook forms.
- The bearish hook becomes valid.

## 2. Why F3 Matters

F3 is broad, unstable, and difficult to trade directly as a zone. It does not usually provide a precise start boundary or a stable stop boundary. However, it creates an important environment:

> After F3, the market may be vulnerable to reversal, exhaustion, transition, or structural re-pricing.

F3 by itself is often too wide to trade. But a hook that forms after an opposing F3 can become the first precise structure inside that broad reversal environment.

## 3. The Role of the Opposing Direction

The hook must oppose the prior F3 direction.

If the prior structure is bearish F3, the valid hook is bullish. If the prior structure is bullish F3, the valid hook is bearish.

The reason is conceptual:

- F3 creates broad exhaustion or instability in one direction.
- The opposing hook creates a more precise risk contract in the other direction.
- The hook converts the broad F3 environment into a potentially tradable zone.

## 4. Validity Conditions

A Hook After Opposing F3 is valid only if:

1. The preceding F3 is clearly identified.
2. The hook forms after that F3, not before it.
3. The hook direction opposes the F3 direction.
4. The hook is not an arbitrary internal hook inside the same direction as the F3.
5. The hook produces a zone with a measurable entry side and stop/expiration side.
6. The broader context still allows open reward potential.

## 5. What This Solves

F3 creates a problem for direct zone trading:

- the reversal area can be very wide,
- the start of the zone is not stable,
- the stop is not obvious,
- the sequence can continue further than expected,
- locking or completing F3 does not necessarily end the F3 environment.

The valid opposing hook solves this by creating a lower-level structural anchor.

Instead of trading F3 directly, the system waits for:

> Opposing F3 environment → valid opposing hook → measurable hook zone → limit-entry risk contract.

## 6. Zone Implication

The valid hook after opposing F3 may generate a hook zone.

That hook zone is important because it is the first tradable contraction of a broad F3 reversal field. It is not the F3 itself that is traded. It is the hook derived from the opposing reaction after F3.

This distinction prevents the system from taking broad, vague F3 reversal trades without a stop.

## 7. Invalid Variants

The following are not valid Hook After Opposing F3 structures:

- A hook that appears before F3 is established.
- A hook in the same direction as the F3, unless independently valid by the Hook After Hook rule.
- A hook counted from arbitrary lower-timeframe noise inside the F3.
- A hook that has no measurable zone boundary.
- A hook that requires hindsight to identify.

## 8. Antifragile Interpretation

The system respects F3 as a broad potential environment, but it does not blindly trade it.

The antifragile policy is:

> Broad potential is not enough. The system must wait for a smaller structure that turns potential into bounded risk.

A hook after opposing F3 does exactly that.

## 9. Learning Implication

In the dataset, this structure should be separated from generic hooks and generic F3 events.

Suggested fields:

- `hook_validity_type = hook_after_opposing_f3`
- `f3_id`
- `f3_direction`
- `hook_id`
- `hook_direction`
- `opposition_confirmed`
- `zone_id`
- `zone_width`
- `invalidation_price`
- `f3_to_hook_delay_bars`
- `outcome_mfe`
- `outcome_mae`
- `mfe_mae_ratio`
- `tail_expansion_flag`

This allows the system to test whether opposing-F3 hooks are genuinely stronger than generic hook-like events.

## 10. Final Rule

> F3 is too broad to trust directly. The opposing hook after F3 is the structure that may convert F3 potential into a tradable zone.
