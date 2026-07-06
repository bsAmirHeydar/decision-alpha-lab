
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL.md"
source_ext: ".md"
source_size: 5727
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Validation / Audit"]
entities: []
---

# Source Card — 00_GOVERNANCE_AND_FREEZE_PROTOCOL.md

## Source

[[docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL|docs/flag_counting/implementation_ladder_v1/00_GOVERNANCE_AND_FREEZE_PROTOCOL.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on th… Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. The decision source for every Phoenix patch is: If a ladder file, engineering-pack file, repair note, README, or legacy document confli

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Flag Counting Implementation Ladder V1
  - Level 00 — Governance and Freeze Protocol
  - Canon source rule
    - Problem this layer solves
    - Rule 1 — Every patch must name its layer
    - Rule 2 — Lower layers are frozen after acceptance
    - Rule 3 — Renderer cannot fix engine defects
    - Rule 4 — Hook/ND cannot starve F structures
    - Rule 5 — Fail-open is a diagnostic mode, not a semantic truth
    - Rule 6 — Audit before visual elegance
    - Rule 7 — Do not mix main chart and audit chart
    - Rule 8 — Every output must be deterministic

## Related Source Documents

- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `22`
- [[docs/flag_counting/README|README.md]] — score `22`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `22`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `20`
- [[docs/experience_capture/questions/README|README.md]] — score `20`
- [[docs/flag_counting/engineering_pack_v5/README|README.md]] — score `20`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|README.md]] — score `20`
- [[docs/ai_execution/README|README.md]] — score `18`
- [[docs/debug/E0008/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
