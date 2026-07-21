---
title: "Invariants and Assumptions"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "3628"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
---


# Invariants and Assumptions

**Source:** [[docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS|docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `3628` bytes

## خلاصه

This file lists rules that must remain true in all implementations. 1. Only candle highs and lows feed structural logic. 2. Node extraction is delegated to the existing project node module. 3. Open, close, body, candle color, and candle direction do not participate in F or ND decisions. 4. A node does not expire. 5. Equality is not a break. 6. A boundary must be passed with strict inequality. 1. A flag is always two legs: 2. A body without Leg2 is not a complete flag body. 3. Leg1 is the true extreme before correction, not the first small node. 4. Waist is the true adverse correction extreme before Leg2. 5. Waist must update while correction deepens/higher-corrects. 6. In bullish body, corre

## Headings

- Invariants and Assumptions
-   Structural Input Invariants
-   Flag Geometry Invariants
-   Sequence Invariants
-   F1 Invariants
-   F2 Invariants
-   F3 Invariants
-   Hook / ND Invariants
-   Rendering Invariants

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY|Concept Glossary]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|Concept Taxonomy]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
