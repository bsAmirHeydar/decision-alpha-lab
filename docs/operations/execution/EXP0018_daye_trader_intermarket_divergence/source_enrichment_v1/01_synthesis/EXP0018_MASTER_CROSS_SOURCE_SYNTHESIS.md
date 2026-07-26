# سنتز کل کورپس Quarterly Theory برای EXP0018

## تصویر کلان

هر سه PDF بازار را به‌عنوان ساختاری فرکتال از چرخه‌های چهارقسمتی توصیف می‌کنند. Q1 اطلاعات اولیه/رنج، Q2 دستکاری یا accumulation بسته به profile، Q3 distribution/manipulation و Q4 ادامه یا برگشت است. دو profile اصلی `AMDX` و `XAMD` چندین بار تکرار می‌شوند.

## ارتباط با EXP0018

هسته EXP0018 فعلاً یک موتور تشخیص واگرایی میان دو نماد در روابط زمانی مشخص است. PDFها نشان می‌دهند این موتور می‌تواند در آینده داخل یک context بزرگ‌تر قرار گیرد:

```text
Time hierarchy
  -> Quarter identity
  -> True Open / DFR context
  -> Intermarket divergence
  -> Confirmation / lifecycle
  -> Optional entry context
```

اما فقط بخش `Intermarket divergence + time relationship` در scope فعلی canonical است.

## عناصر مشترک سه PDF

- زمان و قیمت فرکتال‌اند.
- Q2 open یک True Open است.
- واگرایی فقط در context زمانی مناسب معنی‌دارتر می‌شود.
- سطوح تایم بالاتر و نقدینگی می‌توانند context بدهند.
- رفتار یک نماد نسبت به نمادهای همبسته برای تشخیص ضعف/قدرت استفاده می‌شود.
- تایم پایین باید با تایم بالا ارتباط داشته باشد.

## عناصر گسترش‌دهنده

- DFR و projection؛
- sequential relationships بین quarterها؛
- stacked True Opens؛
- خبر و calendar timing؛
- SSMT taxonomy؛
- intermarket hierarchy؛
- precision levels و execution workflow.

## نتیجه مهندسی

PDFها نقشه یک پلتفرم پژوهشی کامل را می‌دهند، نه مجوز افزودن همه چیز به Expert اصلی. معماری باید core detector را کوچک و deterministic نگه دارد و enrichmentها را به ماژول‌های جدا و خاموش‌پیش‌فرض منتقل کند.
