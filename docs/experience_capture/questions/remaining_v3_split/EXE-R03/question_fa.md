# EXE-R03 — Shadow, Paper, and Live Transition

چرا مهم است: چون سیستم باید مرحله‌ای جلو برود؛ اول shadow، بعد paper، بعد live. هر مرحله باید معیار عبور، safety gate و kill switch داشته باشد.

برای پاسخ، حتماً این موارد را روشن کن:
• Shadow mode دقیقاً چه چیزهایی را log می‌کند؟
• Paper mode چه تفاوتی با shadow دارد؟
• Live mode چه safety gateهایی می‌خواهد؟
• AI در live فقط rank/veto می‌کند یا نقش دیگری هم دارد؟
• چه metricهایی برای رفتن از shadow به paper لازم است؟
• چه metricهایی برای رفتن از paper به live لازم است؟
• چه kill switchهایی لازم است؟
• اگر مدل drift کرد، به کدام mode برمی‌گردد؟
• هر market/timeframe جدا approval می‌خواهد؟
• Audit برای هر intent و order چگونه است؟

عکس لازم: خیر. پاسخ متنی کافی است.

خروجی مورد انتظار بعد از پاسخ:
• shadow_mode_policy_v1.csv
• paper_mode_policy_v1.csv
• live_gate_policy_v1.csv
• kill_switch_policy_v1.csv

پاسخ شما:
