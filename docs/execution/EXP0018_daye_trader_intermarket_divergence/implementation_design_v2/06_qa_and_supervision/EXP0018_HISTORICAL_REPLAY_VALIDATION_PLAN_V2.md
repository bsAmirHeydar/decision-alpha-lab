  ---
  id: EXP0018-REPLAY-VALIDATION-V2
  title: "EXP0018 Historical Replay Validation Plan v2"
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

# اعتبارسنجی Replay

- یک range تاریخی با event-by-event cursor اجرا می‌شود.
- همان range در حالت live-forward یا simulated closed bars اجرا می‌شود.
- event IDs، transitions، lifecycle states و visual coordinates hash می‌شوند.
- mismatch به اولین causal event بازگردانده می‌شود.
- استفاده از final period high/low قبل از close ممنوع است.
