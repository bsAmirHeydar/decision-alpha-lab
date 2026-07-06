
---
type: source_card
source_path: "docs/ui/FOLDER_STRUCTURE.md"
source_ext: ".md"
source_size: 5019
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Hook", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FOLDER_STRUCTURE.md

## Source

[[docs/ui/FOLDER_STRUCTURE|docs/ui/FOLDER_STRUCTURE.md]]

## Summary

Owns: replay controls replay speed cursor position frame stepping viewport synchronization Does not own: metric calculation node detection Owns: metric run selector metric parameter display metric event table metric overlays received from API Does not own: metric computation Owns: experiment list experiment details run status experiment outputs Does not own: experiment execution logic Owns: observation tree hypothesis tree experiment linkage validation linkage production signal linkage Owns: selected object details selected candle details selected event details selected node details source traceability React components: Hooks: API functions: Types: Backend schemas: If a future metric requires a new chart behavior, add it to the shared visualization protocol first. Do not hard-code metric-specific visual behavior inside a page component.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- UI Folder Structure
  - Target Project Layout
  - Frontend Feature Boundaries
    - `features/replay`
    - `features/metrics`
    - `features/experiments`
    - `features/registry`
    - `features/inspector`
  - Naming Conventions
  - Rule

## Related Source Documents

- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `20`
- [[docs/flag_counting/README|README.md]] — score `20`
- [[docs/nds_hook_architecture/README|README.md]] — score `20`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|README.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `19`
- [[docs/ui/README|README.md]] — score `19`
- [[docs/ui/ROADMAP|ROADMAP.md]] — score `19`
- [[docs/ui/VISUALIZATION_API|VISUALIZATION_API.md]] — score `19`
- [[docs/architecture|architecture.md]] — score `18`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
