
---
type: source_card
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2.md"
source_ext: ".md"
source_size: 5997
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — PHOENIX_ROOT_CONTRACT_REPAIR_V2.md

## Source

[[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2.md]]

## Summary

This repair brings the Phoenix implementation back to the documented Flag Counting contract after the Hook/ND visual-cycle changes made the main chart gray and starved the colored F1/F2/F3 flag bodies. The guiding rule is simple: > Hook / ND is a phase-boundary and context layer. It must never erase the two-leg flag-body detector. The main chart must show valid F structures first. Hook / ND is drawn as gray context behind those structures, not as a replacement for them. The uploaded project had four coupled problems. `FP_DetectScale()` first collected Hook-derived roots and then built F1 only from those roots unless no Hook-derived root could build a visible F1. That is not safe. A Hook engine under active research can be incomplete or too narrow. If it emits one usable root, the old logic would suppress all raw-origin roots in that direction and scale. The result is exactly wha… The pro

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phoenix Root Contract Repair V2
  - Purpose
  - Root failure found
    - 1. Hook-origin filtering was too strong
    - 2. Same-direction restart pruning was too aggressive for the research chart
    - 3. Hook rendering was not compact enough across scales
    - 4. Hook counted-node labels were mixed with main-chart labels
  - Repair decisions
    - 1. Always keep fail-open F1 visibility when allowed
    - 2. Disable same-direction chain pruning by default
    - 3. Compact Hook arcs at renderer level
    - 4. Hide Hook counted numbers by default

## Related Source Documents

- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|IMPLEMENTATION_NOTES.md]] — score `21`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
