  ---
  id: EXP0018-DATA-SYNC-CONTRACT-V2
  title: "قرارداد داده چندنمادی v2"
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
# قرارداد داده چندنمادی v2

- هر bar دارای symbol, event_time_utc, event_time_ny, OHLC, completeness و source status است.
- alignment بر timestamp، نه index.
- missing bar explicit است؛ forward fill ممنوع.
- history synchronization قبل از detection gate می‌شود.
- symbol suffix mapping ورودی است و حدس خودکار فقط diagnostic پیشنهاد می‌دهد.
