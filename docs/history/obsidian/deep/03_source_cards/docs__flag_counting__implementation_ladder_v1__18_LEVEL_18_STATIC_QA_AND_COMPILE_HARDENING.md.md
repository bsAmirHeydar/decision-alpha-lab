
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING.md"
source_ext: ".md"
source_size: 2522
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING.md

## Source

[[docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING|docs/flag_counting/implementation_ladder_v1/18_LEVEL_18_STATIC_QA_AND_COMPILE_HARDENING.md]]

## Summary

Level 18 is an extension after the original Level 17 decision lock. It exists because the Phoenix engine became large enough that runtime logic can be correct while MQL5 compile hazards still break execution. This layer is **read-only**. It does not create, mutate, hide, reveal, confirm, invalidate, lock, re-parent, export, render, validate, release, accept, or reinterpret market structures. Level 18 hardens Phoenix against recurring MQL5 failure modes: empty `Print()` calls oversized multi-argument `Print(...)` calls duplicate `input` declarations stale `identity_generation_pass` values stale interface contract versions stale short report alias references missing public Level modules final runtime partition or counter drift after all reporting layers The EA emits: Optional CSV: Runtime MQL cannot inspect its own source files reliably. Therefore Level 18 also ships a dependency-free Pyth

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 18 — Static QA / Compile Hardening
  - Purpose
  - Runtime modules
  - Source-side tool
  - Execution order
  - Acceptance

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `14`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `13`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `13`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
