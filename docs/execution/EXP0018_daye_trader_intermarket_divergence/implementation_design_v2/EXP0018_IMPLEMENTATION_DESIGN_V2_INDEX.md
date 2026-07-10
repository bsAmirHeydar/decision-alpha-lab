---
id: EXP0018-DESIGN-V2-INDEX
title: "EXP0018 Implementation Design v2 — Index"
type: moc
status: active
project: EXP0018
version: 2.2.0
created: 2026-07-10
updated: 2026-07-10
---
# EXP0018 Implementation Design v2

این شاخه نقشه مهندسی کامل برای تبدیل دکترین Daye/Quarterly Theory به سیستم deterministic، replayable، visual-only و بدون اختیار معامله است.

## نقطه شروع

1. [[EXP0018_DESIGN_OPERATING_CONTRACT|قرارداد کار طراحی]]
2. [[EXP0018_MASTER_IMPLEMENTATION_BLUEPRINT|نقشه مادر پیاده‌سازی]]
3. [[EXP0018_OPEN_DECISION_REGISTER|تصمیم‌های باز و blockerها]]
4. [[EXP0018_FIRST_DESIGN_SPRINT|اولین Sprint طراحی]]
5. [[CG_EXP0018_IMPLEMENTATION_DESIGN_V2_MOC|MOC اصلی Obsidian]]

## Implementation evidence packages

- [[EXP0018-P00-V2-INDEX|P00 Doctrine Freeze v2]]
- [[EXP0018-P01-V2-INDEX|P01 New York Time Kernel v2]]
- [[EXP0018-P02-V2-INDEX|P02 Multi-Symbol Data Synchronization v2]]

## وضعیت فعلی

- P00 package کامل است ولی ADR approvalهای نهایی هنوز باید ثبت شوند.
- P01 پیاده‌سازی شده و منتظر Compile/Runtime evidence نهایی است.
- P02 پیاده‌سازی exact-timestamp و no-forward-fill دارد و منتظر MetaEditor/runtime validation است.
- P03 مرحله بعدی رسمی است.
- هیچ فاز فعلی order placement، risk sizing یا execution authority ندارد.
