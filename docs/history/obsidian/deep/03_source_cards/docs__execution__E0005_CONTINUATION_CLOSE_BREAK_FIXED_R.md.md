
---
type: source_card
source_path: "docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md"
source_ext: ".md"
source_size: 2145
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native"]
entities: ["E0001", "E0002", "E0003", "E0004", "E0005", "H0005", "M0001", "M0002"]
---

# Source Card — E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md

## Source

[[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]]

## Summary

E0005 is the fifth H0005 execution module. It is a separate Expert Advisor. It does not modify E0001, E0002, E0003, or E0004. E0005 trades only the continuation side of H0005. A signal is valid when: The local M0002 regime is continuation. The latest fully closed candle breaks a confirmed structural node by close. The node was active before the signal candle. The same node was not already close-broken before the signal candle. The node is not already consumed by a M0001 event. Optional higher-timeframe regime filter passes. Close above a confirmed HIGH node = bullish continuation = market buy. Close below a confirmed LOW node = bearish continuation = market sell. The stop distance is ATR-based. Default: So the stop distance is: The take-profit is fixed R. Default: So the default target is 1:1 against the ATR stop distance. Examples: means 4 ATR stop and 1R target. means 4 ATR stop and 2R

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

E0001, E0002, E0003, E0004, E0005, H0005, M0001, M0002

## Headings

- E0005 — Continuation Close-Break Fixed-R Executor
  - Contract
  - Direction
  - Risk and target
  - No-future behavior
  - Higher-timeframe filter

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `44`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `44`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `44`
- [[docs/execution/README|README.md]] — score `44`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `43`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `41`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `41`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `39`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `36`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `34`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
