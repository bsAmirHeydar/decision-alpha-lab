---
id: EXP0018-P03-COMPLETENESS
title: "P03 Completeness State Model"
type: spec
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - phase03
  - period-aggregation
---

# ماشین وضعیت کامل‌بودن

```text
EMPTY       هیچ bar در Window وجود ندارد
OPEN        Window هنوز پایان نیافته است
PARTIAL     Window بسته شده اما grid کامل نیست
COMPLETE    Window بسته، اولین bar روی start، آخرین bar روی end-base و count دقیق است
UNAVAILABLE یکی از نمادها برای این period وجود ندارد
INVALID     bar خارج از grid یا count غیرممکن دیده شده است
```

قاعده مهم:

```text
No Data ≠ Complete
No Data ≠ No Hunt
Open ≠ Partial
```

`coverage_percent` فقط یک اندازه‌گیری است. رسیدن به درصد بالا، دوره ناقص را به‌صورت پنهانی کامل نمی‌کند.
