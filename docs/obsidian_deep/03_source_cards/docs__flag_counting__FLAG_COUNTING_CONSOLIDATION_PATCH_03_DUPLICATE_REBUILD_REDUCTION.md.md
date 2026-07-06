
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_03_DUPLICATE_REBUILD_REDUCTION.md"
source_ext: ".md"
source_size: 3133
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Flag Counting", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_CONSOLIDATION_PATCH_03_DUPLICATE_REBUILD_REDUCTION.md

## Source

[[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_03_DUPLICATE_REBUILD_REDUCTION|docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_03_DUPLICATE_REBUILD_REDUCTION.md]]

## Summary

This patch is not a new feature level. It does not add Level 31. It does not add execution. It reduces repeated internal rebuilds in the no-send chain by reusing the latest-row caches introduced in Consolidation Patch 01. The no-send chain was correct but repetitive. For example: That was safe, but heavy and noisy. It also meant some internal dedupe counters could be touched more often than necessary. The engines now prefer cached rows when available. If a required cache is missing, the engine falls back to the previous rebuild path. Fallback is preserved intentionally. This means the modules still work if a previous layer is disabled or has not run. The fallback rebuild path also refreshes the relevant context caches so Consolidation Patch 01 and Patch 02 continue to have the latest available state. This patch preserves the existing outputs: This patch also ensures Level 27 through Leve

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting — Consolidation Patch 03 / Duplicate Rebuild Reduction
  - Purpose
  - Problem before this patch
  - What changed
  - Fallback behavior
  - Outputs preserved
  - Context-cache fix
  - Hard boundary
  - Next correct patch

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT|FLAG_COUNTING_CONSOLIDATION_PATCH_01_NO_SEND_CONTEXT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE|FLAG_COUNTING_CONSOLIDATION_PATCH_02_FINAL_DECISION_STATE.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION|FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
