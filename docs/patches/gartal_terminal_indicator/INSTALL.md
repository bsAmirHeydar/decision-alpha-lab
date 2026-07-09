# Install — Gartal Terminal Indicator Patch

زیپ پچ را در روت پروژه بگذارید و در PowerShell اجرا کنید:

```powershell
Expand-Archive -Path .\gartal_terminal_indicator_patch.zip -DestinationPath . -Force
Remove-Item .\gartal_terminal_indicator_patch.zip -Force
```

بعد وضعیت Git را چک کنید:

```powershell
git status
```

اگر تغییرات Obsidian workspace ناخواسته بود:

```powershell
git restore .obsidian/graph.json .obsidian/workspace.json
```

Stage:

```powershell
git add product_lab/indicators/gartal_terminal product_lab/registry/entries/gartal_terminal.md docs/patches/gartal_terminal_indicator
```

Commit:

```powershell
git commit -m "feat(product-lab): add gartal terminal news indicator architecture"
```

## تست اسکلت MQL5

فایل اصلی:

```text
product_lab/indicators/gartal_terminal/mql5/GartalTerminal.mq5
```

برای تست اولیه در MT5:

1. فولدر `mql5` را در مسیر Indicators کپی کنید یا فایل‌ها را به ساختار MQL5 منتقل کنید.
2. فعلاً `InpUseSampleData=true` است تا UI با داده نمونه بالا بیاید.
3. برای اتصال واقعی، در نسخه بعدی `ForexFactory parser adapter` تکمیل شود.

## نکته WebRequest

برای دریافت مستقیم از منبع خارجی، کاربر باید URL منبع را در MT5 whitelist کند:

```text
Tools → Options → Expert Advisors → Allow WebRequest for listed URL
```
