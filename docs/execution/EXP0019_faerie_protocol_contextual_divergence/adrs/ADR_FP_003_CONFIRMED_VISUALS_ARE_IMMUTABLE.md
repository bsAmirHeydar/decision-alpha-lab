---
title: "ADR FP-003 — Visualهای Confirmed Immutable هستند"
tags: [exp0019, adr, architecture]
status: accepted
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# ADR FP-003 — Visualهای Confirmed Immutable هستند

## Decision

پس از confirmation، line حذف یا جابجا نمی‌شود؛ lifecycle بعدی با ledger ثبت می‌شود.

## Context

FP باید از تجربه پروژه‌های واگرایی قبلی استفاده کند بدون اینکه سیاست A/L/N/WW وارد kernel عمومی شود.

## Consequences

این تصمیم درخواست مالک و auditability تاریخی را حفظ می‌کند.

## Rejected alternatives

- copy-paste کامل FP101 به‌عنوان base.
- افزودن switchهای relation داخل CGD/CGH.
- استفاده از drawing object به‌عنوان state.
- حل تصمیم‌ها با default پنهان.

## Verification

- dependency map جهت یک‌طرفه دارد.
- golden tests هسته قبلی بدون تغییر پاس می‌شوند.
- FP tests از adapter public surface استفاده می‌کنند.

## Links

- [[../00_EXP0019_MOC]]
- [[../05_SHARED_CORE_REUSE_MATRIX]]
- [[../27_MQL5_MODULAR_ARCHITECTURE]]
