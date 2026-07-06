
---
type: workflow
---

# Research → Execution Pipeline

## مسیر رسمی

```text
Observation
→ Concept Note
→ Hypothesis
→ Experiment
→ Analysis
→ Validation
→ Production Candidate
→ Monitoring
→ Archive / Learning
```

## قانون اتصال

هر مرحله باید خروجی مرحله قبلی را به شکل لینک Obsidian نگه دارد.

### Observation

- از چارت، ژورنال، خطای کد، backtest یا شهود انسانی می‌آید.
- نباید مستقیم وارد execution شود.

### Concept Note

- در `docs/obsidian_deep/02_concepts` یا `docs/obsidian_deep/99_inbox` ثبت می‌شود.
- باید به source documents وصل شود.

### Hypothesis

- با template ساخته می‌شود.
- باید claim، mechanism، metric و failure condition داشته باشد.

### Experiment

- باید reproducible باشد.
- باید ورودی/خروجی و metricها را ثبت کند.

### Validation

- باید تلاش کند ایده را رد کند.
- باید baseline و regime را لحاظ کند.

### Production Candidate

- فقط وقتی مجاز است که validation کافی داشته باشد.
- باید guardrail و monitoring داشته باشد.
