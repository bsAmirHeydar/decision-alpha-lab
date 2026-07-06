
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE.md"
source_ext: ".md"
source_size: 7181
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 02_LEVEL_02_NODE_ENGINE.md

## Source

[[docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE|docs/flag_counting/implementation_ladder_v1/02_LEVEL_02_NODE_ENGINE.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on th… Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. This layer extracts canonical structural high/low nodes from the Level 01 closed-bar stream. Every later concept depends on node correc

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 02 — Node Engine
  - Purpose
  - Owned source modules
  - Canonical input contract
  - Canonical node definition
    - High node
    - Low node
  - Equality and plateau rule
  - Confirmed versus live-pending
  - Canonicalization after raw extraction
  - Public functions

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE|01_LEVEL_01_CANDLE_STREAM_AND_TIMEBASE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/03_LEVEL_03_NODE_IDENTITY_AND_SCALE|03_LEVEL_03_NODE_IDENTITY_AND_SCALE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE|04_LEVEL_04_HOOK_ND_CONTEXT_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|05_LEVEL_05_FLAG_BODY_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|07_LEVEL_07_F1_LIFECYCLE_ENGINE.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/08_LEVEL_08_F2_LIFECYCLE_ENGINE|08_LEVEL_08_F2_LIFECYCLE_ENGINE.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
