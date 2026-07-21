---
title: "NDS-R03 — Node Identity, Node Cluster, and Node Replacement"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/NDS-R03/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1153"
concepts:
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
---


# NDS-R03 — Node Identity, Node Cluster, and Node Replacement

**Source:** [[docs/experience_capture/answers/NDS-R03/question_en|docs/experience_capture/answers/NDS-R03/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1153` bytes

## خلاصه

Define node identity, node roles, node clustering, and node replacement in NDS. Nodes can start CycleHooks, act as Extreme anchors, appear inside sequences, appear in different Hook/Rally contexts, and change practical validity depending on role. The system needs a stable node identity model. Please clarify: When does a node remain the same node? When does a node become consumed, invalidated, replaced, merged, or archived? If several nodes are near each other, are they separate nodes or a cluster? Does changing L create a new node identity or a different view of the same market area? How do node roles differ: origin, anchor, destination, internal, Extreme anchor, sequence node? If one node a

## Headings

- NDS-R03 — Node Identity, Node Cluster, and Node Replacement
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/experience_capture/answers/EXT-02/question_en|EXT-02 — Which Project Logic Produces the Anchor Node for Extreme?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/DST-R03/question_en|DST-R03 — Destination Repricing and Completion]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-04/question_en|EXT-04 — Is L2 Always the Default, or Only in Specific Contexts?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R02/question_en|NDS-R02 — Cycle Lifecycle: Birth, Life, Near-Death, Death, and New Cycle]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R02/question_en|DATA-R02 — Label and Event Ledger]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
