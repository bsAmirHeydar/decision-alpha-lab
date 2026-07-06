
---
type: canonical_concept
concept: "Licensing"
generated_at: 2026-07-06
source_count: 88
---

# Licensing

## تعریف عملیاتی

سیستم کنترل دسترسی/فعال‌سازی پروژه‌ها و محافظت از استفاده در محیط‌های متفاوت.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]

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
| [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] | — | این سند مشخص می‌کند برای استفاده از تجربه‌ی اکستریم L2، چه لایه‌های الگوریتمی و هوش مصنوعی لازم است. اصل مهم: AI در این سیستم predictor خام نیست. AI این کارها ر |
| [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] | — | این سند، تجربه‌های خام امیر درباره بازار، اکستریم‌ها، اف‌شماری، هوک/رالی، سناریوهای دوطرفه، فرکتال و اجرای لیمیت را تبدیل می‌کند به یک چارچوب قابل‌کدنویسی، قابل |
| [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] | — | این سند تعریف رسمی تجربه‌ی امیر درباره ورود در اکستریم‌هاست. موضوع اصلی: این سند کد اجرایی نیست. این سند پایه‌ی مرحله‌های بعدی است: در تصویر نمونه، ناحیه قرمز ح |
| [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] | D0006, E0001, E0005, H0005, M0001, M0002 | D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they ar |
| [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] | D0009, M0001 | D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002Branch |
| [[docs/debug/MARKET_LANGUAGE/README|README.md]] | M0007 | > Version: draft 0.2 > Scope: discretionary-to-algorithmic vocabulary for Decision Alpha Lab > Purpose: convert the manual multi-timeframe market-reading langua |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX|LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md]] | — | این اصلاح برای پروژه‌ی STC / SMT Cycles است و عمداً inputهای لایسنس را مخفی/غیرمستقیم نگه می‌دارد. هیچ input واضحی با اسم license اضافه نمی‌شود. لایسنس همچنان ا |
| [[docs/execution/EXP0016_intermarket_divergence_execution/README|README.md]] | EXEC001, EXP0016 | This documentation index points to the execution documentation inside the lab folder. Main strategy: `lab/09_execution/EXP0016_intermarket_divergence_execution/ |
| [[docs/EXP0015_cme_live_provider_patch|EXP0015_cme_live_provider_patch.md]] | EXP0015 | This patch adds a CME-compatible provider layer for EXP0015. The historical poller is intended for closed-bar monitoring and operational simplicity. It does not |
| [[docs/experience_capture/answers/SCN-R03/notes_en|notes_en.md]] | — | This answer should be treated as: The scenario layer should not produce one forced direction. It should produce a set: The execution layer should then activate  |
| [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] | M0007 | Status: **active source of truth for Phoenix implementation**. Scope: docs, code patches, audit, renderer, validation, and future execution modules related to F |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] | — | This is a clean rebuild of Level 19 after rolling the project back to the pre-Level-19 state. The new Level 19 is deliberately small, read-only, and isolated. L |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] | — | Phase 10 makes the State Gate panel auditable line-by-line. The problem solved by this phase is simple: > Whatever the panel is supposed to show must also exist |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] | — | Phase 11 is the first formal bridge from the State Gate anatomy map toward future entry design. It still does **not** create trade signals. The purpose is to st |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] | — | Phase 12 adds the first real map from State Gate context toward X-axis candidate extremes. This is still **not an entry system**. Phase 12 does not produce: It  |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] | — | Phase 13 adds a decision-neutral Multi-Timeframe Alignment Map above the Extreme Candidate Map. The State Gate now compares lower-slot context against higher-sl |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX|FLAG_COUNTING_LEVEL_19_PHASE13A_COMPILE_FIX.md]] | — | Phase 13A fixes a compile error introduced during Phase 13. `mtf_alignment_row_count` was accidentally declared twice inside `FP_StateGateTimeframeState`. Remov |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] | — | Phase 14 prepares entry geometry fields from the existing State Gate context. This phase is still **not** an entry system and still does **not** send orders. It |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER.md]] | — | Phase 15 adds the first decision-neutral Entry Idea Layer above Entry Geometry Readiness. This phase still does **not** create executable trade signals. It does |
| [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN.md]] | — | Phase 16 adds the first Entry Decision Layer above the Entry Idea Layer. This phase is still **non-executable**. It does not send orders and it does not allow o |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
