  ---
  id: EXP0018-PERIOD-ID-CONTRACT-V2
  title: "قرارداد هویت دوره v2"
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
# قرارداد هویت دوره v2

`period_instance_id = project + period_type + ny_start + ny_end + symbol + schema_version`

دوره incomplete همان ID را دارد اما status متفاوت؛ نمی‌توان آن را با complete جایگزین کرد بدون transition audit.
