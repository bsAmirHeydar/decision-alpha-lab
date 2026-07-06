# ZONE-AF-0009 — Canonical F-Logic Integration Doctrine

## Status

Canonical integration addendum for the Zone-Centric Antifragile Architecture.

## Purpose

This document locks a strict boundary:

```text
F-counting defines the structure.
Zone-AF interprets the structure as potential, cost, and risk contract.
```

The Zone-AF layer must not redefine F1, F2, or F3. The already-established Flag Counting canon remains the source of truth for all F-body construction, lifecycle, authorization, confirmation, invalidation, extension, and lock behavior.

## Why This Lock Exists

The Zone-AF system is built to extract risk-contract opportunities from mechanical context. F1/F2/F3 are part of that mechanical context. If the Zone layer starts redefining F objects, the system splits into two inconsistent grammars:

1. the mechanical Flag Counting engine;
2. a parallel discretionary zone interpretation.

That would break determinism, auditability, training labels, and future agent behavior.

Therefore:

```text
No F-related zone document may invent a new F rule.
Every F-related zone document must reference canonical F events.
```

## Canonical F Sources

The active F source of truth is the Flag Counting canon and Phoenix path:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md
docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md
docs/flag_counting/engineering_pack_v5/02_definitions/F_LEVELS_DEFINITION.md
docs/flag_counting/engineering_pack_v5/03_explanations/F1_F2_F3_EXPLAINED.md
docs/flag_counting/engineering_pack_v5/04_algorithms/F1_F2_F3_ALGORITHMS.md
docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE.md
docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE.md
docs/flag_counting/implementation_ladder_v1/09_LEVEL_09_F3_EXTENSION_AND_LOCK_ENGINE.md
mql5/Include/FlagCountingPhoenix/
```

## Core Doctrine

F objects are not zones by default. They become relevant to zones only through the risk-contract question:

```text
Does this canonical F state create a price area where:
1. entry can be placed near a defined edge,
2. invalidation can be placed near a stable opposite edge,
3. cost is bounded,
4. reward can remain open,
5. potential justifies the risk?
```

If the answer is no, the F state is context only.

## F1 Usage in Zone-AF

Zone-AF uses canonical F1 as a first structural flag after a valid phase boundary. F1 is not redefined by Zone-AF.

The Zone-AF interpretation is:

- after F1 body and internal post-flag evidence, point 2 / post-flag correction areas may create directional entry interest;
- F1 waist is a crucial risk reference;
- moving closer to the F1 waist compresses risk and can narrow the zone;
- F1 gives a stronger zone only when the zone start and stop boundary are stable enough for a limit risk contract.

Zone-AF must not change:

- F1 start requirements;
- F1 body geometry;
- F1 internal count requirement;
- F1 confirmation rule;
- F1 waist invalidation before confirmation.

## F2 Usage in Zone-AF

Zone-AF uses canonical F2 as the second flag of an existing F-chain. F2 is authorized only after canonical F1 confirmation. Zone-AF must not create F2 from arbitrary local geometry.

Important canonical rule:

```text
F2 invalidates at its Origin, not its Waist.
```

F2 may break its own Waist without invalidating, provided its Origin remains safe.

Canonical waist-break branch:

```text
1 = F2 Waist
2 = node that passes F2 Waist
```

Zone-AF interpretation:

- if F2 hits its own waist, that waist-hit can function as Point 1 in the canonical branch;
- the following hit / extension that passes the F2 waist can function as Point 2;
- from Point 2 onward or beyond, reversal potential becomes active as a parent potential field;
- this does not automatically create a direct execution zone;
- if stop is not stable, lower-timeframe child-zone refinement is required.

Zone-AF must not convert an F2 waist hit into F2 invalidation unless canonical Origin invalidation also happens.

## F3 Usage in Zone-AF

Zone-AF uses canonical F3 as terminal sequence context. F3 is authorized only after canonical F2 confirmation and has its own terminal body, OR qualification, completion, and lock behavior.

Zone-AF interpretation:

- F3 often creates a broad reversal environment;
- F3 itself may be too open for direct limit execution;
- because start edge and stop edge may be unstable, F3 usually requires lower-timeframe child-zone refinement;
- an opposing hook after F3 may become a valid zone source under the Hook Validity doctrine.

Zone-AF must not treat every F3 area as a direct tradable zone.

## Translation Layer

The correct transformation is:

```text
Canonical F event
→ movement constraint
→ potential field
→ zone candidate
→ risk-contract validation
→ child-zone refinement if needed
→ limit execution only if start and stop edges are clear
```

The incorrect transformation is:

```text
F-like visual shape
→ assumed zone
→ direct trade
```

## Hard Rule

```text
No canonical F event = no F-derived zone label.
```

A visual resemblance to F1/F2/F3 is not sufficient for Zone-AF use. The event must come from the canonical F-counting stream or from a documented, audit-equivalent extraction path.

## Practical Debug Rule

If a future chart or patch appears to disagree with the zone interpretation, inspect in this order:

1. Was the F object emitted by the canonical Phoenix engine?
2. Which lifecycle state did it have?
3. Was it confirmed, candidate, size-rejected, OR-rejected, completed, locked, invalidated, or diagnostic-only?
4. Did the Zone layer interpret that state correctly?
5. Did the Zone layer require lower-timeframe child refinement where stop was unstable?

Do not solve F-zone bugs by inventing new F rules inside Zone-AF.
