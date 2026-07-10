---
id: EXP0018-P03-AUDIT
title: "P03 Audit Ledger"
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

# Audit Ledger

CSV اختیاری در Common Files نوشته می‌شود. PERIOD row شامل Window، completeness، counts، coverage، OHLC دو نماد و previous links است. Ledger منبع حقیقت بازار نیست؛ evidence از محاسبه deterministic است.

برای جلوگیری از حجم بالا فقط آخرین N period در هر refresh قابل نوشتن است.
