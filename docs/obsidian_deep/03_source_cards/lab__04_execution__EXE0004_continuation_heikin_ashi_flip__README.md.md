
---
type: source_card
source_path: "lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README.md"
source_ext: ".md"
source_size: 1896
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "UI / React"]
entities: ["E0001", "E0002", "E0003", "E0004", "EXE0004", "H0005", "M0001", "M0002"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README.md]]

## Summary

Fourth execution adapter for the H0005 continuation side. When the market regime is continuation, use Heikin Ashi color flips as repeated entries in the continuation direction. On each closed candle: regime = continuation; current HA candle color differs from previous HA candle color; current HA color agrees with the inferred continuation direction; enter at market. Fixed reward model: SL: opposite edge of the signal Heikin Ashi candle; TP: `InpRewardR`, default `2.0R`. `InpAllowSimultaneousTrades` decides whether repeated signals can stack positions or whether only one E0004 position can be open at a time. The stop is no longer only the signal Heikin Ashi candle edge. For buys, E0004 uses the lower/farther stop from the signal HA low and the last-three-candle low. For sells, it uses the higher/farther stop from the signal… All four execution experts now support an optional higher-timefr

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

E0001, E0002, E0003, E0004, EXE0004, H0005, M0001, M0002

## Headings

- EXE0004 — Continuation Heikin Ashi Flip
  - Idea
  - Signal
  - Exit
  - Simultaneous trades
  - Build 1.01 stop update
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `43`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `43`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `43`
- [[docs/execution/README|README.md]] — score `43`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `43`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `43`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `41`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `38`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `31`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
