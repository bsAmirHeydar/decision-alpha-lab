# INSTALL — EXP0017 Chapter 10 Risk, Invalidation and Time Exit Patch

این پچ فصل ۱۰ پاسخ‌های معمار استراتژی را برای پروژه‌ی `EXP0017_cycle_group_intermarket_divergence` اضافه می‌کند.

## محتوای پچ

این پچ فقط شامل داکیومنت و آبسیدین است و هیچ فایل کدنویسی یا اکسپرت را تغییر نمی‌دهد.

موضوع فصل ۱۰:

- مرز ابطال معامله بعد از ورود
- لمس دوباره‌ی مرجع در نماد تمیز
- استاپ مطلق روی مرجع
- ریسک ثابت
- عدم تغییر ریسک بر اساس کیفیت واگرایی در مدل پایه
- خروج زمانی در انتهای همان سایکل
- ماندن تا انتهای سایکل حتی اگر سود بزرگ قبل از پایان سایکل ایجاد شود
- سنجش برآیند سیگنال با سود/زیان دلاری
- امکان ترکیب خروج زمانی با تارگت‌های قیمتی در آینده
- ثبت ابهام سؤال اول به‌عنوان موضوع نیازمند بازنویسی مفهومی

## نصب در PowerShell

```powershell
Expand-Archive -Force ".\\decision-alpha-lab-exp0017-chapter10-risk-time-exit-expanded-obsidian-patch.zip" ".\\"
Remove-Item ".\\decision-alpha-lab-exp0017-chapter10-risk-time-exit-expanded-obsidian-patch.zip"
```
