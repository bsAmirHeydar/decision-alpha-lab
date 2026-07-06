
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md"
source_ext: ".md"
source_size: 3269
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]]

## Summary

Phase 7 keeps the Level 19 State Gate read-only and improves usability. The objective is not to add entry logic. The objective is to make the State Gate visible, readable, and debuggable while preserving the locked Node / Hook / ND / F-counting engines. Phase 7 introduces four usability changes: The panel defaults to the **left-upper** chart corner instead of the right-upper corner. The panel still supports a **master minimize / restore** button. Each timeframe block supports its own **section minimize / restore** button. Inside every expanded timeframe block, the **Rally** subsection and the **Hook** subsection each have their own minimize / restore toggle. This means the State Gate can be inspected progressively: whole dashboard collapsed or expanded M1 / M10 / H1 blocks collapsed or expanded independently Rally lines collapsed or expanded independently Hook lines collapsed or expanded

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 7 Left-Upper Panel and Section Toggles
  - Purpose
  - What changed
  - Locked boundaries
  - Inputs
  - Chart interactions
    - Master panel button
    - Timeframe buttons
    - Subsection buttons
  - Rendering rules
  - Why this matters
  - Files touched

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `23`
- [[docs/flag_counting/README|README.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE9_VISUAL_DEBUG_CONTRACT.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `23`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
