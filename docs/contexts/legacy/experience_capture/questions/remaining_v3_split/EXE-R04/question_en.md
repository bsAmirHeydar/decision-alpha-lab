# EXE-R04 — Execution Audit and Reconciliation

## Purpose
چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست.

## Required Clarifications
- Intent price و submitted price چطور مقایسه می‌شوند؟
- Submitted price و filled price چطور مقایسه می‌شوند؟
- Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟
- Slippage چطور ثبت شود؟
- Partial fills چطور ثبت شوند؟
- Rejected orders چطور ثبت شوند؟
- Canceled orders چطور ثبت شوند؟
- Split order aggregation چطور باشد؟
- Broker-side modification چطور audit شود؟
- Reconciliation با scenario/zone/entry ID چطور انجام شود؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `execution_audit_ledger_v1.csv`
- `intent_to_order_reconciliation_v1.csv`
- `fill_quality_model_v1.csv`
- `split_order_audit_v1.csv`
