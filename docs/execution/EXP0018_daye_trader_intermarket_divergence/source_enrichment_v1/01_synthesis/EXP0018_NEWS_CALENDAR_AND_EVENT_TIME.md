# تقویم اقتصادی، خبر و Event Time

PDFهای QT و Trader Daye بارها از خبر قرمز به‌عنوان زمان تزریق نقدینگی و احتمال manipulation/distribution نام می‌برند. نکات اصلی:

- تقویم در شروع هفته بررسی شود؛
- روزهای دارای تراکم خبر ممکن است high/low هفته را بسازند؛
- Q3 و open 9:30 نیویورک با volatility مرتبط دانسته شده‌اند؛
- news opening price و candle خبر می‌تواند level باشد؛
- CPI/NFP/FOMC contextهای جدا دارند.

این‌ها causal rule اثبات‌شده نیستند. پیاده‌سازی نیازمند feed خبر نسخه‌دار، timezone، revision handling، event importance و test split است. Core EXP0018 نباید به نبود feed خبر وابسته شود.
