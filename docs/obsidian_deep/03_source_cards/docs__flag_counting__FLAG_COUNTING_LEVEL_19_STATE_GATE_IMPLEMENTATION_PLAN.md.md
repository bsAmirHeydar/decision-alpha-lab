
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md"
source_ext: ".md"
source_size: 13983
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]]

## Summary

Status: implementation plan Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md` Target: read-only multi-timeframe state map above locked Phoenix anatomy Level 19 must be implemented as a read-only layer after the existing Phoenix anatomy pipeline. It must not change: The implementation must behave like a projection: The State Gate is not a strategy engine. Add new include modules under: Recommended files: Responsibilities: Owns enums and structs: Pure label/projection rules: No mutation is allowed in this file. Owns runtime update orchestration: Owns chart objects: Writes: Prints compact audit lines: Add inputs to `FlagCountingPhoenixExperiment.mq5` in a new input group: The final naming may be adjusted to match existing Phoenix conventions, but the semantics must remain. Level 19 should run after the existing canonical state is available. Recommended order: If Level 19 ne

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — State Gate and Dashboard Implementation Plan
  - 1. Implementation principle
  - 2. Proposed module set
    - FP_StateGateTypes.mqh
    - FP_StateGateRules.mqh
    - FP_StateGateEngine.mqh
    - FP_StateGatePanel.mqh
    - FP_StateGateExport.mqh
    - FP_StateGateAudit.mqh
  - 3. Expert input integration
  - 4. Integration point in Phoenix
  - 5. Multi-timeframe architecture

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `33`
- [[docs/flag_counting/README|README.md]] — score `33`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `31`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `28`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `28`
- [[docs/nds_hook_architecture/README|README.md]] — score `28`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `27`
- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|VALIDATION_CASE_REGISTRY.md]] — score `27`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
