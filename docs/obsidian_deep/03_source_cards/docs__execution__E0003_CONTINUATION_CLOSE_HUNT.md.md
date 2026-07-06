
---
type: source_card
source_path: "docs/execution/E0003_CONTINUATION_CLOSE_HUNT.md"
source_ext: ".md"
source_size: 7599
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "H0005", "M0001", "M0002"]
---

# Source Card — E0003_CONTINUATION_CLOSE_HUNT.md

## Source

[[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|docs/execution/E0003_CONTINUATION_CLOSE_HUNT.md]]

## Summary

`E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab. It is separate from `E0001` and `E0002`. Build 1.06 adds a selectable Donchian trigger policy: immediate intrabar tick breakout or closed-bar confirmation. When the effective continuation gate passes: The EA waits for a **closed candle**. Entry can use either: `E0003_ENTRY_CLOSE_HUNTED_NODE`: a structural node close-hunt. `E0003_ENTRY_DONCHIAN_BREAKOUT`: Donchian breakout, default period 20, with selectable trigger policy. Close-hunt model: `HIGH` node close-hunt: `close > node.price + buffer` → buy continuation. `LOW` node close-hunt: `close < node.price - buffer` → sell continuation. Donchian model: The channel is built from the previous 20 **closed** candles. `InpDonchianTriggerMode=E0003_DONCHIAN_TRIGGER_INTRABAR_TICK`: `Ask > upper + buffer` buys immediately; `Bid < lower - buffer` sells immedia

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, H0005, M0001, M0002

## Headings

- E0003 — H0005 Continuation Close-Hunt Market Executor
  - Contract
  - Why the SL exists
  - Minimal inputs
  - Logs
  - Higher-timeframe regime filter
  - Build 1.02: ATR trailing and optional regime exit
  - Build 1.03: lower-timeframe regime gate and Donchian entry
  - Build 1.04: max trades and HTF direction control
  - Build 1.05: intrabar Donchian market trigger
  - Build 1.06: selectable Donchian trigger policy

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `48`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `48`
- [[docs/execution/README|README.md]] — score `48`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `47`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `45`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `44`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `43`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
