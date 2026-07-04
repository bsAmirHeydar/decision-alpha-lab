# RSK-R02 — Convexity Metrics and Cost-to-Potential Formula

## Purpose
چون گفتی win rate بعد از convexity مهم است، نه قبلش. پس باید خود convexity، cost، potential، reward openness و optionality قابل سنجش شوند.

## Required Clarifications
- Cost دقیقاً چیست: stop distance، spread، buffer، probability of fill، missed risk، یا همه؟
- Potential دقیقاً چیست: مقصد، فاصله باز، tail، چند مقصد، reward path، یا explosion؟
- Open reward path چطور عددی یا طبقه‌بندی می‌شود؟
- Explosion potential چه فرقی با destination distance دارد؟
- Optionality score چطور تعریف می‌شود؟
- حداقل convexity برای اینکه win rate بررسی شود چقدر است؟
- اگر stop خیلی کوچک ولی fill probability خیلی پایین باشد، خوب است یا بد؟
- اگر reward خیلی بزرگ ولی ساختار ضعیف باشد، convexity واقعی است یا توهم؟
- متریک‌ها global هستند یا per market/timeframe train می‌شوند؟
- خروجی نهایی فرمول عددی است یا score/class؟

## Image Requirement
خیر. اگر نمودار توزیع R داری، اختیاری مفید است.

## Expected Derived Outputs
- `convexity_metric_model_v1.csv`
- `cost_to_potential_score_v1.csv`
- `optionality_score_v1.csv`
- `reward_path_openness_model_v1.csv`
