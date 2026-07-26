  ---
  id: EXP0018-PERFORMANCE-BUDGET-V2
  title: "بودجه Performance v2"
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
# بودجه Performance v2

- no full lookback scan per tick
- new closed candle is primary trigger
- caches bounded by configured lookback
- drawing batch and ChartRedraw throttled
- CSV writes buffered or event-based
- Phase performance baseline before next phase
