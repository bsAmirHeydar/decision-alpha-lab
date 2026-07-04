# TEST-R02 — Anti-Overfit, OOS, and Deployment Criteria

## Purpose
چون اگر سیاست‌ها train می‌شوند، خطر overfit جدی است. باید معلوم شود چه زمانی یک rule یا policy واقعاً قابل اعتماد و deployable است.

## Required Clarifications
- In-sample / out-of-sample split چطور باشد؟
- Walk-forward چطور طراحی شود؟
- Market split لازم است؟
- Timeframe split لازم است؟
- Regime split چطور تعریف شود؟
- Minimum sample size چقدر باشد؟
- Stability metrics چیست؟
- Failure cases چطور گزارش شوند؟
- Degradation tolerance چقدر است؟
- Deployment threshold چیست؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `anti_overfit_test_plan_v1.csv`
- `oos_validation_policy_v1.csv`
- `walk_forward_evaluation_v1.csv`
- `deployment_criteria_v1.csv`
