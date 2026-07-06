
---
type: source_card
source_path: "docs/debug/E0006/MODULE_KERNEL_README.md"
source_ext: ".md"
source_size: 6061
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0006", "M0001"]
---

# Source Card — MODULE_KERNEL_README.md

## Source

[[docs/debug/E0006/MODULE_KERNEL_README|docs/debug/E0006/MODULE_KERNEL_README.md]]

## Summary

This document describes the reusable modules extracted from the E0006 execution work. The goal is to stop rewriting the same structural ideas inside every EA and instead compose them from small, testable pieces. E0006 accumulated several independent ideas: origin zones from M0001 structural nodes, internal same-side hunt qualification, optional revisit-only entries, node-price versus zone-back stop anchoring, pending-order and open-position side caps, zero initial fixed-R TP with an internal opposite-node TP manager, strict new-candle synchronization instead of tick-heavy computation. Each idea is useful alone. A future executor may want only the internal-hunt filter, only the N-th opposite-node exit, or only the exposure caps. The new module layer breaks those ideas into reusable include files. `DAL_E0006Modules.mqh` is the facade include. A new EA can include only that header and recei

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0006, M0001

## Headings

- E0006 Modular Execution Kernel
  - Why this layer exists
  - Files
  - 1. Types and policies
  - 2. Internal hunt qualification
  - 3. Zone pricing and stop anchoring
  - 4. Revisit-only cycle qualification
  - 5. Internal opposite-node TP
  - 6. Exposure caps
  - Suggested future migration
  - Design rule

## Related Source Documents

- [[docs/debug/E0006/README|README.md]] — score `23`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `22`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `22`
- [[docs/debug/E0006/ENTRY_QUALIFICATION_README|ENTRY_QUALIFICATION_README.md]] — score `19`
- [[docs/debug/E0006/EXIT_AND_RISK_README|EXIT_AND_RISK_README.md]] — score `19`
- [[docs/debug/E0006/INPUT_REFERENCE_README|INPUT_REFERENCE_README.md]] — score `19`
- [[docs/debug/E0006/REVISIT_ONLY_README|REVISIT_ONLY_README.md]] — score `19`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `17`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `17`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
