---
title: "24 — State Machines"
tags: [exp0019, faerie-protocol, divergence-context]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
doc_version: 1.0.0
last_updated: 2026-07-13
---
# 24 — State Machines

## Session

```text
UPCOMING -> ACTIVE -> COMPLETE -> ARCHIVED
```

## Reference side

```text
UNBUILT -> READY_INTACT -> EXHAUSTED_BY_PROTECTED_TOUCH -> EXPIRED
          \-> MISSING_DATA
```

## Candidate

```text
NONE -> RAW_ASYMMETRY -> CONFIRMED -> ARCHIVED
                    \-> CANCELLED_BEFORE_CLOSE
                    \-> MISSING_DATA
```

## Weekly gate

```text
UNRESOLVED -> NONE | BULLISH_ONLY | BEARISH_ONLY | CONFLICT | MISSING_DATA
```

## Trade entitlement

```text
NOT_EVALUATED -> ELIGIBLE -> PLANNED -> CONSUMED
             \-> SUPPRESSED_WW
             \-> SUPPRESSED_QUOTA
             \-> REJECTED_GEOMETRY
```

## Drawing

```text
NOT_DRAWN -> DRAWN_IMMUTABLE
          \-> DRAW_FAILED_RETRYABLE
```

## transition rule

هر transition باید monotonic و reason-coded باشد. هیچ transition به عقب با mutation silent مجاز نیست؛ correction با superseding record انجام می‌شود.

## سطح اختیار این سند

این سند چهار سطح حقیقت را از هم جدا می‌کند:

| سطح | معنی |
|---|---|
| `OWNER_CONFIRMED` | در فایل Word یا درخواست صریح مالک آمده است. |
| `LEGACY_IMPLEMENTED` | در `FP 101.mq5` وجود دارد، حتی اگر قرارداد نهایی نباشد. |
| `ARCHITECTURAL_DERIVATION` | برای ماژولارکردن و حفظ هسته‌های مشترک از منبع استنتاج شده است. |
| `OPEN_DECISION` | قبل از کدنویسی نهایی نیازمند تصمیم مالک است. |

قاعده: رفتار Legacy فقط وقتی canonical است که با Owner Intent و قرارداد این پکیج تعارض نداشته باشد.

## ناوبری

- [[00_EXP0019_MOC|MOC اصلی EXP0019]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|ثبت ابهام‌ها و تصمیم‌ها]]
- [[34_IMPLEMENTATION_ROADMAP|نقشه پیاده‌سازی]]
- [[35_HANDOFF_TO_CODE|تحویل به کدنویسی]]
