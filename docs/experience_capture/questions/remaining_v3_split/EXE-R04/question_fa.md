# EXE-R04 — Execution Audit and Reconciliation

چرا مهم است: چون باید بفهمیم سیستم چه قصدی داشته، چه چیزی به broker فرستاده شده، چه چیزی fill شده و اختلاف‌ها از کجا آمده‌اند. بدون reconciliation، backtest/paper/live قابل اعتماد نیست.

برای پاسخ، حتماً این موارد را روشن کن:
• Intent price و submitted price چطور مقایسه می‌شوند؟
• Submitted price و filled price چطور مقایسه می‌شوند؟
• Structural SL/TP و adjusted SL/TP جدا ذخیره شوند؟
• Slippage چطور ثبت شود؟
• Partial fills چطور ثبت شوند؟
• Rejected orders چطور ثبت شوند؟
• Canceled orders چطور ثبت شوند؟
• Split order aggregation چطور باشد؟
• Broker-side modification چطور audit شود؟
• Reconciliation با scenario/zone/entry ID چطور انجام شود؟

عکس لازم: خیر. پاسخ متنی کافی است.

خروجی مورد انتظار بعد از پاسخ:
• execution_audit_ledger_v1.csv
• intent_to_order_reconciliation_v1.csv
• fill_quality_model_v1.csv
• split_order_audit_v1.csv

پاسخ شما:
