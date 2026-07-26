
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX.md"
source_ext: ".md"
source_size: 4188
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 13_LEVEL_13_VALIDATION_MATRIX.md

## Source

[[docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX|docs/flag_counting/implementation_ladder_v1/13_LEVEL_13_VALIDATION_MATRIX.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Level 13 turns Phoenix from a visually inspected overlay into a repeatable validation target. It runs after: The validation layer is read-only. It must never mutate events, hooks, visibility, identity, ownership, canonical state, export files from Level 11.5, or chart objects from Level 12. The EA wiring lives in: Default when validation is enabled: Unset expected ranges are reported as `WARN baseline_required` and the actual values are written to `latest_validation.csv`. This is how a new broker/range creates its first baseline. After accepting a baseline, fill the expected min/max inputs. For exact expected values, set min and max to the same number. Example: If a patch intentionally changes a count, update the case report and explain why. Expected range inputs exist for: A value of `-1` means unbo

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 13 — Validation Suite / Acceptance Matrix
  - Purpose
  - Active modules
  - Validation modes
    - Baseline mode
    - Regression mode
  - EA controls
  - Output
  - Built-in invariant checks
  - Validation case registry
  - Mandatory case families

## Related Source Documents

- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|VALIDATION_CASE_REGISTRY.md]] — score `24`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `18`
- [[docs/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md]] — score `17`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `17`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `17`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `17`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
