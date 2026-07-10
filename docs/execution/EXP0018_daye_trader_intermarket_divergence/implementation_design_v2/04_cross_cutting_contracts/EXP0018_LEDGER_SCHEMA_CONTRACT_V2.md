  ---
  id: EXP0018-LEDGER-CONTRACT-V2
  title: "قرارداد Schema دفتر ممیزی v2"
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
# قرارداد Schema دفتر ممیزی v2

هر ledger row: run_id, schema_version, event_id, event_type, event_time_utc/ny, availability_time, symbol pair, relationship, reference/current IDs, side, hunter/protected, status, reason_code.

Primary key duplicate و orphan critical failure است.
