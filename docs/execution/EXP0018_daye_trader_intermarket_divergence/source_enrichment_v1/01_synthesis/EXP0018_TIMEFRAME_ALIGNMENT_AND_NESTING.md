# هم‌ترازی تایم‌فریم و Nesting

منابع می‌گویند context تایم بالا باید در تایم پایین «ارتباط» پیدا کند. الگوی رایج:

```text
HTF imbalance / liquidity / True Open
  -> LTF SMT or SSMT
  -> LTF PD array / CSD / breaker
  -> execution candidate
```

Golden Pocket نمونه nesting چند Q3 است: Q3 هفتگی (چهارشنبه)، Q3 روزانه (NY AM) و Q3 سشن (۹:۰۰ تا ۱۰:۳۰). ادعای احتمال بالا باید به‌عنوان hypothesis ثبت و با timezone و news regime تست شود.

برای EXP0018، timeframe میزبان فقط confirmation boundary است. هر alignment اضافی باید optional metadata باشد، نه شرط پنهان.
