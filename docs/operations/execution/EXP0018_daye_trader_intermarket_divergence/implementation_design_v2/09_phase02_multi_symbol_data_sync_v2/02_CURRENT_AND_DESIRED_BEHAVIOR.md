---
id: EXP0018-P02-CURRENT-DESIRED
title: "P02 Current and Desired Behavior"
type: design
status: active
project: EXP0018
---
# رفتار فعلی و مطلوب

## قبل از P02

P01 زمان را حل کرده بود، اما downstream هنوز contract مستقلی برای دو symbol نداشت. خطرهای اصلی عبارت بودند از alignment بر index، history ناقص، suffix متفاوت و برداشت غلط از نبود داده.

## بعد از P02

هر مصرف‌کننده فقط `DAYE_SynchronizedBarPair` می‌گیرد. هر pair دو bar با `event_time_utc` دقیقاً یکسان دارد. timestampهای unmatched حذف نمی‌شوند؛ در summary شمارش و گزارش می‌شوند. هیچ قیمت جایگزین ساخته نمی‌شود.

## نتیجه قابل مشاهده

Expert مستقل P02 در Experts tab وضعیت هر symbol، تعداد copied/accepted/aligned و latest common bar را نشان می‌دهد. Audit CSV اختیاری است.
