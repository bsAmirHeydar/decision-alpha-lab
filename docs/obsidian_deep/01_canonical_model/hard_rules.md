
---
type: hard_rules
---

# Hard Rules — قوانین سخت پروژه

## HR-01 — منبع ادله باید از آناتومی پروژه باشد

تصمیم‌ها باید از مفاهیم داخلی پروژه بیایند: [[docs/obsidian_deep/02_concepts/Hook|Hook]]، [[docs/obsidian_deep/02_concepts/Rally|Rally]]، [[docs/obsidian_deep/02_concepts/Flag_Counting|F-counting]]، [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]، [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone/RTV]].

## HR-02 — هیچ ایده‌ای بدون failure condition وارد آزمایش نمی‌شود

هر hypothesis باید روشن کند تحت چه شرایطی رد می‌شود.

## HR-03 — اجرای live زیر اختیار ایجنت نیست

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent]] می‌تواند پیشنهاد، audit، پچ و گزارش بسازد؛ ولی order، lot، risk و live execution باید توسط rule engine و انسان/موتور deterministic کنترل شود.

## HR-04 — هر پچ باید rollbackپذیر باشد

هر تغییر باید به صورت patch محدود، commit message واضح، diff summary و test checklist ارائه شود.

## HR-05 — نتیجه مثبت بدون baseline معتبر نیست

هر نتیجه باید در برابر benchmark ساده، هزینه معامله، slippage، regime split و sample dependence بررسی شود.

## HR-06 — فرکتال بودن باید متریک داشته باشد

عبارت «بازار فرکتال است» کافی نیست. باید بگویی دقیقاً کدام خاصیت در کدام scale تکرار می‌شود.

## HR-07 — تمام اسناد باید به گراف دانش وصل باشند

README، report، plan، patch note و registry باید در Obsidian card و relation map قابل ردیابی باشد.
