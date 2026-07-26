  ---
  id: EXP0018-ROLLBACK-V2
  title: "EXP0018 Rollback and Recovery Plan v2"
  type: release
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

# Rollback و Recovery

- هر Phase patch root-relative و atomic است.
- فایل‌های جدید با exact manifest حذف‌پذیرند.
- schema change migration/rollback دارد.
- chart objects فقط با owned prefix پاک می‌شوند.
- old RC artifact و config preset حفظ می‌شود.
- ledger/research evidence در rollback حذف نمی‌شود؛ version marker می‌گیرد.
