
---
type: source_card
source_path: "docs/mql_native/M0001_STRICT_NODE_MARKERS.md"
source_ext: ".md"
source_size: 1003
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node"]
entities: ["M0001"]
---

# Source Card — M0001_STRICT_NODE_MARKERS.md

## Source

[[docs/mql_native/M0001_STRICT_NODE_MARKERS|docs/mql_native/M0001_STRICT_NODE_MARKERS.md]]

## Summary

M0001 node visualization is now strict arrow-only. The visual layer no longer draws chevron wing segments for nodes and no longer draws full-chart horizontal node price lines. The only node objects are: Chevron markers are implemented as `OBJ_TREND` segments. On dense M1 charts they look like high/low tracing lines around candles. This is visually noisy and makes node inspection harder. When `InpShowNodePrices=true`: HIGH node price is written above the red down arrow LOW node price is written below the green up arrow Arrow marker anchor typing now uses `ENUM_ARROW_ANCHOR`, not `ENUM_ANCHOR_POINT`, so MetaEditor should no longer warn about implicit enum conversion.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]

## Entities

M0001

## Headings

- M0001 Strict Node Markers
  - Change
  - Why
  - Inputs
  - Price labels
  - Warning fix

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|M0001_CLEAN_ARROW_MARKERS.md]] — score `12`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001_FAST_FINAL_ONLY_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `12`
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
