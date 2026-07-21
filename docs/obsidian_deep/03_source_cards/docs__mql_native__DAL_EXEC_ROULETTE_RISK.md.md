
---
type: source_card
source_path: "docs/mql_native/DAL_EXEC_ROULETTE_RISK.md"
source_ext: ".md"
source_size: 4243
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native"]
entities: []
---

# Source Card — DAL_EXEC_ROULETTE_RISK.md

## Source

[[docs/mql_native/DAL_EXEC_ROULETTE_RISK|docs/mql_native/DAL_EXEC_ROULETTE_RISK.md]]

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

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `5`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `5`
- [[docs/mql_native/H0007_F1_MQL5_IMPLEMENTATION|H0007_F1_MQL5_IMPLEMENTATION.md]] — score `5`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `5`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `5`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `5`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `5`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001_FULL_REVISIT_LOGIC.md]] — score `5`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `5`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001_LATEST_VISUAL_CAPS.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
