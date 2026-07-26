# نصب خروجی Obsidian برای Decision Alpha Lab

این ZIP یک **overlay patch** است؛ یعنی کل پروژه را دوباره نمی‌آورد، بلکه پروژه فعلی را به یک Obsidian Vault ساختاریافته تبدیل می‌کند.

## روش استفاده در PowerShell ویندوز

در ریشه پروژه `decision-alpha-lab-main` برو و این را اجرا کن:

```powershell
Expand-Archive -Path .\alpha_lab_obsidian_overlay_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_obsidian_overlay_patch.zip
```

بعد در Obsidian:

```text
Open folder as vault -> decision-alpha-lab-main
```

## نقطه شروع

بعد از باز کردن Vault، این فایل را باز کن:

```text
00_OBSIDIAN_START_HERE.md
```

## چیزهایی که اضافه شده

- داشبورد مرکزی پروژه؛
- MOCهای تخصصی برای Flag Counting، Hook/NDS، MQL Native، AI Execution، Validation، Execution و Registry؛
- کارت مستقل برای هر فایل مستندات؛
- نقشه روابط document/entity/concept؛
- استخراج متنی PDFهای مانیفست؛
- templateهای فرضیه، آزمایش، validation، ADR و Agent task؛
- policyهای Agent برای آینده پروژه؛
- پر کردن READMEها و reportهای خالی با اسکلت دقیق و linkable.

## نکته مهم

فایل‌های اصلی Markdown پروژه جابه‌جا نشده‌اند. این overlay فقط آنها را برای Obsidian قابل ناوبری، قابل جست‌وجو، و قابل اتصال می‌کند.
