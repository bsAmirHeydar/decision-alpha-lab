
---
type: source_card
source_path: "mql5/Include/Execution/README_DAL_ExecRouletteRisk.md"
source_ext: ".md"
source_size: 4243
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native"]
entities: []
---

# Source Card — README_DAL_ExecRouletteRisk.md

## Source

[[mql5/Include/Execution/README_DAL_ExecRouletteRisk|mql5/Include/Execution/README_DAL_ExecRouletteRisk.md]]

## Summary

`DAL_ExecRouletteRisk` is a reusable MQL5 execution-risk module. It returns **money risk** only. It does not send orders, decide entries, or decide exits. Each cycle stores: Default inputs: At cycle start: Example: If the account moves down but stays inside the protected band: risk remains fixed: Example: The risk does not shrink on every small loss. If balance breaks below the protected floor, the base account used for lot calculation must update downward. Rule: Example: The cycle re-locks: This is the corrected rule: the base does not follow every loss, but it does follow the account down after the protected floor is broken. The cycle becomes profit-active only after balance rises above the locked balance: Then risk can grow from the distance above the floor: Example: Then: If the account first creates a profit cluster and then one realized loss occurs, the old cycle ends immediately.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- DAL_ExecRouletteRisk — Roulette Execution Risk Model
  - Core state
  - Losing-side floor band
  - Downside floor break
  - Profit-active rule
  - Profit cluster then loss re-lock
  - Final behavior summary
  - Safety contract

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/architecture|architecture.md]] — score `4`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `4`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `4`
- [[docs/debug/E0006/MODULE_KERNEL_README|MODULE_KERNEL_README.md]] — score `4`
- [[docs/debug/E0006/README|README.md]] — score `4`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `4`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]] — score `4`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `4`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
