# Canonical F-Logic Integration Patch

## Purpose

This documentation patch corrects the Zone-AF documentation layer by explicitly binding all F-related zone interpretations to the existing Flag Counting canon.

The Zone engine may use F1/F2/F3 structures to locate reversal potential, movement constraints, parent zones, child-zone requirements, and risk-contract opportunities. However, it must not create a parallel definition of F1, F2, or F3.

## Core Rule

```text
The Flag Counting canon defines F objects.
The Zone-AF layer interprets canonical F objects as potential zones.
```

## Source of Truth

The F source-of-truth hierarchy remains:

1. `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`
2. `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md`
3. `docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md`
4. `docs/flag_counting/engineering_pack_v5/`
5. `docs/flag_counting/implementation_ladder_v1/`
6. Current Phoenix implementation under `mql5/Include/FlagCountingPhoenix/`

## What This Patch Adds

- canonical F logic integration doctrine;
- source-of-truth map for F-to-zone usage;
- Obsidian MOC and concept pages;
- policy note preventing duplicate F definitions;
- training note requiring canonical F events as labels/features.

## What This Patch Does Not Change

- No MQL5 code changes.
- No Python changes.
- No execution changes.
- No registry changes.
- No redefinition of F1/F2/F3.
