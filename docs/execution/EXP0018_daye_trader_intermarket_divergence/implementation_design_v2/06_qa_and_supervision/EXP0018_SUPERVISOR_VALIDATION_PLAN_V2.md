  ---
  id: EXP0018-SUPERVISOR-PLAN-V2
  title: "EXP0018 Supervisor Validation Plan v2"
  type: test-plan
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# برنامه ناظر استراتژی

ناظر بدون خواندن کد باید بتواند برای هر نمونه بگوید:

1. دوره مرجع و دوره جاری درست‌اند؟
2. کدام نماد سطح را لمس کرده؟
3. نماد Protected تا close سطح را نزده؟
4. خط فقط روی Hunter و از extreme مرجع تا extreme کندل تأیید است؟
5. مرجع مصرف‌شده دوباره استفاده نشده؟
6. خروجی historical با replay همان روز یکی است؟

برای هر فاز حداقل ۵ نمونه مثبت، ۵ نمونه منفی و ۳ boundary ثبت می‌شود.
