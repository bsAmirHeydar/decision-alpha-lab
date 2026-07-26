
---
type: source_card
source_path: "docs/experience_capture/answers/EXE-R02/answer_normalized_en.md"
source_ext: ".md"
source_size: 4123
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Market Anatomy", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — answer_normalized_en.md

## Source

[[docs/experience_capture/answers/EXE-R02/answer_normalized_en|docs/experience_capture/answers/EXE-R02/answer_normalized_en.md]]

## Summary

Broker validation and send-gate rules are mechanical. They are not part of the native NDS decision ontology. Their rules are clear and deterministic. Recommended canonical rule: The broker validator should not reinterpret the market, rank scenarios, select zones, or change NDS structural reasoning. It should only check whether an already-created ExecutionIntent is mechanically valid for broker submission. NDS responsibility: Broker Validator responsibility: The validator is not an AI policy layer. It is not a scenario layer. It is not a zone layer. It is not an entry-selection layer. It is a mechanical send gate. The broker validator should handle deterministic broker-side constraints such as: These are not discretionary. They should be implemented as explicit checks. Some constraints may allow mechanical adjustment. Examples: Other constraints should veto. Examples: The exact adjust/vet

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- EXE-R02 — Normalized Interpretation
  - Core Claim
  - Separation of Responsibilities
  - Deterministic Constraint Layer
  - Mechanical Adjust vs Veto
  - No NDS Reasoning Mutation
  - Audit Requirement
  - Send Gate
  - Machine-Readable Summary
  - Short Formal Statement

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `12`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-02/answer_raw_en|answer_raw_en.md]] — score `12`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/EXE-R01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `12`
- [[docs/experience_capture/answers/NDS-R01/question_en|question_en.md]] — score `12`
- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R02|EXE-R02.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
