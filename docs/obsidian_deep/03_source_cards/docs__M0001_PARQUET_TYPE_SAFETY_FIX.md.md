
---
type: source_card
source_path: "docs/M0001_PARQUET_TYPE_SAFETY_FIX.md"
source_ext: ".md"
source_size: 862
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Python Brain", "UI / React"]
entities: ["M0001"]
---

# Source Card — M0001_PARQUET_TYPE_SAFETY_FIX.md

## Source

[[docs/M0001_PARQUET_TYPE_SAFETY_FIX|docs/M0001_PARQUET_TYPE_SAFETY_FIX.md]]

## Summary

`visual_rows` contains drawing rows where some fields are not applicable for every row. For example, `NODE_PRICE` has `price`, while `EVENT` rows use `lower` and `upper`. The CSV adapter can represent missing fields as blank strings, but Parquet requires stable column types. Typical error: Before writing Parquet, the Python bridge now normalizes DataFrames: numeric columns are converted with `pd.to_numeric(..., errors="coerce")` blank strings become nullable values booleans become nullable boolean columns non-numeric/object fields become strings This keeps the Parquet artifacts stable while the thin CSV render adapter remains compatible with MQL.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

M0001

## Headings

- M0001 Parquet Type Safety Fix
  - Problem
  - Fix

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `12`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `12`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001_NODE_ARROW_TIP_ANCHOR_FIX.md]] — score `12`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]] — score `12`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `12`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `12`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `12`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `12`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `11`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
