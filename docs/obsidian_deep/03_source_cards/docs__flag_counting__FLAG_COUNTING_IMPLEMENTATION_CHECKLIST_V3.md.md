
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md"
source_ext: ".md"
source_size: 8148
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Flag Counting", "Hook", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md

## Source

[[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This checklist is for implementing or auditing the Flag Counting V3 contract. Each item should be reviewed before touching detector code. [ ] Detector reads swing high / swing low nodes. [ ] F logic does not use candle open. [ ] F logic does not use candle close. [ ] F logic does not use candle body. [ ] F logic does not use candle color. [ ] ND logic does not use candle open. [ ] ND logic does not use candle close. [ ] ND logic does not use candle body. [ ] ND logic does not use candle color. [ ] Documentation says close is irrelevant, not forbidden. [ ] All raw high/low nodes are stored. [ ] Compression does not delete raw nodes.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Implementation Checklist V3
  - 1. High/Low Only
  - 2. Raw Node Preservation
  - 3. Flag Body Builder
  - 4. F1
  - 5. F2
  - 6. F3
  - 7. ND / Hook
  - 8. Rendering
  - 9. Duplicate Handling
  - 10. Audit Logging
  - 11. Anti-Regression Tests

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]] — score `15`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]] — score `15`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
