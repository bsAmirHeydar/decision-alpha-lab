---
type: architecture_note
id: HOOK-VAL-0005
title: Hook Zone Risk Contract
domain: hook_validity
status: canonical_draft
related:
  - Valid Hook
  - Zone as Risk Contract
  - Limit Entry
  - No Stop No Trade
---

# HOOK-VAL-0005 — Hook Zone Risk Contract

## 1. Core Thesis

A valid hook matters because it can create a valid hook zone.

The hook itself is not the trade. The zone derived from the valid hook is the tradable object.

The rule:

> Valid hook → valid hook-zone candidate → risk contract evaluation → possible limit entry.

## 2. Hook Zone Definition

A Hook Zone is a price range derived from a valid hook source where:

- the entry side is known,
- the stop/expiration side is known,
- the zone is not excessively wide,
- the reward side remains open,
- the surrounding context justifies reversal or reaction potential.

## 3. Entry and Stop Logic

The hook zone follows the general Alpha Lab zone principle:

- entry is planned near the first tradable edge of the zone,
- stop/expiration is placed beyond the opposite edge or behind the structural hook boundary,
- profit is not capped by a fixed pattern target,
- the trade is held only if the movement quality justifies growth.

## 4. Validity Before Risk

The system must not evaluate a hook zone until the hook itself passes validity.

Sequence:

```text
Hook-like candidate
→ hook validity test
→ valid hook family?
→ zone boundary evaluation
→ risk/reward evaluation
→ limit-entry plan
```

The system must not skip the validity test.

## 5. Strong Hook Zones

The strongest hook zones are expected to come from:

1. Hook After Hook with exact shared node lineage.
2. Hook After Opposing F3 where the hook converts a broad F3 reversal field into a measurable risk contract.

These hooks are not merely visual formations. They carry structural meaning.

## 6. Weak or Non-Tradable Hook Zones

A hook zone becomes weak or non-tradable when:

- the hook is invalid,
- the zone is too wide,
- the stop is not stable,
- the entry boundary is unclear,
- the hook was only visible through arbitrary fractal interpretation,
- the context does not provide open reward potential,
- the zone is only identifiable after the move.

## 7. Lower-Timeframe Refinement

Even valid hooks may sometimes create zones that are too wide for direct entry. In that case, the hook zone becomes a parent or watch zone.

The system must then wait for a lower-timeframe child zone.

Policy:

> Valid hook but broad zone → wait for child risk contract.

A lower-timeframe child zone should provide:

- tighter entry,
- clearer invalidation,
- smaller MAE risk,
- better potential/width ratio,
- more precise limit-entry placement.

## 8. Hook Zone Outcome Evaluation

Hook zones should be evaluated through convexity-oriented outcomes, not raw win rate.

Important metrics:

- MFE,
- MAE,
- MFE/MAE,
- time to expansion,
- zone width,
- potential/width,
- path smoothness,
- stop efficiency,
- tail participation.

The hook zone is successful if it creates favorable asymmetry, not merely if it wins often.

## 9. Final Principle

> A hook zone is valid only when the hook is valid and the zone can be treated as a measurable bounded-risk contract.
