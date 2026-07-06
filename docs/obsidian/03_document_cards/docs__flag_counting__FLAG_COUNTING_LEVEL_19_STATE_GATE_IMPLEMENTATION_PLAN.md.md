---
title: "Flag Counting Level 19 — State Gate and Dashboard Implementation Plan"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "13983"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# Flag Counting Level 19 — State Gate and Dashboard Implementation Plan

**Source:** [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `13983` bytes

## خلاصه

Status: implementation plan Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md` Target: read-only multi-timeframe state map above locked Phoenix anatomy Level 19 must be implemented as a read-only layer after the existing Phoenix anatomy pipeline. It must not change: The implementation must behave like a projection: The State Gate is not a strategy engine. Add new include modules under: Recommended files: Responsibilities: Owns enums and structs: Pure label/projection rules: No mutation is allowed in this file. Owns runtime update orchestration: Owns chart objects: Writes: Prints compact audit lines: Add inputs to `FlagCountingPhoenixExperiment.mq5` in a new input group: The f

## Headings

- Flag Counting Level 19 — State Gate and Dashboard Implementation Plan
-   1. Implementation principle
-   2. Proposed module set
-     FP_StateGateTypes.mqh
-     FP_StateGateRules.mqh
-     FP_StateGateEngine.mqh
-     FP_StateGatePanel.mqh
-     FP_StateGateExport.mqh
-     FP_StateGateAudit.mqh
-   3. Expert input integration
-   4. Integration point in Phoenix
-   5. Multi-timeframe architecture

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|Flag Counting Level 19 — Multi-Timeframe State Gate and Dashboard Specification]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|Flag Counting Validation Case Registry]] — `flag_counting_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
