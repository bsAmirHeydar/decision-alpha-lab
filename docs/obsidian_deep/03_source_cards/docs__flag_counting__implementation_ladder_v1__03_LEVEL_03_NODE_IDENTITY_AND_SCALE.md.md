
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md"
source_ext: ".md"
source_size: 4451
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md

## Source

[[docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE|docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Lower layers become frozen foundations before higher layers depend on them. Level 03 makes identity explicit before Hook/ND, F1/F2/F3 lifecycle, ownership, and renderer work. Phoenix must never decide visibility from only `node_id`, `event_id`, or chart object names. This layer separates: Wiring consumers: `FP_Node`, `FP_HookBranch`, and `FP_FlagEvent` carry Level 03 fields: For `FP_Node`, `source_L` is represented by the existing `L` field. Structural node identity: Visual node identity: This allows audit to keep multiple L versions while the main chart can collapse visually identical structures deterministically. Structural event identity: Visual event identity: Phase identity: Chain identity: Audit identity: Visibility/canonicalization may use `canonical_rank_score`, but identity assignment is low

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 03 — Node Identity and Scale
  - Purpose
  - Owned source modules
  - Identity fields
  - Node identity
  - Event identity
  - Canonical winner policy
  - Audit contract
  - Forbidden behavior
  - Acceptance tests
    - Test 01 — Same visible body across L

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE|02_LEVEL_02_NODE_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|05_LEVEL_05_FLAG_BODY_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|07_LEVEL_07_F1_LIFECYCLE_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE|08_LEVEL_08_F2_LIFECYCLE_ENGINE.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
