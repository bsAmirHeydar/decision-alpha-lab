
---
type: ontology
---

# Project Ontology — هستی‌شناسی پروژه

## Entityهای اصلی

| Entity | معنی | نمونه |
|---|---|---|
| Concept | مفهوم تحلیلی/معماری | Hook, Rally, F-counting |
| Hypothesis | ادعای قابل تست | H0007 |
| Experiment | اجرای تست روی داده/کد | EXP0016 |
| Validation | ممیزی و اعتبارسنجی | VAL0001 |
| Component | ماژول core یا کد | CP0001, M0001 |
| Execution Profile | حالت اجرای research/paper/live | EXEC profile |
| Registry | state machine پروژه | registry/*.yaml |
| ADR | تصمیم معماری | ADR-XXXX |
| Journal Label | تجربه انسانی ساختاریافته | clean_hook, path_smooth |
| Agent Task | کار قابل واگذاری به ایجنت | patch audit, experiment design |

## Relationهای مجاز

- `defines`: تعریف می‌کند
- `implements`: پیاده‌سازی می‌کند
- `tests`: می‌آزماید
- `validates`: اعتبارسنجی می‌کند
- `depends_on`: وابسته است
- `produces`: تولید می‌کند
- `audits`: ممیزی می‌کند
- `guards`: محدود می‌کند
- `labels`: برچسب می‌زند

## مسیر استاندارد

```text
Observation → Concept → Hypothesis → Experiment → Validation → Production → Monitoring → Learning
```
