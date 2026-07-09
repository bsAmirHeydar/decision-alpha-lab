# Product Lab Foundation Patch

## تغییرات

- اضافه شدن پوشه مستقل `product_lab/` برای ساخت اندیکاتور و ابزار قابل فروش.
- اضافه شدن استانداردهای محصول‌سازی، اعتبارسنجی، بسته‌بندی، فروش، لایسنس و مستند مشتری.
- اضافه شدن قالب آماده برای اندیکاتورهای جدید.
- اضافه شدن قالب آماده برای ابزارهای پشتیبان.
- اضافه شدن کاتالوگ محصول و Backlog ایده‌ها.
- اضافه شدن اسکریپت `New-ProductLabItem.ps1` برای ساخت سریع پوشه محصول جدید.
- اضافه شدن اسکریپت `Move-RootDocs.ps1` برای انتقال READMEها و INSTALLهای پراکنده روت به `docs/root_archive/`.

## فایل‌های مهم

| مسیر | کاربرد |
|---|---|
| `product_lab/00_START_HERE.md` | نقطه شروع محصول‌سازی |
| `product_lab/docs/00_product_strategy.md` | استراتژی تبدیل تحلیل به محصول |
| `product_lab/docs/01_indicator_design_standard.md` | استاندارد طراحی اندیکاتور |
| `product_lab/docs/02_validation_standard.md` | استاندارد اعتبارسنجی قبل از فروش |
| `product_lab/docs/03_packaging_distribution_standard.md` | استاندارد انتشار و بسته‌بندی |
| `product_lab/docs/04_license_sales_ops.md` | چارچوب لایسنس و فروش |
| `product_lab/registry/indicator_catalog.md` | کاتالوگ اندیکاتورها |
| `tools/repo_maintenance/Move-RootDocs.ps1` | مرتب‌سازی مستندات روت |
