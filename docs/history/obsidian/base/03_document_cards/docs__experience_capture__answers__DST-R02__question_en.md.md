---
title: "DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/answers/DST-R02/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1440"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
---


# DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

**Source:** [[docs/experience_capture/answers/DST-R02/question_en|docs/experience_capture/answers/DST-R02/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1440` bytes

## خلاصه

When several destinations or exit opportunities exist, how should take profit, partial close, runner/tail logic, and trailing behavior be handled? NDS does not treat profit-taking as a single fixed TP. The strategy may have multiple destinations, multiple exit conditions, partial exits, and an optional runner/tail component. Because the broader model prioritizes low cost, open profit potential, and convex opportunity, exit logic must be trained and evaluated through the same lens. Please clarify: Should different exit variants be trained and compared? What metrics should decide which exit policy is better? Should the system prioritize potential, open profit path, low cost, or win rate? Is tr

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy
-   Question
-   Why This Question Remains
-   Answer Requirements
-   Expected Output

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R04/question_en|SCN-R04 — Scenario Update, Death, and Repricing]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DATA-R01/question_en|DATA-R01 — Canonical State Packet v1]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v3_split/DST-R01/question_en|DST-R01 — Destination Taxonomy and Open One-Two]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/question_en|BASE-02 — What Exactly Is a Scenario?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-03/question_en|BASE-03 — What Counts as a Valid Reason, and What Is Only Noise?]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
