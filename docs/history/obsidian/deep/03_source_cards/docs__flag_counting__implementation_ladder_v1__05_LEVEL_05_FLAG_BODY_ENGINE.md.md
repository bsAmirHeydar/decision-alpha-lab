
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE.md"
source_ext: ".md"
source_size: 4271
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 05_LEVEL_05_FLAG_BODY_ENGINE.md

## Source

[[docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE|docs/flag_counting/implementation_ladder_v1/05_LEVEL_05_FLAG_BODY_ENGINE.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on th… Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. This layer detects the invariant two-leg flag body. It is the central object of Phoenix. F1/F2/F3 are all built from the same body shap

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 05 — Flag Body Engine
  - Purpose
  - Owned source modules
  - Body contract
  - Bullish body
  - Bearish body
  - Equal price rule
  - Leg2 extension rule
  - Output object
  - Forbidden behavior
  - Acceptance tests

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[docs/flag_counting/implementation_ladder_v1/07_LEVEL_07_F1_LIFECYCLE_ENGINE|07_LEVEL_07_F1_LIFECYCLE_ENGINE.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/11_LEVEL_11_CANONICALIZATION_AND_AUDIT|11_LEVEL_11_CANONICALIZATION_AND_AUDIT.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE|17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md]] — score `15`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `15`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
