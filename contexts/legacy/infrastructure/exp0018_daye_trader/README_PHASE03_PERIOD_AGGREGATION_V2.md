---
id: EXP0018-P03-INFRA-README
title: "EXP0018 Phase 03 Infrastructure"
type: spec
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - phase03
  - period-aggregation
---

# Phase 03 Infrastructure

این شاخه قرارداد ماشینی، fixture، validator، test و runner فاز تجمیع دوره‌ها را نگه می‌دارد.

## اجرا

```powershell
.\contexts\legacy\infrastructure\exp0018_daye_trader\powershell\run_exp0018_phase03_period_aggregation_v2_checks.ps1 -RepoRoot "."
```

## Gate

- fixtureهای `COMPLETE/PARTIAL/OPEN/EMPTY` پاس شوند.
- p4 دقیقاً ۳۰ دقیقه بماند.
- Daily در روز عادی، Spring DST و Fall DST تعداد متفاوت اما صریح داشته باشد.
- Weekly تا ADR-DY-A03 غیرفعال بماند.
- execution authority برابر false باشد.
