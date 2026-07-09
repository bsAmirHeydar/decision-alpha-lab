# Product Spec — {{PRODUCT_TITLE}}

## 1. هویت محصول

| فیلد | مقدار |
|---|---|
| Product Name | {{PRODUCT_TITLE}} |
| Slug | {{PRODUCT_SLUG}} |
| Product Type | Indicator |
| Platform | MetaTrader 5 |
| Status | idea |
| Created | {{CREATED_DATE}} |

## 2. مسئله مشتری

مشتری دقیقاً چه چیزی را سخت، کند، مبهم یا پرخطا انجام می‌دهد؟

```text
...
```

## 3. وعده محصول

این ابزار چه کمک مشخصی می‌کند؟

```text
...
```

## 4. چیزی که وعده نمی‌دهد

```text
این ابزار سیگنال قطعی، سود تضمینی یا جایگزین مدیریت ریسک نیست.
```

## 5. خروجی بصری

| لایه | توضیح | پیش‌فرض |
|---|---|---|
| Labels |  | On |
| Lines |  | On |
| Zones |  | Off |
| Alerts |  | Off |

## 6. Inputها

| Input | Type | Default | User Meaning | Advanced? |
|---|---|---|---|---|
| ShowLabels | bool | true | نمایش لیبل‌ها | No |
| Sensitivity | enum | Normal | حساسیت تشخیص | No |
| MaxBars | int | 1500 | کنترل پردازش | Yes |

## 7. سناریوهای استفاده

### مناسب

- ...

### نامناسب

- ...

## 8. معیار آماده شدن برای Beta

- [ ] نصب تمیز
- [ ] چارت خلوت
- [ ] ورودی‌های قابل فهم
- [ ] مستند مشتری
- [ ] تست روی چند نماد و تایم‌فریم
