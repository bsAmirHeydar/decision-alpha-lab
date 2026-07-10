  ---
  id: EXP0018-DATA-LINEAGE-MAP-V2
  title: "EXP0018 Data Lineage Map v2"
  type: data-contract
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

# نقشه Lineage داده

```text
Broker bars
→ normalized symbol-local bars
→ synchronized timestamp frame
→ period snapshots
→ relationship instance
→ hunt observation
→ confirmation event
→ lifecycle transition
→ visual event / ledger row
→ replay hash / QA evidence
```

## شناسه‌های پیشنهادی

- `run_id`
- `symbol_pair_id`
- `period_instance_id`
- `reference_id`
- `relationship_id`
- `observation_id`
- `signal_event_id`
- `visual_event_id`
- `object_id`

تمام شناسه‌ها deterministic و از فیلدهای canonical ساخته می‌شوند؛ randomness ممنوع است.
