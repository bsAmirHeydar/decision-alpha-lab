
---
type: source_card
source_path: "docs/experience_capture/answers/ENT-R03/notes_en.md"
source_ext: ".md"
source_size: 4164
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Python Brain", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — notes_en.md

## Source

[[docs/experience_capture/answers/ENT-R03/notes_en|docs/experience_capture/answers/ENT-R03/notes_en.md]]

## Summary

This answer should be treated as: The pending order engine should not keep orders alive only because they have not expired by time. It should re-check the reason set. Recommended flow: This should happen before any broker send or pending order maintenance. Which reasons are core reasons versus secondary reasons? Does any core reason failure cancel immediately? Can a pending order remain alive if reasons are weakened but not invalidated? Should weakened reasons move the order to `PENDING_LIMIT_REASON_WEAKENED`? Is time expiration ever allowed as a secondary safety rule? What exactly defines a missed limit? Can a missed order remain eligible for replacement? Should replacement require a new `pending_limit_id`? Can replacement occur inside the same reason set, or must it create a new reason set? If a better entry appears while the old order is still valid, should the old order be canceled?

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- ENT-R03 — Notes and Open Questions
  - Classification
  - Core Hard Rules
  - Core Learnable Policies
  - Proposed Objects
  - Proposed Datasets
  - Proposed Fields
  - Proposed Labels
  - Proposed AI Modules
  - Architecture Consequence
  - Open Questions
  - Attachment Index

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `22`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `18`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `18`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `18`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `18`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `18`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `16`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
