# Alpha Lens Mobile — نصب نسخه Studio v6

## اعمال patch

در ریشه پروژه:

```powershell
Expand-Archive -Path .\alpha_lens_mobile_refined_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lens_mobile_refined_patch.zip
```

## اجرا

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

سپس این آدرس را باز کن:

```text
http://localhost:8787/index.html?v=studio6
```

اگر روی موبایل یا PWA هنوز نسخه قبلی را می‌بینی:
- اپ قبلی را از Home Screen حذف کن
- آدرس `index.html?v=studio6` را مستقیم باز کن
- دوباره Add to Home Screen بزن
