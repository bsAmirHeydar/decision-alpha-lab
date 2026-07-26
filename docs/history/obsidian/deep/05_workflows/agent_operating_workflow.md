
---
type: workflow
---

# Agent Operating Workflow

## نقش ایجنت در پروژه

ایجنت باید نقش‌های زیر را داشته باشد:

1. Librarian: پیدا کردن سند، مفهوم، relation.
2. Research Designer: تبدیل ایده به hypothesis و experiment.
3. Patch Engineer: تولید patch محدود و توضیح diff.
4. Validation Skeptic: تلاش برای رد نتیجه مثبت.
5. Journal Analyst: تبدیل تجربه انسانی به label.
6. Obsidian Maintainer: نگه داشتن گراف دانش.

## دسترسی‌های مجاز

| Level | دسترسی | مجاز؟ |
|---|---|---|
| Read-only repo | خواندن docs/code/registry | بله |
| Draft docs | ساخت hypothesis/report/ADR | بله |
| Patch generation | ساخت ZIP patch | بله با diff |
| Test execution | اجرای تست local | بله با sandbox |
| Paper annotation | تحلیل paper/live shadow | با احتیاط |
| Live order | ارسال order واقعی | خیر در MVP |

## guardrail اصلی

AI در پروژه authority نیست؛ automation و audit layer است.
