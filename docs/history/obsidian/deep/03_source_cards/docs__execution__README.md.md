
---
type: source_card
source_path: "docs/execution/README.md"
source_ext: ".md"
source_size: 5747
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "H0005", "M0001", "M0002"]
---

# Source Card — README.md

## Source

[[docs/execution/README|docs/execution/README.md]]

## Summary

Canonical execution root: There must not be a nested `decision-alpha-lab/decision-alpha-lab` source copy. `E0001_ReversalOneToOne.mq5` implements H0005 reversal fixed-R execution. Current E0001 builds run once per closed candle, resolve the effective reversal/continuation regime from M0002 plus optional human context input, and park spread-aware pending limits on the nearest active reversal nodes: 3 nearest buy limits from LOW nodes below market by default. 3 nearest sell limits from HIGH nodes above market by default. SL is behind the zone. TP defaults to the first opposite-node touch; `InpRewardR` is an optional reference/cap when enabled. Continuation/non-reversal deletes managed pending orders. Optional time filter can block new orders outside the configured session and delete managed pending orders. H5 research reporting prints directional memory and fixed-R reversal outcome metrics

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, H0005, M0001, M0002

## Headings

- Decision Alpha Lab — Execution
  - Current execution adapter
  - MetaEditor include sync
  - Build 1.20 — strict touch/revisit ledger
    - Build 1.21 node-zone lock note
  - TP policy — first opposite node touch with optional R exit
    - Build 1.24 TP correction
    - Build 1.25 performance/compile fix
  - Minimal input surface
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `58`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `50`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `48`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `47`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `47`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `44`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `43`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
