
---
type: canonical_concept
concept: "Validation / Audit"
generated_at: 2026-07-06
source_count: 527
---

# Validation / Audit

## تعریف عملیاتی

لایه بی‌رحم پروژه برای رد کردن ایده‌ها، کنترل overfit، walk-forward، robustness و baseline.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]
- [[docs/obsidian_deep/02_concepts/Obsidian_Knowledge_OS|Obsidian Knowledge OS]]
- [[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]]

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
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] | — | این سند، تجربه‌های خام امیر درباره بازار، اکستریم‌ها، اف‌شماری، هوک/رالی، سناریوهای دوطرفه، فرکتال و اجرای لیمیت را تبدیل می‌کند به یک چارچوب قابل‌کدنویسی، قابل |
| [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] | — | این فایل قالب خام ثبت تجربه‌هاست. هر تجربه باید به یکی از این فرم‌ها تبدیل شود: |
| [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] | — | این سند تعریف رسمی تجربه‌ی امیر درباره ورود در اکستریم‌هاست. موضوع اصلی: این سند کد اجرایی نیست. این سند پایه‌ی مرحله‌های بعدی است: در تصویر نمونه، ناحیه قرمز ح |
| [[docs/architecture|architecture.md]] | M0001, M0002, M0004, M0005 | Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural |
| [[docs/articles/distribution_engineering_for_conditional_sequence_extraction|distribution_engineering_for_conditional_sequence_extraction.md]] | EXP0012, H0008 | Decision Alpha Lab is moving from **edge discovery** to **distribution engineering**: the objective is not merely to find a strategy with positive expectancy, b |
| [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summ |
| [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] | H0004, M0001, M0002 | A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster |
| [[docs/astro_ml_training_quickstart|astro_ml_training_quickstart.md]] | — | This is the shortest reliable path to start training the astro ML stack. The astro stack is ready for training when these are true: the astro feature builder is |
| [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] | M0001 | This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the eng |
| [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] | D0005, H0005, M0001, M0002 | D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging. The goal is to detect and prevent look-ahead leakage in H5 regime and node l |
| [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] | D0006, E0001, E0005, H0005, M0001, M0002 | D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they ar |
| [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] | D0007, H0004, H0005, M0004 | D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proo |
| [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008_H4_CAUSAL_BATCH_REPORT.md]] | D0008, H0004 | This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts sample |
| [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] | D0009, M0001 | D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002Branch |
| [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] | D0010, H0004, M0001, M0002, M0004 | D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL |
| [[docs/debug/E0006/README|README.md]] | E0006, M0001 | E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market |
| [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] | E0006, M0001 | E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 liv |
| [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] | H0004, M0001, M0002 | This release restores the full stress/test surface for the official H0004 atomic no-sample report while preserving the strict contract: no M0002 branch samples  |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
