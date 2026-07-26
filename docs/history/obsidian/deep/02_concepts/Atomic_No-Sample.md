
---
type: canonical_concept
concept: "Atomic No-Sample"
generated_at: 2026-07-06
source_count: 32
---

# Atomic No-Sample

## تعریف عملیاتی

رویکرد sample-free/atomic برای ارزیابی ساختارهای بازار بدون اتکا به توهم نمونه‌گیری یا داده‌های آینده.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]]
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
| [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] | M0001 | This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the eng |
| [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] | D0009, M0001 | D0009 is the strict H5 validator for the "do not build samples first" contract. It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002Branch |
| [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] | D0010, H0004, M0001, M0002, M0004 | D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL |
| [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] | H0004, M0001, M0002 | This release restores the full stress/test surface for the official H0004 atomic no-sample report while preserving the strict contract: no M0002 branch samples  |
| [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] | M0002, M0004 | This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamples |
| [[docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT|H4_FAST_ATOMIC_EXTENDED_REPORT.md]] | — | This update keeps the official H4 report no-sample and fast, while restoring useful diagnostics that were previously only visible in the legacy sample report. T |
| [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] | M0001, M0002, M0004 | M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path. The first atomic no-sample  |
| [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] | H0006, M0001, M0002 | Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default. Still atomic and no- |
| [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] | H0006, M0001 | This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples. H6 remains atomic and no-sample: `s |
| [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] | H0006, M0001, M0002 | This release redefines H0006 as a chart-facing no-sample node survival map. A raw M0001 node becomes an edge-candidate level if, after its known-time candle, th |
| [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] | H0004, H0006, M0006 | H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionalit |
| [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] | M0001, M0002, M0004, M0005 | This release moves the no-sample / live-style contract into the main M0004 and M0005 experts. The main reports now default to atomic raw M0001 event replay: no  |
| [[docs/glossary|glossary.md]] | — | A structural high or low where the market previously made a visible decision. A finite territory around a node. The project avoids treating structural nodes as  |
| [[docs/principles|principles.md]] | — | Price is the only directly observable market truth. Structural memory is preferred over fixed temporal assumptions. The market x-axis is a sequence of decision  |
| [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] | H0004, H0005, M0001, M0002 | This report summarizes the project findings from the GOLD M10 H4/H5 logs and the subsequent code-audit discussion. Instrument: GOLD Timeframe: M10 Bars: approxi |
| [[docs/research-roadmap|research-roadmap.md]] | — | Objective: determine whether decision nodes can be systematically extracted from price. Status: active foundation. Objective: model structural nodes as zones wi |
| [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] | D0009, D0010, H0004, H0005 | This document records the most important lessons learned during the H0004 and H0005 development process. Completed branch samples are useful for discovery. They |
| [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] | H0004, H0005, M0001, M0002 | Do reversal and continuation branch regimes display persistence beyond random ordering when measured by the time at which the regime became knowable? The classi |
| [[docs/evidence/h0005_directional_memory_execution/57d9666c6533_H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] | H0005, M0001 | If the latest known structural regime is reversal or continuation, does it improve the next structural decision in a way that can become executable alpha? The o |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
