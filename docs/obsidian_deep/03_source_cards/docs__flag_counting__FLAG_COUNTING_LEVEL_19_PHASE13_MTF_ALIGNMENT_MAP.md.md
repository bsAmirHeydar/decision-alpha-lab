
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md"
source_ext: ".md"
source_size: 3351
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Intermarket Divergence", "Licensing", "MQL Native", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]]

## Summary

Phase 13 adds a decision-neutral Multi-Timeframe Alignment Map above the Extreme Candidate Map. The State Gate now compares lower-slot context against higher-slot context. Default slot order is interpreted as: With the default inputs, this means: Phase 13 reads the already-built Phase 12 Extreme Candidate Map and builds pair rows between configured timeframes. It compares: It then labels the relationship with decision-neutral alignment fields. Phase 13 writes: This is the primary Phase 13 output. Each State Gate timeframe state now has: Direction relationship: Side relationship: Context role: Readiness examples: All labels remain context-only and decision-neutral. Phase 13 does not produce: It only explains whether lower-timeframe candidate extremes make sense relative to higher-timeframe context. Phase 13 extends: and adds: Phase 13 does not modify: It only reads projected Level 19 Stat

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map
  - Purpose
  - What Phase 13 does
  - New CSV
  - New per-timeframe fields
  - Alignment labels
  - What Phase 13 does not do
  - Updated exports
  - New input
  - Locked boundaries
  - Next natural phase

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
