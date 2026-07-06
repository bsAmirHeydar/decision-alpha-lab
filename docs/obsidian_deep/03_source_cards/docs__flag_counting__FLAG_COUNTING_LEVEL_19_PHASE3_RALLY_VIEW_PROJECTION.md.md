
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md"
source_ext: ".md"
source_size: 7399
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE3_RALLY_VIEW_PROJECTION.md]]

## Summary

Status: implemented design note Parent spec: `FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md` Parent implementation plan: `FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md` Phase 3 upgrades Level 19 State Gate from a closed-bar tracker into the first real anatomy projection layer. Phase 2 answered: Phase 3 now also answers: This is still not an entry engine. It does not answer: It only maps the locked Phoenix F1/F2/F3 output into a live multi-timeframe State Gate snapshot. Phase 3 does not change any locked anatomy logic. It does not edit or override: The new code only reads already-built Phoenix event fields. The direction is strictly: No reverse dependency is allowed. Phase 3 adds Rally View projection for the three configured State Gate timeframes. Default timeframes remain: They remain configurable through the existing Level 19 inputs. For each timeframe, Phase 3 builds

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 3 Rally View Projection
  - 1. Purpose
  - 2. Non-negotiable boundary
  - 3. What Phase 3 adds
  - 4. Rally View definition
  - 5. Row selection
  - 6. Latest established F
  - 7. Probable next F
  - 8. Body state labels
  - 9. In-flag stage labels
  - 10. Post-flag stage labels
  - 11. CSV output

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `31`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `31`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH|FLAG_COUNTING_LEVEL_19_PHASE5_PANEL_POLISH.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE|FLAG_COUNTING_LEVEL_19_PHASE6_STATE_CONTRACT_STORAGE.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
