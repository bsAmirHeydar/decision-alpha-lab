# نصب پچ Product Lab Foundation

این پچ پوشه مستقل `product_lab/` را برای ساخت ابزارها و اندیکاتورهای قابل فروش اضافه می‌کند و یک اسکریپت برای تمیز کردن مستندات پراکنده روت پروژه می‌گذارد.

## نصب با PowerShell

فایل زیپ پچ را داخل روت پروژه قرار بده و اجرا کن:

```powershell
Expand-Archive -Path .\product_lab_foundation_patch.zip -DestinationPath . -Force
Remove-Item .\product_lab_foundation_patch.zip -Force
```

## مرتب‌سازی READMEها و فایل‌های نصب پراکنده روت

اول پیش‌نمایش بگیر:

```powershell
.\tools\repo_maintenance\Move-RootDocs.ps1 -WhatIfOnly
```

اگر خروجی درست بود، جابه‌جایی واقعی:

```powershell
.\tools\repo_maintenance\Move-RootDocs.ps1
```

## ساخت اندیکاتور جدید

```powershell
.\product_lab\scripts\New-ProductLabItem.ps1 -Type indicator -Slug "nds-lens-pro" -Title "NDS Lens Pro"
```

## ساخت ابزار جدید

```powershell
.\product_lab\scripts\New-ProductLabItem.ps1 -Type tool -Slug "license-console" -Title "License Console"
```
