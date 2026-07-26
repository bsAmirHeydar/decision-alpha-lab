  ---
  id: EXP0018-REFERENCE-LIFECYCLE-CONTRACT-V2
  title: "قرارداد چرخه عمر مرجع v2"
  type: contract
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---
# قرارداد چرخه عمر مرجع v2

Stateها: `CANDIDATE`, `ACTIVE`, `PROTECTED`, `CONSUMED`, `RETIRED`, `INVALIDATED`.

- مصرف و retirement irreversible است.
- eligibility تابع policy composite key مصوب است.
- lifecycle state از chart object بازسازی نمی‌شود.
