  ---
  id: EXP0018-TEST-RELEASE-MAP-V2
  title: "EXP0018 Test and Release Map v2"
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

# نقشه تست و Release

```text
Static/Schema
→ Unit/Pure Functions
→ Invariant/Property
→ Scenario Fixtures
→ Historical Replay
→ Live/Replay Reconciliation
→ Visual Golden Review
→ Performance/Restart
→ Supervisor Sign-off
→ RC + Rollback Drill
```

## هیچ تستی چه چیزی را اثبات نمی‌کند؟

- Compile فقط پذیرش syntax/type را اثبات می‌کند.
- Screenshot فقط همان نمونه را اثبات می‌کند.
- Replay بدون causal-time audit می‌تواند leakage داشته باشد.
- ناظر بصری جای duplicate/schema tests را نمی‌گیرد.
