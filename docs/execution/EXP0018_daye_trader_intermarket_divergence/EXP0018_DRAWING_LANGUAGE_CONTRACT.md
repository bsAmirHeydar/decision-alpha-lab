# قرارداد زبان رسم Daye

## اصل

Drawing واگرایی فقط یک trend line ساده است.

## محل رسم

طبق منبع، خط فقط روی چارت نماد Hunter رسم می‌شود.

## نقاط خط

### High-side

- Origin: high دوره reference
- Destination: high اولین کندل confirmation

### Low-side

- Origin: low دوره reference
- Destination: low اولین کندل confirmation

## متن خط

- برای WW/DD/PA/AL/LN/NP: نام signal در وسط خط
- برای 16 زیرسایکل: بدون متن

## style

- رنگ trend input است.
- ضخامت trend در متن صریح input نشده، اما برای implementation حرفه‌ای باید یا ثابت مشخص یا input جدا داشته باشد؛ این مورد هنوز نیازمند تصمیم است.
- ray راست/چپ باید خاموش باشد.
- line باید بین دو نقطه محدود بماند.

## ماندگاری

confirmed line حذف یا جابه‌جا نمی‌شود.

## نام object پیشنهادی

`EXP0018_DAYE_<signal_id>_<side>_<hunter>_<reference_start>_<confirm_close>`
