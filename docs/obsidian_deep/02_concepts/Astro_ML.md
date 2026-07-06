
---
type: canonical_concept
concept: "Astro ML"
generated_at: 2026-07-06
source_count: 65
---

# Astro ML

## تعریف عملیاتی

بخش آزمایشی برای featureهای آسترولوژیک/ephemeris و سنجش اثر آن‌ها با روش علمی و auditپذیر.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]
- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

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
| [[docs/architecture|architecture.md]] | M0001, M0002, M0004, M0005 | Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural |
| [[docs/astro_ml_training_quickstart|astro_ml_training_quickstart.md]] | — | This is the shortest reliable path to start training the astro ML stack. The astro stack is ready for training when these are true: the astro feature builder is |
| [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab. It is separate from `E0001` and `E0002`. Build 1.06 adds a selectable D |
| [[docs/research/H0009_astro_feature_store_distribution_engineering|H0009_astro_feature_store_distribution_engineering.md]] | EXP0012, H0009 | **Astro Distribution Engineering: Candle-Aligned Planetary State as a Causal Feature Layer** Decision Alpha Lab does not treat astrology as a belief system. It  |
| [[docs/research/H0009_astro_feature_taxonomy|H0009_astro_feature_taxonomy.md]] | EXP0013 | This document defines what each astrological raw field can become as a testable feature. The project does not assume that astrology is causal. In Decision Alpha |
| [[docs/research/H0009_astro_path_cleanliness_metrics|H0009_astro_path_cleanliness_metrics.md]] | H0009 | This note defines the first Decision Alpha Lab interpretation layer for astrological data. The project does not use astrology as a raw directional signal. It us |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|ASTRO_CSV_COMMON_FILES_TESTER_FIX.md]] | EXP0013 | MetaTrader has different runtime file roots: If the CSV is placed under the live terminal `MQL5\Files`, the visual tester may still fail with `FILE_OPEN_FAILED` |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|ASTRO_CSV_DIAGNOSTIC_GUIDE.md]] | EXP0013 | This guide explains how the runtime diagnostic separates file-path errors from CSV-content and timestamp-alignment errors. MQL5 does not read files from the rep |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|ASTRO_CSV_FILES_ROOT_FALLBACK.md]] | EXP0013 | This patch makes the Astro CSV reader accept both common runtime layouts: and: The input may be either: or: The loader now tries three paths in order: the exact |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX.md]] | EXP0013 | This note explains the two separate failure classes used by the EXP0013 visual tester demos. If the panel shows: then the Expert Advisor did not even open the C |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_FIX|ASTRO_CSV_RUNTIME_PATH_FIX.md]] | EXP0013 | MQL5 does not read the `.xlsx` workbook at runtime. The workbook is only for human review. The Expert Advisor reads the CSV mirror. Human review file: MQL runti |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE|ASTRO_DASHBOARD_V10_SPACING_HEADER_TUNE.md]] | EXP0013 | This patch refines the cockpit layout without changing the stable in-place update model from V9. smaller and cleaner header title so the top line fits better la |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V11_BEST_VERSION|ASTRO_DASHBOARD_V11_BEST_VERSION.md]] | EXP0013 | This is the most polished dashboard build so far. It keeps the stable in-place update behavior from V9, and improves layout quality beyond V10. cleaner and slig |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V12_HEADER_MINIMIZE_CLEAN_OSC|ASTRO_DASHBOARD_V12_HEADER_MINIMIZE_CLEAN_OSC.md]] | EXP0013 | This patch improves three user-facing areas: clearer header text hierarchy explicit Symbol / TF / View line explicit Status and File line cleaner Broker / UTC l |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN|ASTRO_DASHBOARD_V13_UI_REVIEW_AND_REDESIGN.md]] | EXP0013 | **Header hierarchy was weak** the title, metadata, status, and file info competed for the same visual attention some items visually collided and reduced readabi |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] | EXP0013 | This version replaces the crowded single oscillator cloud with a cockpit layout. The EA is research-only: no orders no iCustom no indicator path dependency no x |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] | EXP0013 | This patch upgrades the dashboard into a more professional interactive cockpit. cleaner screen layout all major astro states visible open/close behavior through |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE|ASTRO_DASHBOARD_V4_LAYOUT_CLEANUP_GUIDE.md]] | EXP0013 | This patch focuses specifically on visual cleanup and readability. The previous interactive cockpit was functionally better, but visually it still had these pro |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V5_PRO_CLEAN_GUIDE|ASTRO_DASHBOARD_V5_PRO_CLEAN_GUIDE.md]] | EXP0013 | This patch is focused on making the dashboard noticeably more professional and easier to read. removed extra clutter from the header removed the old crowded tog |
| [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX|ASTRO_DASHBOARD_V6_CLEANUP_AND_SPACING_FIX.md]] | EXP0013 | This patch addresses two specific problems from the previous versions: When the expert refreshed, changed mode, or was reloaded, some previous panels stayed on  |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
