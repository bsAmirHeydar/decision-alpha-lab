
---
type: source_card
source_path: "docs/mql_native/M0001_HARD_CLEAN_VISUAL.md"
source_ext: ".md"
source_size: 993
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "MQL Native"]
entities: ["M0001"]
---

# Source Card — M0001_HARD_CLEAN_VISUAL.md

## Source

[[docs/mql_native/M0001_HARD_CLEAN_VISUAL|docs/mql_native/M0001_HARD_CLEAN_VISUAL.md]]

## Summary

The chart still showed red/blue lines tracking candle highs/lows. These lines were not part of the desired node output. Desired node output: No high/low trace lines, no chevron wings, no indicator traces. The Expert now has hard cleanup controls: `InpPurgeTraceLines` deletes trend/channel style chart objects on every redraw. `InpPurgeMainWindowIndicators` removes main-window indicators on init, useful when ZigZag-style traces remained attached to the chart. Node price labels now use separate gaps: This moves high labels higher and low labels lower for readability. `M0001_LiveVisualLab.mq5` version: `1.15`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

M0001

## Headings

- M0001 Hard Clean Visual
  - Problem
  - Fix
  - Price label spacing
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001_CLEAN_REVISIT_LABELS.md]] — score `12`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001_FULL_REVISIT_LOGIC.md]] — score `12`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `12`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS.md]] — score `12`
- [[docs/mql_native/M0001_PROJECT_REPORT_SYNC|M0001_PROJECT_REPORT_SYNC.md]] — score `12`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001_REVISIT_EXTREME_RESET.md]] — score `12`
- [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|M0001_REVISITED_LIVE_MEMORY.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
