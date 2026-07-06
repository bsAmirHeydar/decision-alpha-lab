
---
type: source_card
source_path: "docs/articles/reversal_vs_continuation_execution.md"
source_ext: ".md"
source_size: 2762
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Path Smoothness", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "E0005", "H0005"]
---

# Source Card — reversal_vs_continuation_execution.md

## Source

[[docs/articles/reversal_vs_continuation_execution|docs/articles/reversal_vs_continuation_execution.md]]

## Summary

Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic. This article summarizes the execution lessons learned from H0005. A reversal setup asks whether a structural zone can create a reaction when price revisits it. Important properties: entry is usually a zone touch, the edge may be short-lived, full structural targets can be too ambitious, same-bar target/stop ambiguity can be high on larger timeframes, costs and fill price matter heavily. A reversal report must therefore include: touch-based entry, zone-edge or structural invalidation stop, fixed R or first-opposite-zone target, same-bar policy, spread-aware entry/stop. A structural path report may show that zones react. It does not prove that a reversal EA is profitable. A continuation setup asks whether a broken structural state can produce a larg

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, E0005, H0005

## Headings

- Article — Reversal vs Continuation Execution
  - Abstract
  - Reversal is a reaction problem
  - Continuation is a path problem
  - Why old continuation PF was not enough
  - Recommended execution split
    - Reversal family
    - Continuation family
  - Final rule

## Related Source Documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `35`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `34`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `33`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `33`
- [[docs/execution/README|README.md]] — score `33`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `33`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `33`
- [[lab/06_production/EXECUTION_FAMILIES/README|README.md]] — score `33`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `31`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `28`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
