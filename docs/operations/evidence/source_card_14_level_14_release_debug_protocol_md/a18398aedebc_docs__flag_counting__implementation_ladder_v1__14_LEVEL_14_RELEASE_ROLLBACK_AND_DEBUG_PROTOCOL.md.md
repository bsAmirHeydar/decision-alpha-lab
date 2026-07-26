
---
type: source_card
source_path: "docs/contexts/legacy/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md"
source_ext: ".md"
source_size: 9329
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md

## Source

[[docs/contexts/legacy/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL|docs/contexts/legacy/flag_counting/implementation_ladder_v1/14_LEVEL_14_RELEASE_ROLLBACK_AND_DEBUG_PROTOCOL.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on th… Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. Level 14 makes Phoenix operationally safe. It prevents losing time to stale MetaTrader `.ex5` files, stale chart objects, ambiguous deb

## Concepts

[[docs/history/obsidian/deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/history/obsidian/deep/02_concepts/Decision_Node|Decision Node]], [[docs/history/obsidian/deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/history/obsidian/deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/history/obsidian/deep/02_concepts/Hook|Hook]], [[docs/history/obsidian/deep/02_concepts/MQL_Native|MQL Native]], [[docs/history/obsidian/deep/02_concepts/Python_Brain|Python Brain]], [[docs/history/obsidian/deep/02_concepts/UI____React|UI / React]], [[docs/history/obsidian/deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Level 14 — Release, Rollback, and Debug Protocol
  - Purpose
  - Implemented modules
  - Runtime order
  - Release profiles
    - normal
    - clean_main
    - audit_export
    - validation
    - debug_max
    - render_off

## Related Source Documents

- [[docs/contexts/legacy/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `19`
- [[docs/contexts/legacy/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `19`
- [[docs/contexts/legacy/flag_counting/implementation_ladder_v1/README|README.md]] — score `19`
- [[docs/operations/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `18`
- [[docs/contexts/legacy/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
