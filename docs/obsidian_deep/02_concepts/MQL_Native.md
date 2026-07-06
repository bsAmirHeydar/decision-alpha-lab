
---
type: canonical_concept
concept: "MQL Native"
generated_at: 2026-07-06
source_count: 298
---

# MQL Native

## تعریف عملیاتی

پیاده‌سازی native در MQL5 برای کاهش وابستگی به bridgeهای شکننده و نمایش/اجرا روی MetaTrader.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]]
- [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]
- [[docs/obsidian_deep/02_concepts/Licensing|Licensing]]

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
| [[docs/00_project_index|00_project_index.md]] | M0007 | M0007 — Adaptive F1 Flag Counting Project-name repetition inside MQL folders is avoided. Correct MQL module layout: |
| [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] | — | این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است. این سند کد اجرایی نیست. این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، |
| [[docs/architecture|architecture.md]] | M0001, M0002, M0004, M0005 | Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural |
| [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] | D0005, H0005, M0001, M0002 | D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging. The goal is to detect and prevent look-ahead leakage in H5 regime and node l |
| [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] | D0006, E0001, E0005, H0005, M0001, M0002 | D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they ar |
| [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] | E0006, M0001 | This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA an |
| [[docs/debug/E0006/README|README.md]] | E0006, M0001 | E0006 is the execution-facing layer of Decision Alpha Lab. It does **not** try to discover an alpha by itself and it does **not** redefine the structural market |
| [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] | E0006, M0001 | E0006 is a lightweight execution module that uses existing M0001 / execution modules instead of rebuilding structure logic. Source of truth for zones: M0001 liv |
| [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] | M0001, M0002, M0004 | M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path. The first atomic no-sample  |
| [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] | H0004, H0006, M0006 | H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionalit |
| [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] | M0001, M0002, M0004, M0005 | This release moves the no-sample / live-style contract into the main M0004 and M0005 experts. The main reports now default to atomic raw M0001 event replay: no  |
| [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`. It does **not** add a mode to E0001 and does not modify the lim |
| [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] | E0001, E0002, E0003, E0004, H0005, M0001 | `E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab. It is separate from `E0001` and `E0002`. Build 1.06 adds a selectable D |
| [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] | E0001, E0002, E0003, E0004, M0001, M0002 | `E0004_ContinuationHeikinAshiFlip.mq5` is the fourth execution adapter for Decision Alpha Lab. It is intentionally separate from E0001, E0002, and E0003. E0004  |
| [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] | E0001, E0002, E0003, E0004, E0005, H0005 | E0005 is the fifth H0005 execution module. It is a separate Expert Advisor. It does not modify E0001, E0002, E0003, or E0004. E0005 trades only the continuation |
| [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|LEGACY_COMPILE_FIX.md]] | EXP0015 | This patch fixes compile errors triggered by the deprecated expert: `mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5` `mql5/Include/Interma |
| [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|IMPLEMENTATION_PLAN_INDEX.md]] | EXEC001, EXP0016 | The EXEC001 STC SMT Cycles implementation plan is documented in the strategy folder: `17_implementation_plan.md` — full staged implementation plan `18_module_br |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|LEVEL_01_STC_SMT_SKELETON.md]] | — | This patch adds the first compileable MQL5 shell for `EXEC001_STC_SMT_Cycles`. The level is deliberately safe: it validates inputs, creates runtime journals, st |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] | — | Level 05 adds the previous-W reference matrix and raw touch-only hunt detector for `EXEC001_STC_SMT_Cycles`. It is still an audit-only level. It creates no SMT  |
| [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR.md]] | EXEC001 | This level adds paper partial-close accounting for EXEC001 STC SMT Cycles. The EA remains no-order. It writes `stc_level10_partial_actions.csv` and simulates on |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
