
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md"
source_ext: ".md"
source_size: 2937
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Flag Counting", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md

## Source

[[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION|docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md]]

## Summary

This patch is not a new feature level. It does not add Level 31. It does not add execution. It adds a machine-friendly normalized CSV snapshot derived from the final no-send decision state. Consolidation Patch 02 created a human-readable final decision file. Consolidation Patch 04 creates a cleaner version for Excel, Python, dashboards, and automated reports. This is a latest-state snapshot. It is not an append ledger. The normalized CSV uses: Boolean fields are exported as integers: Examples: Direction is exported as both text and sign: Values: The normalized file adds: These are derived from: The normalized file preserves the no-send integrity check. If no-send integrity is broken and the requirement is enabled, the row is marked: This patch does not add: It remains: The next patch should be a compile-fix if MetaEditor reports errors. If compile is clean, the next engineering patch can

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization
  - Purpose
  - New output
  - New inputs
  - What is normalized
  - Boolean columns
  - Direction columns
  - Risk/reward columns
  - No-send integrity
  - Hard boundary
  - Next correct patch

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `18`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
