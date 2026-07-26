  ---
  id: EXP0018-DESIGN-CHANGE-CONTROL
  title: "EXP0018 Design Change Control"
  type: governance
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

# کنترل تغییر طراحی

هر تغییر بعد از freeze باید یکی از این سه نوع باشد:

1. **Clarification:** معنی قبلی را بدون تغییر رفتار دقیق‌تر می‌کند.
2. **Correction:** رفتار مصوب قبلی اشتباه بوده؛ نیازمند ADR و migration است.
3. **Enrichment:** قابلیت اختیاری جدید؛ حق تغییر Core ندارد.

## اطلاعات اجباری Change Request

- change_id
- source and authority
- current behavior / desired behavior
- affected phases/modules/schemas
- preserved invariants
- migration and rollback
- new/updated fixtures
- architect approval

تغییر مستقیم کد بدون به‌روزرسانی rule، ADR و test ممنوع است.
