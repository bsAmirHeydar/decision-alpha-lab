# نصب Alpha Lens Mobile در پروژه

این patch یک اپ آفلاین PWA به مسیر زیر اضافه می‌کند:

```text
tools/alpha_lens_mobile/
```

## نصب patch

در PowerShell داخل ریشه پروژه:

```powershell
Expand-Archive -Path .\alpha_lens_mobile_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lens_mobile_patch.zip
```

## اجرا روی کامپیوتر

```powershell
cd .\tools\alpha_lens_mobile
python -m http.server 8787
```

بعد باز کن:

```text
http://localhost:8787
```

## اجرا روی موبایل

موبایل و کامپیوتر باید روی یک Wi-Fi باشند. IP کامپیوتر را پیدا کن:

```powershell
ipconfig
```

بعد در مرورگر موبایل باز کن:

```text
http://YOUR-PC-IP:8787
```

بعد از Chrome/Safari گزینه Add to Home Screen را بزن.

## کامیت پیشنهادی

```powershell
git add tools/alpha_lens_mobile INSTALL_ALPHA_LENS_MOBILE.md

git commit -m "tools(mobile): add offline Alpha Lens matrix PWA" -m "Add an offline mobile-first PWA for the Alpha Lens Matrix.

Includes:
- four-perspective market lens grid: bullish hook, bullish rally, bearish hook, bearish rally
- three timeframe columns: 1H, 10M, 1M
- per-cell risk, reward, action, score, and notes
- global context, final bias, final action, and decision notes
- local offline persistence via browser localStorage
- snapshot saving, JSON export, and JSON import
- service worker and manifest for installable offline PWA behavior

This is a tooling/UI addition only. It does not change trading logic, MQL5 code, Python research code, execution behavior, or registry semantics."
```
