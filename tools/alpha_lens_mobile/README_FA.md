# Alpha Lens Minimal — اپ آفلاین موبایل

این نسخه مینیمال و فشرده‌ی ماتریس نگاه بازار است.

## تغییرات نسخه مینیمال

- ماتریس واقعی ۴×۳ به جای کارت‌های بزرگ پشت سر هم
- هر سلول فقط score، risk، reward و action را فشرده نشان می‌دهد
- با لمس هر سلول، پنل ویرایش کوچک پایین ماتریس باز می‌شود
- رنگ‌های خنثی و مینیمال: کرم، مشکی نرم، سبز خاکی، قرمز خاکی
- دکمه‌های اصلی در نوار پایین موبایل
- Snapshot، Export و Import حفظ شده‌اند
- داده‌ها همچنان آفلاین و داخل خود مرورگر ذخیره می‌شوند

## اجرا

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

بعد روی موبایل در همان Wi-Fi باز کن:

```text
http://YOUR-PC-IP:8787
```

## نصب مثل اپ

- Android/Chrome: منوی سه‌نقطه → Add to Home screen یا Install app
- iPhone/Safari: Share → Add to Home Screen
