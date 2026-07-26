
---
type: canonical_model
---

# Canonical Model — مدل رسمی دانش Alpha Lab

این بخش ستون فقرات دانشی پروژه است. هر فایل مستند، هر مفهوم، هر آزمایش و هر پچ باید نسبت خود را با این مدل روشن کند.

## لایه‌ها

1. **فلسفه تصمیم**: پتانسیل، تحدب، هزینه شکست، گستره سود.
2. **آناتومی بازار**: Hook، Rally، F-counting، Decision Node، Zone، RTV.
3. **فرضیه‌سازی**: تبدیل شهود یا مشاهده به claim قابل تست.
4. **آزمایش**: تبدیل claim به protocol، داده، metric و failure condition.
5. **اعتبارسنجی**: audit، walk-forward، sensitivity، regime robustness، leakage check.
6. **اجرا**: MQL/Python bridge، chart visualization، input policy، license، patch discipline.
7. **ژورنال و تجربه انسانی**: label کردن ادراک انسانی و تبدیل آن به dataset.
8. **ایجنت AI**: automation layer، نه authority layer.

## اصل معماری

```text
Concept → Hypothesis → Experiment → Validation → Production Candidate → Monitoring → Archive/Learning
```

هیچ مفهومی نباید بی‌ردیابی بماند. هر مفهوم باید حداقل به یکی از این‌ها وصل شود:

- تعریف canonical
- سند source
- hypothesis
- experiment
- validation
- implementation file
- decision/ADR
- journal label
