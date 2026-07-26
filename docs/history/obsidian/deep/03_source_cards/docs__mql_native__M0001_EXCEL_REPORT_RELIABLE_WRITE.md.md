
---
type: source_card
source_path: "docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE.md"
source_ext: ".md"
source_size: 908
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "MQL Native", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_EXCEL_REPORT_RELIABLE_WRITE.md

## Source

[[docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE|docs/mql_native/M0001_EXCEL_REPORT_RELIABLE_WRITE.md]]

## Summary

Excel report writing now creates missing folders before `FileOpen` and prints success/failure messages to the Experts log. `InpExcelReportUseFullHistorySnapshot=true` writes a report-only CopyRates snapshot for full-history validation. It does not affect the live-stream engine or trading logic. This is useful when: because the runtime stream can be empty at init while a full report is still needed for research validation. In Strategy Tester, MetaTrader writes files under the tester agent sandbox, not always the normal terminal `MQL5\Files` folder. `M0001_LiveVisualLab.mq5` version: `1.34`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Reliable Excel Report Writing
  - Fix
  - Inputs
  - Output
  - Version

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `17`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `17`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `12`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001_PROJECT_REPORT_SYNC.md]] — score `12`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001_RTV_LOG_HILO.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
