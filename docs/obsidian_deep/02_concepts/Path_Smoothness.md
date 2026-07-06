
---
type: canonical_concept
concept: "Path Smoothness"
generated_at: 2026-07-06
source_count: 49
---

# Path Smoothness

## تعریف عملیاتی

کیفیت مسیر حرکت؛ میزان تمیز بودن، کم‌پولبک بودن و قابلیت trend following یا convex follow-through.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]]

## سؤال‌های طراحی

- تعریف دقیق این مفهوم در داده چیست؟
- آیا در زمان live قابل دانستن است یا future leak دارد؟
- آیا روی چند regime تست شده است؟
- آیا ارتباطش با تحدب/هزینه شکست روشن است؟
- آیا پیاده‌سازی MQL/Python آن traceable است؟
- آیا در ژورنال دستی label می‌شود؟

## Source Documents

| سند | entityها | خلاصه |
|---|---|---|
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/articles/distribution_engineering_for_conditional_sequence_extraction|distribution_engineering_for_conditional_sequence_extraction.md]] | EXP0012, H0008 | Decision Alpha Lab is moving from **edge discovery** to **distribution engineering**: the objective is not merely to find a strategy with positive expectancy, b |
| [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summ |
| [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] | — | This answer should be treated as: DST-R02 should not hard-code one exit rule. Recommended flow: Trailing should be treated as a tested optional family, not the  |
| [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|CONCEPT_TAXONOMY.md]] | — | This file organizes the model into object layers. Only high and low are structurally consumed. Other bar fields may exist in platform data but are irrelevant to |
| [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|ANTI_PATTERNS_AND_FAILURES.md]] | — | This file lists mistakes that previously produced wrong charts. Wrong: Why wrong: no phase boundary; no ownership; can start in middle of move; creates orphan l |
| [[docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT|VISUAL_CONTRACT.md]] | — | Renderer receives render model objects: It does not receive raw bars to infer structures. A flag body uses two visual pieces: All flag lines are thin by default |
| [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] | — | This document converts the concept specification into implementation-level algorithms. Fields: `int index` `datetime time` `double price` `int kind` where `+1 = |
| [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE26_PAPER_PERFORMANCE_REPORT|FLAG_COUNTING_LEVEL_19_PHASE26_PAPER_PERFORMANCE_REPORT.md]] | — | Phase 26 adds a paper performance report above the Phase 25 Persistent Paper Trade Lifecycle Engine. This phase still does **not** send real orders. It summariz |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md]] | — | Phase 27 adds paper MFE / MAE path quality diagnostics above the Phase 26 Paper Performance Report. This phase still does **not** send real orders. It evaluates |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX|FLAG_COUNTING_LEVEL_19_PHASE27A_COMPILE_FIX.md]] | — | Phase 27A fixes a compile error introduced in Phase 27. Phase 27 used `FP_StateGateClampDouble` inside the paper path smoothness score function, but that helper |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX.md]] | — | Phase 28 adds a context performance matrix above the Phase 27 Paper MFE / MAE Path Quality layer. This phase still does **not** send real orders. It groups pape |
| [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |
| [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] | — | <!-- CURRENT CANON NOTICE This file remains the active semantic sequence contract for Phoenix, but it is subordinate to: docs/flag_counting/FLAG_COUNTING_CURREN |
| [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]] | — | <!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_ |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
