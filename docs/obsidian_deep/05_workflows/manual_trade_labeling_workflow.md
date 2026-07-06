
---
type: workflow
---

# Manual Trade Labeling Workflow

هدف این workflow این است که تجربه انسانی تریدر تبدیل به داده قابل یادگیری شود.

## بعد از هر معامله ثبت کن

- سناریو: Hook / Rally / F-count / Divergence / Zone
- کیفیت مسیر: smooth / choppy / compressed / explosive
- نوع تصمیم: convex / mean-reversion / continuation / rejection
- زمان ورود: قبل از confirmation / بعد از confirmation / دیرهنگام
- خطا: early / late / emotional / invalid structure / risk mistake
- نتیجه: R multiple، duration، MAE/MFE

## خروجی مورد نیاز برای AI

```yaml
trade_id:
date:
symbol:
timeframe:
scenario_type:
manual_labels:
entry_reason:
exit_reason:
rule_alignment:
emotional_state:
post_trade_lesson:
linked_concepts:
linked_hypothesis:
```
