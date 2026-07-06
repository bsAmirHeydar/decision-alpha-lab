
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT.md"
source_ext: ".md"
source_size: 1459
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Flag Counting", "Hook", "Rally", "UI / React"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE25B_RESPONSIVE_PANEL_LAYOUT.md]]

## Summary

This patch redesigns the State Gate panel layout so it adapts better to different chart resolutions and monitor sizes. The panel now reads the chart pixel width and height at runtime. Width is chosen responsively instead of staying fixed. Font size and row height are reduced automatically on smaller charts. The panel position is clamped inside the visible chart area. The content switches between roomy, compact, and ultra-compact rendering modes. Rally and Hook preview rows are reduced automatically on smaller screens. Section buttons remain intact: main minimize button per-timeframe collapse button Rally collapse button Hook collapse button Keep the dashboard readable on: lower-resolution monitors smaller chart windows different DPI / monitor configurations larger monitors where more detail can still be shown The panel now chooses among these display styles automatically: **Roomy**: larg

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 25B Responsive Panel Layout
  - What changed
  - Goal
  - Rendering modes
  - Safety

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY|FLAG_COUNTING_LEVEL_19_PHASE23_DRY_RUN_DECISION_POLICY.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md]] — score `11`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
