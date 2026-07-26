
---
type: source_card
source_path: "lab/06_production/EXECUTION_FAMILIES/README.md"
source_ext: ".md"
source_size: 1616
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "E0005"]
---

# Source Card — README.md

## Source

[[lab/06_production/EXECUTION_FAMILIES/README|lab/06_production/EXECUTION_FAMILIES/README.md]]

## Summary

This document summarizes the current execution families implied by the research. Purpose: capture reaction from structural zones. Expected members: E0001 — reversal touch/limit execution, E0002 — close-confirmed market reversal execution. Core rules: entry after valid regime is known, zone touch or close confirmation, zone-edge or structural invalidation stop, fixed R or first opposite zone target, same-bar stop-first policy unless tick data proves ordering. Main risk: full structural reversal targets can be too ambitious, same-bar target/stop ambiguity can be high, costs can destroy small reaction edges. Purpose: capture larger path after structural break in continuation regime. Expected members: E0003 — continuation close-hunt / Donchian / ATR trailing, E0004 — Heikin Ashi continuation flip, E0005 — close-break fixed-R continuation. Core rules: entry after continuation regime is known,

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, E0005

## Headings

- Execution Families
  - Reversal execution family
  - Continuation execution family
  - Family-level reporting

## Related Source Documents

- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `28`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `27`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `26`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `26`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `26`
- [[docs/execution/README|README.md]] — score `26`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `26`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `26`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `24`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
