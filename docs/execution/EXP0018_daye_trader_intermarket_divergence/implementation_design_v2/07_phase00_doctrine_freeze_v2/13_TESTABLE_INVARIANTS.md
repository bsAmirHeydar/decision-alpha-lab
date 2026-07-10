---
id: EXP0018-P00-INVARIANTS
title: "EXP0018 Phase 00 — Testable Invariants"
type: standard
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
# Invariantهای قابل تست

## INV-001

تمام زمان‌های domain نیویورک هستند.

## INV-002

Trading Day از 18:00 تا 16:59:59 است.

## INV-003

17:00–17:59:59 عضو هیچ session نیست.

## INV-004

p4 فقط 30 دقیقه است.

## INV-005

هر نماد فقط با سطح خودش مقایسه می‌شود.

## INV-006

Equality در Hunt حساب می‌شود.

## INV-007

Hunt به close پشت سطح نیاز ندارد.

## INV-008

No Data با Not Hunted متفاوت است.

## INV-009

تأیید فقط روی closed host bar انجام می‌شود.

## INV-010

Double Hunt در Close خط تأیید تولید نمی‌کند.

## INV-011

Relationshipها مستقل ارزیابی می‌شوند.

## INV-012

Renderer truth تولید نمی‌کند.

## INV-013

خط فقط روی Hunter chart و با قیمت همان نماد است.

## INV-014

Minor signal متن ندارد.

## INV-015

Object ID deterministic است.

## INV-016

Retired reference دوباره فعال نمی‌شود.

## INV-017

Replay از همان core engine لایو استفاده می‌کند.

## INV-018

EXP0018 هیچ Order API ندارد.

## INV-019

Optional module اجازه تغییر silent Core ندارد.

## INV-020

PDF claim بدون promotion وارد rule نمی‌شود.

## INV-021

هر event دارای event_time و availability_time است.

## INV-022

هر mutable state یک owner دارد.

## INV-023

Duplicate event transition دوم ندارد.

## INV-024

Confirmed historical event با داده آینده repaint نمی‌شود.
