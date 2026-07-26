---
id: EXP0018-P02-EXACT-ALIGNMENT
title: "P02 Exact Timestamp Alignment"
type: algorithm
status: active
project: EXP0018
---
# الگوریتم همگام‌سازی

دو آرایه chronological با two-pointer پیمایش می‌شوند:

```text
A.time == B.time → pair
A.time < B.time  → unmatched A
A.time > B.time  → unmatched B
```

Index خام هیچ authority ندارد. دو bar در position مشابه ولی با اختلاف یک ثانیه pair نمی‌شوند.

## ممنوع

- nearest-bar matching
- tolerance window
- forward fill
- previous close substitution
- zero-price placeholder

هر سیاست tolerance در آینده نیازمند ADR جدا است.
