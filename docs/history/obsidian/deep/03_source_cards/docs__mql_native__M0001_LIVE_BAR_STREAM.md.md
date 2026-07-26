
---
type: source_card
source_path: "docs/mql_native/M0001_LIVE_BAR_STREAM.md"
source_ext: ".md"
source_size: 1521
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_LIVE_BAR_STREAM.md

## Source

[[docs/mql_native/M0001_LIVE_BAR_STREAM|docs/mql_native/M0001_LIVE_BAR_STREAM.md]]

## Summary

The first MQL-native version recomputed the engine by loading a whole bar window with `CopyRates()` on every update. That is convenient for research snapshots, but it does not express the strict live mental model: The active M0001 Expert now runs in live-stream mode by default. This means: The Expert does not bulk-copy history at attach time. It waits for the next newly closed candle. On each new closed candle, it reads only `shift=1`. That single bar is appended to the in-memory chronological stream. L-rule nodes, M0001 events, and visuals are recomputed from that live stream. `InpBars` is now the rolling stream capacity, not a bulk-copy request, when `InpUseLiveBarStream=true`. For research convenience, you may set: This loads only historical context at attach time. For strict forward-only visual validation, keep it at `0`. The old snapshot mode remains available: In that mode, the Exp

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Live Bar Stream
  - Problem
  - Decision
  - Inputs
  - Optional warmup
  - Fallback mode

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001_CONSUMED_NODE_REPAIR.md]] — score `12`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001_FAST_FINAL_ONLY_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `12`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `12`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `12`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `12`
- [[docs/debug/E0006/README|README.md]] — score `11`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
