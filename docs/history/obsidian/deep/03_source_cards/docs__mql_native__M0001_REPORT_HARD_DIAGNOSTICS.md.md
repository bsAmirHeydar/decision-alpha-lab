
---
type: source_card
source_path: "docs/mql_native/M0001_REPORT_HARD_DIAGNOSTICS.md"
source_ext: ".md"
source_size: 1196
empty: false
generated_at: 2026-07-06
concepts: ["MQL Native", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_REPORT_HARD_DIAGNOSTICS.md

## Source

[[docs/mql_native/M0001_REPORT_HARD_DIAGNOSTICS|docs/mql_native/M0001_REPORT_HARD_DIAGNOSTICS.md]]

## Summary

Report generation now has hard diagnostics and fallback behavior. If `InpWriteExcelReport=true`, the expert immediately writes probe files: If these files are not created, the EA is not running with report writing enabled, the compiled version is not the new one, or MT5 file I/O is failing. The expert prints: If writing to the project-relative sandbox path fails: the writer falls back to the root MT5 Files sandbox: `M0001_LiveVisualLab.mq5` version: `1.36`.

## Concepts

[[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Report Hard Diagnostics
  - Fix
  - Inputs
  - What happens on init
  - Experts log messages
  - Fallback
  - Version

## Related Source Documents

- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `17`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `17`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `17`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `10`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `10`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `10`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `10`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `10`
- [[docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE|M0001_EXCEL_REPORT_RELIABLE_WRITE.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
