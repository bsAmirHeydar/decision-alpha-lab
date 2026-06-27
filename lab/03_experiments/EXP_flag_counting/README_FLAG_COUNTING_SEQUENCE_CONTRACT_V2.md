# EXP flag_counting — Sequence Contract V2

این فولدر باید از این به بعد منطق اف‌شماری را بر اساس سند زیر جلو ببرد:

```text
docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md
```

چک‌لیست اجرایی:

```text
docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md
```

اصل‌های قفل‌شده:

- منطق فقط High/Low node است.
- Fها زنجیره‌ای هستند: F1 -> F2 -> F3.
- F1 بعد از ND یا انتهای F مخالف شروع می‌شود.
- F2 فقط بعد از F1 confirmed ساخته می‌شود.
- F3 بعد از F2 ساخته می‌شود و با body دو لگه قفل می‌شود.
- همه‌ی raw high/lowها نگه داشته می‌شوند، اما در شمارش با scale بزرگ‌تر فشرده می‌شوند.
- بیشتر از 4 node در یک واحد شمارشی مجاز نیست؛ L بالا می‌رود تا <=4 شود.
- 3/4 node cycle می‌تواند ND/Hook باشد.
- rejectedها روی چارت اصلی نمایش داده نمی‌شوند.
- candidateها دیده می‌شوند، اما با status/color متفاوت.
