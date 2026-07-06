---
title: "Concept Glossary"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "4844"
concepts:
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Concept Glossary

**Source:** [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY|docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_GLOSSARY.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `4844` bytes

## خلاصه

The only raw price observations used by the structural logic. Open, close, body, candle direction, and candle color are not structural inputs. A high or low price point that satisfies the project node definition for a given L. A node is extracted from candle highs/lows and remains historically valid after it is created. The project node clearance parameter: A high node requires at least L candles on the left and L candles on the right that do not reach that high price. A low node requires at least L candles on the left and L candles on the right that do not reach that low price. Equal highs/lows are handled as plateau nodes by the existing project node module. A stable reference to a specifi

## Headings

- Concept Glossary
-   Candle High / Candle Low
-   Node
-   L
-   Node Identity
-   Equality
-   Pass / Break / Hit
-   Flag Body
-   Origin
-   Leg1
-   Waist
-   Leg2

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/glossary|Glossary]] — `core_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|Concept Taxonomy]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/INVARIANTS_AND_ASSUMPTIONS|Invariants and Assumptions]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/README|01 Concepts README]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/answer_normalized_en|BASE-03 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
