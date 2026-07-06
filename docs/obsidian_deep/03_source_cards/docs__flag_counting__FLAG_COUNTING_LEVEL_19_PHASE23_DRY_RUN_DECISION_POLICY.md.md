
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md"
source_ext: ".md"
source_size: 3657
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md]]

## Summary

Phase 23 adds a dry-run decision policy above the Phase 22 Paper Filter Diagnostics layer. This phase still does **not** send real orders. It converts paper regime attribution and filter diagnostics into a policy gate that can allow or block a **dry-run only** decision. The policy can allow a dry-run row, but it never enables real execution. Phase 23 writes: Each State Gate timeframe state now stores: The State Gate snapshot now stores: Examples: The score is diagnostic and paper-only. It rewards: It penalizes: The score is capped to: Examples: Examples: Phase 23 is the first policy gate, but it is deliberately not an execution gate. It does not say: It only says whether a context is worth a dry-run policy row. Every Phase 23 policy row keeps: Phase 23 does not modify: It only reads paper regime, paper result, paper portfolio, and filter diagnostic context. The next phase can be: That ph

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 23 Dry-Run Decision Policy
  - Purpose
  - Hard safety contract
  - New CSV
  - New input
  - New per-timeframe fields
  - New snapshot-level fields
  - Policy names
  - Policy score
  - Policy block reasons
  - Policy status
  - Design boundary

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
