
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP.md"
source_ext: ".md"
source_size: 1951
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "UI / React", "Zone / RTV"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP|docs/flag_counting/FLAG_COUNTING_LEVEL_19A_SILENT_DEFAULTS_AND_LIFECYCLE_CLEANUP.md]]

## Summary

Level 19A applies two operational safety changes requested after the clean Level 19 rebuild. All EA input defaults with `InpPrint...` are now set to: The input switches are still present, so any diagnostic print can be enabled manually when needed. Additional print controls were added: This means normal chart usage is silent by default. Object cleanup is now explicit for important lifecycle events: The EA cleans chart objects by the renderer prefix: So when: old drawings are removed and the fresh run can draw the new timeframe/state cleanly. This patch does not modify renderer source files: It also does not change: The drawing cleanup uses the existing renderer object prefix and lifecycle hooks. It does not change how lines or curves are calculated. The print change only changes input defaults and adds explicit print gates for summary/failure/license logs.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Flag Counting Level 19A — Silent Defaults and Lifecycle Cleanup
  - Purpose
  - Change 1 — Prints disabled by default
  - Change 2 — Lifecycle object cleanup
  - Important no-touch boundary
  - Why this is safe

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND|FLAG_COUNTING_LEVEL_26_BROKER_VALIDATOR_NO_SEND.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
