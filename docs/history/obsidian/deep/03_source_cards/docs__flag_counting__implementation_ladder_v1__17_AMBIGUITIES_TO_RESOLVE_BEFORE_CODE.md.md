
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md"
source_ext: ".md"
source_size: 4341
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md

## Source

[[docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE|docs/flag_counting/implementation_ladder_v1/17_AMBIGUITIES_TO_RESOLVE_BEFORE_CODE.md]]

## Summary

Implemented in Phoenix Level 17. Runtime modules: EA support: The old purpose of this document was to list unresolved questions before code. That is now closed. Level 17 turns those decisions into a runtime decision registry and emits `FP_LEVEL17` after Level 16 acceptance and before `FP_SUMMARY`. The canonical source remains: Level 17 does not replace the canon. It audits whether the active EA inputs and runtime reports are aligned with the canon decisions. Level 17 checks the following decision families: Canon source is `FLAG_COUNTING_CURRENT_CANON.md`. `identity_generation_pass` is `phoenix_level17`. Closed-bar timebase remains default. Confirmed F bodies do not consume live pending nodes by default. F1 remains phase-boundary gated. Fail-open remains diagnostic-only. Pre-internal favorable breaks are absorbed as Leg2 extension, not confirmation. F2 main chart requires size qualificati

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Level 17 — Ambiguity Resolution / Final Decision Lock
  - Status
  - Source of truth
  - Runtime position
  - Level 17 decisions checked
  - EA inputs
  - Optional CSV
  - Non-authority rule
  - Acceptance

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `24`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `18`
- [[docs/flag_counting/implementation_ladder_v1/15_MODULE_INTERFACE_CONTRACTS|15_MODULE_INTERFACE_CONTRACTS.md]] — score `17`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `17`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `17`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `16`
- [[docs/flag_counting/IMPLEMENTATION_LADDER_V1_INDEX|IMPLEMENTATION_LADDER_V1_INDEX.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
