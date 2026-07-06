
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md"
source_ext: ".md"
source_size: 20740
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]]

## Summary

Status: design specification Scope: read-only state projection layer above the locked Phoenix anatomy engines Primary implementation target: `FlagCountingPhoenixExperiment.mq5` + `mql5/Include/FlagCountingPhoenix/` Level 19 introduces a live **State Gate** for the Flag Counting project. This layer is not a new counting engine, not a new rally detector, not a new hook detector, and not an entry system. It is a higher-level state map that reads the already locked Phoenix anatomy outputs and stores the cur… The State Gate is the bridge between anatomy and future entry design. It must hold the current state of the market in memory and render a compact dashboard so that the operator can see, debug, and reason about the struct… The design goal is: This creates a live map such as: No buy/sell label is allowed in Level 19. The layer only stores and displays state. The following engines are locke

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Multi-Timeframe State Gate and Dashboard Specification
  - 1. Purpose
  - 2. Non-negotiable boundaries
  - 3. Cadence
  - 4. Symbol scope
  - 5. Timeframe inputs
  - 6. Dashboard role
  - 7. Dashboard inputs
  - 8. Core State Gate data model
    - 8.1 Snapshot
    - 8.2 Timeframe state
    - 8.3 Rally row

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH|FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
