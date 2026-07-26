---
id: EXP0018-P00-INDEX-V2
title: "EXP0018 Phase 00 — Doctrine Freeze v2 Index"
type: index
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# Phase 00 — انجماد دکترین نسخه ۲

## هدف

این فاز پیش از هر Signal Engine، تمام تعاریف هسته Daye را به قواعد صریح، قابل تست و قابل ارجاع تبدیل می‌کند. خروجی Phase 00 «کد سیگنال» نیست؛ خروجی آن **حقیقت دامنه‌ای نسخه‌دار** است که فازهای بعدی اجازه دارند اجرا کنند.

## وضعیت فعلی

```text
Non-conflicting core rules: documented and provisionally frozen
Conflicting rules: converted to ADR decisions
Architect approval: pending
Signal implementation: blocked until critical ADRs close
```

## ترتیب مطالعه

1. [[01_MASTER_BASELINE]]
2. [[02_AUTHORITY_AND_INTERPRETATION]]
3. [[03_CORE_SCOPE_AND_NON_GOALS]]
4. [[04_CANONICAL_GLOSSARY]]
5. [[05_TIME_AND_PERIOD_DOCTRINE]]
6. [[06_RELATIONSHIP_DOCTRINE]]
7. [[07_HUNT_AND_DIVERGENCE_DOCTRINE]]
8. [[08_CLOSE_CONFIRMATION_DOCTRINE]]
9. [[09_REFERENCE_LIFECYCLE_DOCTRINE]]
10. [[10_DRAWING_AND_PERSISTENCE_DOCTRINE]]
11. [[11_DATA_AND_PARTIAL_HISTORY_DOCTRINE]]
12. [[12_IDENTITY_AND_DEDUPLICATION]]
13. [[13_TESTABLE_INVARIANTS]]
14. [[14_POSITIVE_NEGATIVE_SCENARIOS]]
15. [[15_ARCHITECT_DECISION_WORKBOOK]]
16. [[16_RECOMMENDED_BASELINE]]
17. [[17_SOURCE_EVIDENCE_MATRIX]]
18. [[18_CONFLICT_RESOLUTION_PROTOCOL]]
19. [[19_FIXTURE_CATALOG]]
20. [[20_DOCTRINE_FREEZE_GATE]]
21. [[21_HANDOFF_TO_IMPLEMENTATION]]

## ADRهای تصمیم

- [[adr/ADR-DY-A01-BUY-SELL-MAPPING]]
- [[adr/ADR-DY-A02-TWO-ANCHOR]]
- [[adr/ADR-DY-A03-WEEKLY-BOUNDARY]]
- [[adr/ADR-DY-A04-FIRST-SWEEP-SCOPE]]
- [[adr/ADR-DY-A05-NP-RELATIONSHIP]]
- [[adr/ADR-DY-A06-WICK-VS-BODY]]
- [[adr/ADR-DY-A07-CORE-VS-SSMT]]
- [[adr/ADR-DY-A08-EXTENDED-TRUE-OPENS]]
- [[adr/ADR-DY-A09-DFR-PLACEMENT]]
- [[adr/ADR-DY-A10-TRIAD-AUTHORITY]]
- [[adr/ADR-DY-A11-NEWS-AUTHORITY]]
- [[adr/ADR-DY-A12-HISTORICAL-LINE-PERSISTENCE]]

## خروجی ماشینی

- `data/EXP0018_PHASE00_DECISION_LEDGER_V2.csv`
- `data/EXP0018_PHASE00_RULE_REGISTRY_V2.csv`
- `data/EXP0018_PHASE00_INVARIANT_REGISTRY_V2.csv`
- `data/EXP0018_PHASE00_FIXTURE_REGISTRY_V2.csv`
- `data/EXP0018_PHASE00_RELATIONSHIP_SNAPSHOT_V2.csv`
- `data/EXP0018_PHASE00_GLOSSARY_V2.csv`
- `data/EXP0018_PHASE00_TRACEABILITY_V2.csv`
- `data/EXP0018_PHASE00_DOCTRINE_SNAPSHOT_V2.json`

## مرز قطعی

Phase 00 هیچ Order API، ریسک، تارگت، معامله، مدل آماری یا dependency از EXP0017 اضافه نمی‌کند.
