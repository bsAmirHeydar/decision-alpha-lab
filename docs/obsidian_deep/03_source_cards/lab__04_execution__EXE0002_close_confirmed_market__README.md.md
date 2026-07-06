
---
type: source_card
source_path: "lab/04_execution/EXE0002_close_confirmed_market/README.md"
source_ext: ".md"
source_size: 2969
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "EXE0002", "H0005", "M0001", "M0002"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0002_close_confirmed_market/README|lab/04_execution/EXE0002_close_confirmed_market/README.md]]

## Summary

This execution experiment is the second implementation of the H0005 reversal idea. It is intentionally a separate EA: It does not add a mode to `E0001_ReversalOneToOne.mq5`. When the effective regime is reversal: Build H5 reversal node candidates from M0001/M0002. Watch nearest LOW nodes below market and HIGH nodes above market. Wait for the last closed candle to touch a candidate zone. If the close does not break the far edge of the zone, enter at market. Put SL behind the zone. Put TP at the first opposite-node touch by default. `InpRewardR` is a reference/cap only if `InpUseFixedRExitIfCloser=true`. Lock that node touch until a full zone exit and later revisit. TP defaults to the first opposite-node touch. If `InpUseFixedRExitIfCloser=true`, the fixed-R target from `InpRewardR` may be used only when it is closer than that opposite touch. If `InpAllowOppositeTouchBelowRewardR=fa… The c

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, EXE0002, H0005, M0001, M0002

## Headings

- EXE0002 — Close-Confirmed Market After Touch
  - Rule
  - Recommended default test settings
  - TP policy
  - Build 1.03 performance defaults
  - Minimal input surface
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `47`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `47`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `47`
- [[docs/execution/README|README.md]] — score `47`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `45`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `43`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `42`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
