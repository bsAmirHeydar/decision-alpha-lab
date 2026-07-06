
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md"
source_ext: ".md"
source_size: 10180
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_STATE_MACHINE_V3.md

## Source

[[docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3|docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V3.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This document converts the sequence contract into a deterministic state machine. It is intended for implementation in MQL5 or any other detector backend. The state machine must operate on high/low nodes only. Every sequence has: A sequence never restarts at F1 after F1 has confirmed. The sequence advances in order. Use explicit statuses instead of implicit boolean flags. Display policy: Allowed entry points: after ND/Hook, after an opposite sequence endpoint, after an F3 lock triggered by the first smallest confirmed opposite F1. Transition: Do not transition on raw four-node windows without sequence origin. The engine builds: Bull

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting State Machine V3
  - 1. Global State Principles
  - 2. Event Statuses
  - 3. Sequence States
    - 3.1 WAITING_FOR_F1
    - 3.2 F1_BODY_LIVE
    - 3.3 F1_POST_FLAG_CORRECTION
    - 3.4 SEEKING_F2
    - 3.5 F2_BODY_LIVE
    - 3.6 F2_POST_FLAG_CORRECTION
    - 3.7 SEEKING_F3
    - 3.8 F3_BODY_LIVE

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `25`
- [[docs/principles|principles.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX|FLAG_COUNTING_LEVEL_19_PHASE8_PANEL_VISIBILITY_FIX.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
