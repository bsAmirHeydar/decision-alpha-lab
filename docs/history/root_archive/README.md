# Root Archive

این پوشه برای جمع‌آوری مستندات پراکنده روت پروژه است.

هدف این است که روت پروژه تمیز بماند و فقط فایل‌های اصلی مثل `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `requirements.txt` و `.gitignore` در روت باقی بمانند.

## گروه‌بندی پیشنهادی

```text
docs/root_archive/
├── 00_start_here/
├── install_guides/
├── patch_readmes/
└── patch_diffs/
```

برای انتقال فایل‌ها از اسکریپت زیر استفاده کن:

```powershell
.\tools\repo_maintenance\Move-RootDocs.ps1
```

برای پیش‌نمایش بدون جابه‌جایی:

```powershell
.\tools\repo_maintenance\Move-RootDocs.ps1 -WhatIfOnly
```
