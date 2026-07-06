# ZONE-AF-0010 — F Source-of-Truth Map for Zone Usage

## Purpose

This document maps existing F-counting canon files to the Zone-AF interpretation layer. It exists to prevent drift.

## Rule

```text
When Zone-AF mentions F1, F2, F3, Waist, Origin, Leg1, Leg2, confirmation, invalidation, lock, or authorization, the definition comes from Flag Counting canon.
```

## Source Map

| Zone-AF Need | Canonical Source |
|---|---|
| F-body geometry | `engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md` |
| Shared `Origin -> Leg1 -> Waist -> Leg2` body | `F_LEVELS_DEFINITION.md` |
| F1 role and explanation | `engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED.md` |
| F1 lifecycle implementation | `implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE.md` |
| F2 authorization and origin backfill | `implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE.md` |
| F2 waist-break branch | `F_LEVELS_DEFINITION.md` and `F1_F2_F3_ALGORITHMS.md` |
| F2 invalidation at Origin | `F_LEVELS_DEFINITION.md` and Level 08 docs |
| F3 authorization | `implementation_ladder_v1/09_LEVEL_09_F3_EXTENSION_AND_LOCK_ENGINE.md` |
| F3 terminal behavior and lock | Level 09 docs |
| Current implementation reality | `mql5/Include/FlagCountingPhoenix/` |

## F1-to-Zone Usage

Canonical F1 supplies:

- first-flag context;
- waist as risk reference;
- post-flag 1/2 as directional continuation context;
- potential entry interest after the F1 flag and internal correction evidence.

Zone-AF adds:

- risk-contract interpretation;
- potential/width assessment;
- limit-entry suitability;
- child-zone requirement when zone width is poor.

Zone-AF does not add:

- new F1 confirmation rules;
- new F1 invalidation rules;
- new F1 start rules.

## F2-to-Zone Usage

Canonical F2 supplies:

- authorized second flag only after F1 confirmation;
- F2 origin from owned post-F1 correction context;
- size relation against F1;
- invalidation at F2 Origin;
- waist-break branch where `1 = F2 Waist` and `2 = node that passes F2 Waist`.

Zone-AF adds:

- reversal-potential interpretation from Point 2 onward in the waist-break branch;
- broad parent-zone classification when stop is not stable;
- lower-timeframe child-zone requirement for direct limit execution.

Zone-AF does not add:

- F2 invalidation at Waist;
- arbitrary F2 starts;
- direct execution permission where stop is missing.

## F3-to-Zone Usage

Canonical F3 supplies:

- terminal flag context;
- authorization by confirmed F2;
- origin backfill from post-F2 correction context;
- terminal body and OR qualification;
- lock evidence from first opposite confirmed F1.

Zone-AF adds:

- broad reversal environment interpretation;
- watch-zone classification when boundaries are unstable;
- requirement for lower-timeframe child zones;
- connection to opposing valid hook logic.

Zone-AF does not add:

- direct F3 zone entry without a stable risk contract;
- new F3 lock rules;
- F3 completion from visual assumption.

## Correct Patch Policy

Every future patch that touches F-derived zones must state:

```text
F source checked:
- FLAG_COUNTING_CURRENT_CANON.md
- F_LEVELS_DEFINITION.md
- F1_F2_F3_EXPLAINED.md
- F1_F2_F3_ALGORITHMS.md
- Level 07/08/09 docs
- Phoenix implementation, if code changes are involved
```

If a patch changes F definitions, it belongs in Flag Counting canon first, not Zone-AF.
