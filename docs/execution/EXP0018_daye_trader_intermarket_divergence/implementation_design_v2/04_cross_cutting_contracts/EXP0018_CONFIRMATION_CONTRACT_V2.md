  ---
  id: EXP0018-CONFIRMATION-CONTRACT-V2
  title: "قرارداد تأیید v2"
  type: contract
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
# قرارداد تأیید v2

- observation intrabar می‌تواند تغییر کند.
- فقط اولین host closed-bar event پس از observation تصمیم را نهایی می‌کند.
- both-hunt تا close = invalidated.
- هم‌زمانی چند relationship یا BUY/SELL حذف نمی‌شود.
