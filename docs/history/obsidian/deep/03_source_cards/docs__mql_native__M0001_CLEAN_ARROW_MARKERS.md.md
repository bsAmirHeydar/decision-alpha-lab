
---
type: source_card
source_path: "docs/mql_native/M0001_CLEAN_ARROW_MARKERS.md"
source_ext: ".md"
source_size: 759
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node"]
entities: ["M0001"]
---

# Source Card — M0001_CLEAN_ARROW_MARKERS.md

## Source

[[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|docs/mql_native/M0001_CLEAN_ARROW_MARKERS.md]]

## Summary

The default node marker is now a clean `OBJ_ARROW`, not a two-segment chevron. This removes the red/green diagonal wing lines that visually tracked around candle highs/lows and made the chart noisy. Optional old chevron mode remains available: `InpShowNodePrices=true` draws a simple local text label: HIGH node: price text above the high-node arrow LOW node: price text below the low-node arrow Full horizontal price lines are still disabled by default: Use `InpNodePriceTextGapPoints` and `InpNodePriceTextFontSize` to tune readability.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]

## Entities

M0001

## Headings

- M0001 Clean Arrow Markers
  - Change
  - Inputs
  - Node price labels

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001_FAST_FINAL_ONLY_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `12`
- [[docs/mql_native/M0001_STRICT_NODE_MARKERS|M0001_STRICT_NODE_MARKERS.md]] — score `12`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `12`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `12`
- [[docs/debug/E0008/README|README.md]] — score `11`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `11`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `11`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
