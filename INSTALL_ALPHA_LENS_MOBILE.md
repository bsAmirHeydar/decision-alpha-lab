# نصب Alpha Lens Minimal Mobile Patch

این patch نسخه قبلی `tools/alpha_lens_mobile` را با یک UI خیلی مینیمال‌تر جایگزین می‌کند.

## نصب داخل پروژه

```powershell
Expand-Archive -Path .\alpha_lens_mobile_minimal_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lens_mobile_minimal_patch.zip
```

## اجرا

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

بعد در مرورگر:

```text
http://localhost:8787
```

برای موبایل، IP کامپیوتر را با `ipconfig` پیدا کن و در موبایل باز کن:

```text
http://YOUR-PC-IP:8787
```

## نصب روی موبایل

### Android / Chrome

سه‌نقطه → Add to Home screen / Install app

### iPhone / Safari

Share → Add to Home Screen
