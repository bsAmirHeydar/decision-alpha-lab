# INSTALL — EXP0017 Phase 01 Time Anatomy Patch

این پچ فاز ۱ پیاده‌سازی EXP0017 را اضافه می‌کند: **CG Time Anatomy**.

## نصب در PowerShell

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase01-time-anatomy-code-docs-obsidian-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase01-time-anatomy-code-docs-obsidian-patch.zip"
```

## فایل اصلی اکسپرت

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Time_Anatomy.mq5
```

## مرز فاز

این فاز هیچ تریدی نمی‌کند، هیچ هانتی تشخیص نمی‌دهد، هیچ واگرایی نمی‌سازد، و هیچ ورودی/خروجی معاملاتی ندارد. فقط زمان و سایکل‌گروپ‌ها را می‌سازد.
