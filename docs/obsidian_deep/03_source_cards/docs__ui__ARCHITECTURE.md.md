
---
type: source_card
source_path: "docs/ui/ARCHITECTURE.md"
source_ext: ".md"
source_size: 5000
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — ARCHITECTURE.md

## Source

[[docs/ui/ARCHITECTURE|docs/ui/ARCHITECTURE.md]]

## Summary

Build a professional, extensible visual research terminal for Decision Alpha Lab while preserving strict separation between research logic and presentation logic. Responsibilities: render the visual lab terminal replay candles through time display overlays returned by the API synchronize chart selections with table selections expose filters, toggles, and inspectors call backend endpoints through typed clients Forbidden: calculating structural nodes calculating metric values deciding event validity mutating research results without explicit backend action Responsibilities: expose market data to the UI expose structural nodes to the UI expose metric runs and event rows to the UI expose experiment and validation metadata normalize research outputs into visualization contracts stream replay frames when needed Forbidden: duplicating metric logic outside the lab modules creating UI-only interp

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- UI System Architecture
  - Objective
  - High-Level Architecture
  - Layer Responsibilities
    - 1. Frontend — `apps/web`
    - 2. API — `apps/api`
    - 3. Research Lab — `lab/`
    - 4. Cache Layer — `lab/cache_*`
  - UI Domain Model
  - Central UI Contract
  - Runtime Modes
    - Cache Mode

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `20`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `18`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `14`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `14`
- [[docs/ui/README|README.md]] — score `13`
- [[docs/ui/ROADMAP|ROADMAP.md]] — score `13`
- [[docs/ui/VISUALIZATION_API|VISUALIZATION_API.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
