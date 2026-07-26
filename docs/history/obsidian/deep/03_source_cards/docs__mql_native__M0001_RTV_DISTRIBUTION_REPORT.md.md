
---
type: source_card
source_path: "docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT.md"
source_ext: ".md"
source_size: 913
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_RTV_DISTRIBUTION_REPORT.md

## Source

[[docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT|docs/mql_native/M0001_RTV_DISTRIBUTION_REPORT.md]]

## Summary

This document describes the older verbose distribution-report phase from version `1.53`. The active runtime no longer includes: The current active report is the compact final-only node-vs-random logRTV report: The active statistical module is: It still preserves the important distribution logic in compact form: raw RTV mean/median/percentiles, logRTV mean/median, positive logRTV percentage, skewness, excess kurtosis, Jarque-Bera statistic, KS distance to fitted normal, tail ratios, node-vs-random paired comparison. For current semantics, use:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 RTV Distribution Report — Retired Module Note

## Related Source Documents

- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `19`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `18`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `17`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `17`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001_CLEAN_REVISIT_LABELS.md]] — score `12`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
