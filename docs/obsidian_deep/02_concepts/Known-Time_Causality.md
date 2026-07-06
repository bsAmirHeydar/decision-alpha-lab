
---
type: canonical_concept
concept: "Known-Time Causality"
generated_at: 2026-07-06
source_count: 65
---

# Known-Time Causality

## تعریف عملیاتی

اصل causal بودن: چیزی فقط وقتی قابل استفاده است که در زمان خودش known بوده باشد. برای جلوگیری از future leak و repaint حیاتی است.

## نقش در Alpha Lab

این مفهوم باید در یکی از چهار نقش زیر قرار بگیرد:

1. **زبان دیدن بازار**: کمک به خواندن ساختار.
2. **قانون تولید فرضیه**: تبدیل مشاهده به claim قابل تست.
3. **فیچر/شرط قابل اندازه‌گیری**: ورود به Python/MQL/Backtest.
4. **قید اجرایی/اعتبارسنجی**: محدود کردن خطا، repaint، leakage یا ریسک.

## روابط مستقیم

- [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]
- [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]]

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
| [[docs/articles/structural_regime_memory_without_samples|structural_regime_memory_without_samples.md]] | H0004, M0001, M0002 | A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster |
| [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] | M0001 | This document defines the strict contract used to prevent future leakage, fake sequencing, and non-tradable R statistics. For every decision candle `t`, the eng |
| [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] | D0007, H0004, H0005, M0004 | D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proo |
| [[docs/debug/D0008_H4_CAUSAL_BATCH_REPORT|D0008_H4_CAUSAL_BATCH_REPORT.md]] | D0008, H0004 | This release fixes the main H0004 live-validity ambiguity: multiple branch samples can become knowable on the same candle. The classic H0004 report sorts sample |
| [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] | D0010, H0004, M0001, M0002, M0004 | D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL |
| [[docs/debug/E0008/README|README.md]] | E0007, E0008, M0001 | E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that |
| [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4_ATOMIC_FULL_STRESS_CONTEXT.md]] | H0004, M0001, M0002 | This release restores the full stress/test surface for the official H0004 atomic no-sample report while preserving the strict contract: no M0002 branch samples  |
| [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] | M0002, M0004 | This release extends the official M0004 atomic/no-sample report without reintroducing M0002 samples or fake same-candle ordering. `sampleCalls=0` `branchSamples |
| [[docs/debug/H4_FAST_ATOMIC_EXTENDED_REPORT|H4_FAST_ATOMIC_EXTENDED_REPORT.md]] | — | This update keeps the official H4 report no-sample and fast, while restoring useful diagnostics that were previously only visible in the legacy sample report. T |
| [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] | M0001, M0002, M0004 | M0004 build 1.07 keeps the official no-sample contract but removes the heavy strict prefix replay from the default main report path. The first atomic no-sample  |
| [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] | H0006, M0001, M0002 | Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default. Still atomic and no- |
| [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] | H0006, M0001 | This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples. H6 remains atomic and no-sample: `s |
| [[docs/debug/H6_NODE_SURVIVAL_MAP|H6_NODE_SURVIVAL_MAP.md]] | H0006, M0001, M0002 | This release redefines H0006 as a chart-facing no-sample node survival map. A raw M0001 node becomes an edge-candidate level if, after its known-time candle, th |
| [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] | M0001, M0002, M0006 | Release 112 changes the official H6 chart visual from simple horizontal survivor lines to reaction-zone rectangles. Contract: Raw M0001 nodes only. No M0002 bra |
| [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] | H0004, H0006, M0006 | H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionalit |
| [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] | M0001, M0002, M0004, M0005 | This release moves the no-sample / live-style contract into the main M0004 and M0005 experts. The main reports now default to atomic raw M0001 event replay: no  |
| [[docs/glossary|glossary.md]] | — | A structural high or low where the market previously made a visible decision. A finite territory around a node. The project avoids treating structural nodes as  |
| [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] | H0001, H0002, H0004, H0005, H0006, H0007 | > Status: design lock, topology-only. > Version: v0.2 — nested `R12` rule added and expanded. > Layer: structural grammar on top of the M0001 final-only known-t |
| [[docs/principles|principles.md]] | — | Price is the only directly observable market truth. Structural memory is preferred over fixed temporal assumptions. The market x-axis is a sequence of decision  |

## Trace Targets

- Hypothesisهای مرتبط: از [[docs/obsidian_deep/04_relationships/entity_to_document_map|Entity Map]] پیدا شود.
- Experiments مرتبط: از [[docs/obsidian_deep/04_relationships/traceability_matrix|Traceability Matrix]] پیدا شود.
- Code مرتبط: از [[docs/obsidian_deep/04_relationships/code_to_concept_map|Code Map]] پیدا شود.
- تصمیم‌های معماری: در ADRها و patch notes ثبت شود.
