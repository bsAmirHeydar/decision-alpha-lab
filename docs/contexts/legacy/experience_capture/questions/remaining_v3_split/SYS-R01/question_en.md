# SYS-R01 — Final NDS Architecture and Build Order

## Purpose
چون بعد از ثبت ontology، سناریو، زون، ورود، ریسک، execution، data و AI باید ترتیب ساخت مشخص شود. بدون build order، پروژه سنگین و پراکنده می‌شود.

## Required Clarifications
- اول object builderها ساخته شوند یا execution layer؟
- Canonical State Packet قبل از AI لازم است؟
- Event ledger قبل از training لازم است؟
- Scenario/Zone/Entry layer قبل از backtest چطور ساخته شود؟
- UI لازم است یا بعداً؟
- Shadow/Paper/Live gate در چه مرحله‌ای می‌آید؟
- کدام بخش‌ها hard rule هستند؟
- کدام بخش‌ها trainable هستند؟
- کدام بخش‌ها فعلاً فقط مستندسازی شوند؟
- Roadmap نهایی ساخت سیستم چیست؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `nds_build_order_v1.csv`
- `system_architecture_v1.csv`
- `hard_rule_vs_trainable_policy_map_v1.csv`
- `deployment_roadmap_v1.csv`
