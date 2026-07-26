# Flag Counting Engineering Pack V5

## Purpose

This documentation package defines the Flag Counting model as an engineering system. It is written for implementation, audit, debugging, and future extension.

The package is not a visual design note and it is not an informal trading explanation. It defines the objects, identities, invariants, state transitions, algorithms, audit requirements, and visualization contract required to implement the model without ambiguity.

## System Philosophy

Flag Counting is a high/low-node sequence engine. It models market movement as structured two-leg flags chained in a strict F1 -> F2 -> F3 lifecycle, with ND/Hook phases describing multi-node correction or non-directional cycle behavior.

The core belief behind the model is:

```text
No meaningful movement should be structurally idle.
```

A move should belong to one of these structural roles:

- ND/Hook phase;
- F1 candidate or confirmed structure;
- F2 candidate or confirmed structure;
- F3 candidate, completed, extending, or locked structure;
- child candidate within an existing parent sequence;
- opposite-sequence phase boundary.

However, this does not mean that the engine may create arbitrary structures to cover every local window. Ownership and phase boundaries are mandatory.

## Package Structure

### 01 Concepts

High-level map of the model. This package names the main objects and explains how they relate.

Files:

- `01_concepts/README.md`
- `01_concepts/CONCEPT_GLOSSARY.md`
- `01_concepts/CONCEPT_TAXONOMY.md`
- `01_concepts/INVARIANTS_AND_ASSUMPTIONS.md`

### 02 Definitions

Canonical definitions. These files specify exact meanings of node, L, flag body, F levels, ND/Hook, identity, lifecycle, and boundary behavior.

Files:

- `02_definitions/README.md`
- `02_definitions/NODE_AND_L_DEFINITION.md`
- `02_definitions/FLAG_BODY_DEFINITION.md`
- `02_definitions/F_LEVELS_DEFINITION.md`
- `02_definitions/ND_HOOK_DEFINITION.md`
- `02_definitions/SEQUENCE_IDENTITY_DEFINITION.md`
- `02_definitions/STATUS_AND_LIFECYCLE_DEFINITION.md`

### 03 Explanations

Narrative explanations and edge-case reasoning. These files explain why the rules exist and how to reason through confusing cases.

Files:

- `03_explanations/README.md`
- `03_explanations/FLAG_COUNTING_EXPLAINED.md`
- `03_explanations/F1_F2_F3_EXPLAINED.md`
- `03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md`
- `03_explanations/BACKFILL_AND_CONTEXT_EXPLAINED.md`
- `03_explanations/ANTI_PATTERNS_AND_FAILURES.md`

### 04 Algorithms

Implementation plan. These files break the system into modules and define deterministic algorithms and pseudocode.

Files:

- `04_algorithms/README.md`
- `04_algorithms/MODULE_ARCHITECTURE.md`
- `04_algorithms/NODE_ENGINE_ALGORITHM.md`
- `04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM.md`
- `04_algorithms/FLAG_BODY_ENGINE_ALGORITHM.md`
- `04_algorithms/SEQUENCE_ENGINE_ALGORITHM.md`
- `04_algorithms/F1_F2_F3_ALGORITHMS.md`
- `04_algorithms/DEDUP_AUDIT_ALGORITHM.md`
- `04_algorithms/PSEUDOCODE_REFERENCE.md`

### 05 Visualization

Rendering contract. These files define how emitted logical objects should appear on the chart without letting the renderer invent logic.

Files:

- `05_visualization/README.md`
- `05_visualization/VISUAL_CONTRACT.md`
- `05_visualization/LABEL_STACKING.md`
- `05_visualization/OBJECT_NAMING_AND_LAYERS.md`
- `05_visualization/DEBUG_VIEWS.md`

## Non-Negotiable Engineering Boundaries

1. Structural logic uses candle highs and lows only.
2. Open, close, candle body, and candle color are irrelevant to structural decisions.
3. Node extraction must use the existing project node logic.
4. Equality is not a break. A level must be passed.
5. A flag is a two-leg object: Origin -> Leg1 -> Waist -> Leg2.
6. F1/F2/F3 differ by post-body behavior and sequence role, not by body shape.
7. In one chain, after F1 comes F2, and after F2 comes F3.
8. F2 is authorized only after F1 confirmation, but its origin is backfilled from the post-F1 correction context.
9. F3 is authorized only after F2 confirmation, but its origin is backfilled from the post-F2 correction context.
10. A child candidate that dies does not kill the parent context.
11. Rejected structures do not remain on the main chart by default.
12. Locked F3 must remain historically persistent.
13. ND/Hook can overlap with F structures if both are logically emitted.
14. Renderer may only draw emitted logical objects.

## Version Intent

V5 is designed as a rewrite/audit foundation for Phoenix. It must be read through `docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON.md`, which is the conflict resolver. Do not use V5 to revive `FlagCountingVNext`; Phoenix is the active implementation path.

The recommended workflow is:

1. Read the concepts.
2. Read canonical definitions.
3. Read explanations for edge cases.
4. Implement modules in the architecture order.
5. Add audit logs before adding complex chart rendering.
6. Add visualization only after emitted objects are logically correct.
