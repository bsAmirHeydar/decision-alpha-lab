# نصب Alpha Lens Ultra Minimal

## اعمال patch

```powershell
Expand-Archive -Path .\alpha_lens_mobile_ultra_minimal_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lens_mobile_ultra_minimal_patch.zip
```

## اجرا

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

روی کامپیوتر:

```text
http://localhost:8787/index.html?v=ultra4
```

روی موبایل:

```text
http://YOUR-PC-IP:8787/index.html?v=ultra4
```

## اگر چیزی تغییر نکرد

نسخه قبلی توسط Service Worker یا PWA cache شده است. این کارها را انجام بده:

1. اپ قبلی Alpha Lens را از Home Screen حذف کن.
2. در Chrome/Safari همان آدرس `index.html?v=ultra4` را باز کن.
3. صفحه باید بالای خودش بنویسد: `Ultra minimal · v4`.
4. دوباره Add to Home Screen بزن.
