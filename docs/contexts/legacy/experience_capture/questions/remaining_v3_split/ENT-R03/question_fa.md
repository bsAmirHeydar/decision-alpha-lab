# ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

چرا مهم است: چون بعد از ساختن Limit Entry، هنوز معلوم نیست سفارش تا چه زمانی زنده است، چه زمانی باید کنسل شود، چه زمانی missed حساب شود، و چه زمانی با یک Entry-Level Extreme جدید جایگزین شود. این بخش جلوی اجرای کور و سفارش‌های مرده را می‌گیرد.

برای پاسخ، حتماً این موارد را روشن کن:
• وقتی parent zone سالم است ولی قیمت هنوز به limit نرسیده، سفارش تا چه زمانی زنده می‌ماند؟
• اگر سناریو، زون، یا محدودیت اصلی‌ای که سفارش را ساخته invalid شد، آیا pending limit فوراً cancel می‌شود؟
• اگر نود یا death boundary تایم ورود قبل از fill زده شد، سفارش چه وضعیتی می‌گیرد؟
• اگر قیمت بدون fill از زون برگشت و حرکت کرد، این missed است یا باید دنبال replace بگردیم؟
• Missed دقیقاً یعنی چه: حرکت به سمت مقصد بدون fill، خروج از زون، یا بسته‌شدن entry window؟
• Replace دقیقاً چه زمانی مجاز است؟ فقط وقتی Entry-Level Extreme جدید داخل همان زون ساخته شود یا در سناریوی هم‌خانواده هم مجاز است؟
• Entry جدید باید از قبلی بهتر باشد؟ مثلاً stop کوچک‌تر، near-death بهتر، convexity بهتر، یا فقط معتبر بودن کافی است؟
• اگر سفارش قبلی هنوز زنده است و entry extreme جدید ساخته شد، قبلی cancel می‌شود یا هر دو می‌مانند؟
• Pending order باید expiration زمانی داشته باشد یا فقط structural expiration؟
• خروجی نهایی چه stateهایی داشته باشد؟

عکس لازم: اختیاری. اگر نمونه‌ای از limit missed یا replace روی چارت داری، عکس کمک می‌کند.

خروجی مورد انتظار بعد از پاسخ:
• pending_limit_state_machine_v1.csv
• cancel_policy_v1.csv
• missed_entry_policy_v1.csv
• replace_entry_policy_v1.csv
• pending_order_structural_expiration_v1.csv

پاسخ شما:
