
---
type: source_card
source_path: "lab/04_execution/EXE0003_continuation_close_hunt/README.md"
source_ext: ".md"
source_size: 5562
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "UI / React"]
entities: ["E0001", "E0002", "E0003", "E0004", "EXE0003", "M0001", "M0002"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0003_continuation_close_hunt/README|lab/04_execution/EXE0003_continuation_close_hunt/README.md]]

## Summary

This lab contains the third H5 execution path: regime: continuation trigger: structural node close-hunt or Donchian 20 breakout entry: market on the next bar position size: cash risk to `3 × ATR` stop distance by default TP: none primary exit: regime change Recommended first test: All four execution experts now support an optional higher-timeframe regime gate. The default is off, so existing tests are unchanged. Inputs: `InpUseHigherTimeframeRegimeFilter` — enable/disable the higher-timeframe regime confirmation. `InpHigherRegimeTimeframe` — timeframe used for the higher-timeframe M0001/M0002 regime calculation, default `PERIOD_H1`. `InpUseHigherTimeframeDirectionFilter` — when false, the higher timeframe only grants/blocks continuation permission; it does not restrict buy/sell direction. When true, the signal direction must match the latest higher-… Behavior: E0001 and E0002 require the

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

E0001, E0002, E0003, E0004, EXE0003, M0001, M0002

## Headings

- EXE0003 — Continuation Close-Hunt Market Execution
  - Higher-timeframe regime filter
  - Build 1.02: ATR trailing and optional regime exit
  - Build 1.03: Donchian 20 and optional lower-timeframe regime gate
  - Build 1.04: max trades and HTF direction control
  - Build 1.05: intrabar Donchian market trigger
  - Build 1.06: selectable Donchian trigger policy

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `38`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `38`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `38`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `38`
- [[docs/execution/README|README.md]] — score `38`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `38`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `38`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `38`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `36`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
