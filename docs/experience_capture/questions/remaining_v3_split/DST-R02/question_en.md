# DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy

## Purpose
چون در مدل تو سود فقط یک TP ثابت نیست؛ ممکن است چند مقصد، خروج پله‌ای، runner و tail داشته باشیم. این سیاست باید از سناریو و position جدا ولی متصل تعریف شود.

## Required Clarifications
- TP اولیه کجا قرار می‌گیرد؟
- TP همیشه روی مقصد است یا کمی قبل/بعد از مقصد؟
- خروج پله‌ای چند مرحله‌ای چطور تصمیم‌گیری می‌شود؟
- چند درصد در مقصد اول، دوم، سوم بسته می‌شود؟
- خروج پله‌ای rule-based است یا trainable؟
- اگر مقصد اول نزدیک باشد ولی مقصد دوم خیلی باز باشد، چطور تصمیم می‌گیریم؟
- آیا می‌شود بخشی از معامله را برای tail / explosion باز گذاشت؟
- بعد از خروج اول، stop بقیه position چه می‌شود؟
- Break-even مجاز است یا با منطق convexity تضاد دارد؟
- خروج نهایی چه زمانی است؟

## Image Requirement
اختیاری. اگر نمونه چند مقصد و خروج پله‌ای داری، عکس کمک می‌کند.

## Expected Derived Outputs
- `take_profit_policy_v1.csv`
- `partial_exit_policy_v1.csv`
- `multi_destination_exit_model_v1.csv`
- `runner_tail_position_policy_v1.csv`
