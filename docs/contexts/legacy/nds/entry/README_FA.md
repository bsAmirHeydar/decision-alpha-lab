# معماری لایه ورود NDS

این بسته مسیر زیر را به‌صورت ماژولار آماده می‌کند:

```text
هوک معتبر
→ قرارداد زون
→ کاندید ستاپ
→ پلن معامله
→ پیش‌نمایش دستور معاملاتی
```

نسخه فعلی عمداً هیچ سفارشی ارسال نمی‌کند. حجم همیشه صفر و `send_allowed` همیشه false است. پروفایل پیش‌فرض نیز تا زمان قفل شدن Canon زون و ورود، در وضعیت `PRE_CANON_BLOCKED` باقی می‌ماند.

فایل اصلی مطالعه:

```text
docs/contexts/legacy/nds/entry/README.md
```

خروجی‌های زمان اجرا:

```text
nds_entry_structure_snapshot.csv
nds_entry_setup_candidate.csv
nds_entry_trade_plan.csv
nds_entry_command_preview.csv
nds_entry_pipeline_summary.csv
```

برای تست صرفاً تشخیصی می‌توان پروفایل manual geometry را فعال کرد؛ اما این حالت صریحاً غیر Canonical است و هیچ مجوز معامله‌ای ایجاد نمی‌کند.
