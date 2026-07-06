---
title: "ENT-R04 — After Fill: Scenario-to-Position Transition"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/ENT-R04/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1764"
concepts:
  - "Execution"
  - "Structural Nodes"
---


# ENT-R04 — After Fill: Scenario-to-Position Transition

**Source:** [[docs/experience_capture/answers/ENT-R04/question_en|docs/experience_capture/answers/ENT-R04/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1764` bytes

## خلاصه

After a Limit Entry is filled, how should the system transition from Scenario / ExecutionIntent into an active Position? Should the scenario remain alive, should it become a PositionThread, how should duplicate entries be prevented, and how should exits or hedges be treated? ENT-R01 defined Entry-Level Extreme as Extreme Near Death. ENT-R02 defined limit entry, stop geometry, spread adjustment, trainable buffer, and max-lot splitting. ENT-R03 defined pending limit lifecycle as reason-integrity based. ENT-R04 defines what happens after fill. Please clarify: After fill, does the ScenarioThread remain alive or become a PositionThread? Should the system prevent duplicate trades with the same rea

## Headings

- ENT-R04 — After Fill: Scenario-to-Position Transition
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-09/question_en|EXT-09 — How Do You Understand the Quality of the Anchor Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R02/question_en|RSK-R02 — Convexity Metrics and Cost-to-Potential Formula]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
