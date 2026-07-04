# DATA-R03 — Training Granularity and Regime Weight Drift

## Purpose
چون گفتی شاید حتی در یک market/timeframe هم وزن‌ها ثابت نمانند. باید معلوم شود آموزش global، market-specific، timeframe-specific و dynamic weight regime چطور انجام می‌شود.

## Required Clarifications
- Global training دقیقاً چه چیزهایی را یاد می‌گیرد؟
- Market-specific training چه زمانی لازم است؟
- Market-timeframe-specific training چه زمانی لازم است؟
- Dynamic weight regime یعنی چه؟
- Rolling windows چطور استفاده شوند؟
- Minimum sample برای اعتماد به وزن‌ها چقدر است؟
- Stability criteria چیست؟
- Drift detection چطور انجام شود؟
- Weight decay/boost چطور تعریف شود؟
- چه زمانی یک rule جهانی کنار گذاشته یا فقط local می‌شود؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `training_granularity_model_v1.csv`
- `market_timeframe_policy_v1.csv`
- `dynamic_weight_regime_model_v1.csv`
- `weight_drift_detection_v1.csv`
