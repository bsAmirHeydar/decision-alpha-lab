# Context اجرایی بدون Authority معامله

PDFها workflowهای ورود را شرح می‌دهند: HTF level، SMT، LTF confirmation، FVG/BPR/breaker، stop پشت Q2 و target در liquidity. این مطالب برای ساخت research dataset مفیدند، اما پروژه EXP0018 فعلی drawing-only است.

قاعده:

- `signal detection` با `entry model` یکی نیست.
- یک line تأییدشده مجوز order نیست.
- stop/target پیشنهادی PDFها تا قرارداد ریسک و تست مستقل فقط metadata هستند.
- اگر بعدها execution ساخته شود، raw detector و filtered executor باید دو محصول جدا بمانند.
