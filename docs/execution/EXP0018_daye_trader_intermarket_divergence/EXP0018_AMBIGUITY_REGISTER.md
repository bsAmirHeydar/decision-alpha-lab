# ثبت ابهام‌های EXP0018

| ID | موضوع | متن/تعارض | اثر | وضعیت |
|---|---|---|---|---|
| DY-A01 | جهت high/low | یک جمله low را برای SELL می‌گوید؛ مثال LN، high را برای SELL می‌گوید | critical | باز |
| DY-A02 | NP | «P قبلی با N قبلی» نوشته شده؛ current/reference روشن نیست | critical | باز |
| DY-A03 | signal alias order | DOCX aliasها مثل p4a1 است، ولی نسخه‌های خوانش RTL ممکن است 1a4p دیده شوند | medium | canonical ID پیشنهاد شد |
| DY-A04 | تعداد signal inputs | یک‌جا 22، انتها 21 | medium | باز؛ فهرست واقعی 22 است |
| DY-A05 | p4 duration | p4 فقط 30 دقیقه است ولی در گروه 90m آمده | medium | باز |
| DY-A06 | first sweep vs repeat | فقط دفعه اول مهم است، اما protected-survival تکرار را ممکن می‌داند | critical | باز |
| DY-A07 | session DST hours | جدول اصلی 18/0/6/12/17 است؛ متن DST از 20/4/9/16 نام می‌برد | critical | باز |
| DY-A08 | weekly boundary | شروع/پایان دقیق W در نیویورک تعریف نشده | critical | باز |
| DY-A09 | PA day relation | A فعلی با P قبلی؛ باید مشخص شود P روز معاملاتی قبلی است | high | باز |
| DY-A10 | AL/LN continuity | «قبلی» به دوره بلافاصله قبل در همان trading day اشاره دارد؟ | high | باز |
| DY-A11 | line width | فقط color input صریح است | low | باز |
| DY-A12 | box opacity | fill گفته شده، opacity مشخص نیست | low | باز |
| DY-A13 | anchor without exact bar | TWO/TDO در نبود bar دقیق چه کنند؟ | high | باز |
| DY-A14 | incomplete box | سشن ناقص رسم شود یا نه؟ | medium | باز |
| DY-A15 | broader cycles | 22.5m/M1/4Q/y/4y بدون تعریف اجرایی‌اند | high | خارج scope فعلی |
| DY-A16 | drawing label mechanism | متن «وسط trend» می‌خواهد؛ OBJ_TREND خود label داخلی ندارد | medium | نیازمند object pair یا tooltip |
| DY-A17 | line after later invalidation | منبع می‌گوید خط حذف نشود؛ باید immutable بودن قطعی تأیید شود | high | تقریباً روشن |
| DY-A18 | simultaneous opposite signals | منبع می‌گوید همه BUY/SELLها رسم شوند؛ overlap policy مشخص نیست | low | رفتار: همه رسم شوند |

## قانون

تا حل DY-A01، DY-A02، DY-A06، DY-A07 و DY-A08، شروع کدنویسی هسته signal ممنوع است.
