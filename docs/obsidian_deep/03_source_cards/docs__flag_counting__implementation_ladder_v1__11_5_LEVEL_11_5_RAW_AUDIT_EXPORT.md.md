
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md"
source_ext: ".md"
source_size: 5216
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md

## Source

[[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md]]

## Summary

Level 11.5 makes the Phoenix engine auditable as data before Level 12 renderer/layout work. The chart is useful, but it is not proof. The export layer serializes the final Level 11 canonical stream into stable CSV files… Pipeline position: Level 11.5 is read-only. It may: It may not: Default output folder: Default overwrite mode: Validation mode may set: `events.csv` exports both visible and hidden events by default. Each row includes: This is intentionally wide. The goal is debugability, not compactness. `hooks.csv` exports both visible and hidden Hook/ND contexts by default. Each row includes: `summary.csv` is a one-row aggregate view with core counters: `manifest.csv` is key/value metadata: When enabled, terminal output includes: `FP_SUMMARY` also includes export counters so export failures are visible in the normal run summary. With `InpExportAuditFiles=false`, no files are written a

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Level 11.5 — Raw Audit Export / Report Engine
  - Purpose
  - Active files
  - Authority boundary
  - Inputs
  - Inputs added to EA
  - Output path
  - Event CSV contract
  - Hook CSV contract
  - Summary CSV contract
  - Manifest CSV contract
  - Sanity log

## Related Source Documents

- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `20`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `19`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `19`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `18`
- [[docs/flag_counting/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
