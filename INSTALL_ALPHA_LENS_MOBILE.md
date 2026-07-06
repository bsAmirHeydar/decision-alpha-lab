# NDS Lens Mobile — نصب نسخه Studio v11

## اعمال patch

در ریشه پروژه:

```powershell
Expand-Archive -Path .\nds_lens_mobile_v12_patch.zip -DestinationPath . -Force
Remove-Item .\nds_lens_mobile_v12_patch.zip
```

## اجرا

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

سپس این آدرس را باز کن:

```text
http://localhost:8787/index.html?v=studio12
```

## تغییرات مهم v10

- فیلد `زمان ثبت` اضافه شد و همیشه لحظه فعلی دستگاه را نشان می‌دهد.
- هنگام اسنپ یا خروجی گرفتن، زمان فعلی در داده ذخیره می‌شود.
- ورق‌زدن تایم‌فریم‌ها بازنویسی شد و دیگر وابسته به scrollLeft در RTL نیست.
- تب‌های تایم‌فریم و swipe افقی هر دو کار می‌کنند.
- لیبل‌های قابل مشاهده UI فارسی‌تر و یکدست‌تر شدند.

## اگر هنوز نسخه قبلی را می‌بینی

- اپ قبلی را از Home Screen حذف کن
- همین آدرس `index.html?v=studio12` را مستقیم باز کن
- دوباره Add to Home Screen بزن


## داکیومنت فونت

```text
tools/alpha_lens_mobile/docs/FONT_POLICY_V11.md
```


## تغییرات v12

- نام اپ از Alpha Lens به NDS Lens تغییر کرد.
- زیرعنوان نسخه/فونت زیر نام اپ حذف شد.
- تب‌های تایم‌فریم کامل شدند: ۱ ساعته، ۱۰ دقیقه، ۱ دقیقه.
- جمله راهنمای «تایم‌فریم را ورق بزن» حذف شد.
- پرش عمودی صفحه هنگام انتخاب وضعیت/ریسک/ریوارد/جهت سلول اصلاح شد.
