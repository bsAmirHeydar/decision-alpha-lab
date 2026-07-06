
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_GLOSSARY.md"
source_ext: ".md"
source_size: 2706
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_GLOSSARY.md

## Source

[[docs/flag_counting/FLAG_COUNTING_GLOSSARY|docs/flag_counting/FLAG_COUNTING_GLOSSARY.md]]

## Summary

A structural market movement grammar that counts movement as F1 -> F2 -> F3 sequences, with ND/Hook phases between or around them. The root flag in a sequence. It must form Origin -> Leg1 -> Waist -> Leg2, then Internal 1/2, then rebreak Leg2 before Waist invalidation. Mandatory continuation after a valid F1. Its Origin is the parent F1 Internal 2. It invalidates at its own Origin, not its Waist. Its size must be at least the parent F1 size. Mandatory continuation after F2. Its Origin is parent F2 Internal 2. After its two-leg body is formed, the sequence becomes terminal/locked and the following movement is special. The starting point of a flag body. For F1 it must be a legitimate root after ND/opposite completion/reset. For F2/F3 it is Internal 2 of the parent. The first impulse away from Origin in the direction of the sequence. The correction after Leg1 and before Leg2. For F1, Waist

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Glossary
  - F-counting
  - F1
  - F2
  - F3
  - Origin
  - Leg1
  - Waist
  - Leg2
  - Internal 1
  - Internal 2
  - Rebreak

## Related Source Documents

- [[docs/glossary|glossary.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `13`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
