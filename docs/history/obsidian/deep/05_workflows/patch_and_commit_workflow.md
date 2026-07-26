
---
type: workflow
---

# Patch and Commit Workflow

## ترتیب استاندارد

1. Issue یا نیاز را در Obsidian ثبت کن.
2. فایل‌های مرتبط را از Local Graph پیدا کن.
3. Patch plan بنویس.
4. تغییر محدود بزن.
5. Compile/test checklist را اجرا کن.
6. ZIP patch بساز.
7. commit message کامل بنویس.
8. نتیجه را به ADR یا source card وصل کن.

## قانون پچ

- پچ نباید کل پروژه را جایگزین کند مگر وقتی صریحاً لازم است.
- پچ باید PowerShell-friendly باشد.
- پچ باید قابل rollback باشد.
- پچ نباید رفتار trading را بی‌اجازه تغییر دهد.
