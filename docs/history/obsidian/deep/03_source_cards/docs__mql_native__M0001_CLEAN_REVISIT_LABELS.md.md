
---
type: source_card
source_path: "docs/mql_native/M0001_CLEAN_REVISIT_LABELS.md"
source_ext: ".md"
source_size: 1062
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_CLEAN_REVISIT_LABELS.md

## Source

[[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|docs/mql_native/M0001_CLEAN_REVISIT_LABELS.md]]

## Summary

`InpShowRevisitLabels` now draws only true revisit labels. It no longer prints full event diagnostics such as: Instead, the revisit layer prints only the revisit identity: In HUNT mode: Only `REV#1+` is drawn by the revisit-label layer. TOUCH mode is one-shot: So `InpShowRevisitLabels` does not draw TOUCH mode event text. Actual revisit labels are drawn with a distinct revisit color: This makes actual revisits visually separate from normal touch, pending, consumed and hunt labels. To see only revisit text: `M0001_LiveVisualLab.mq5` version: `1.43`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Clean Revisit Labels
  - Decision
  - True revisit
  - TOUCH mode
  - Color
  - Recommended debug setup
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001_FULL_REVISIT_LOGIC.md]] — score `14`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `14`
- [[docs/mql_native/M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS|M0001_NODE_ORIGIN_ZONES_AND_REVISIT_COLORS.md]] — score `14`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001_REVISIT_EXTREME_RESET.md]] — score `14`
- [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|M0001_REVISITED_LIVE_MEMORY.md]] — score `14`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001_RTV_LOG_HILO.md]] — score `14`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001_VIEWPORT_VISUAL_RENDERER.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
