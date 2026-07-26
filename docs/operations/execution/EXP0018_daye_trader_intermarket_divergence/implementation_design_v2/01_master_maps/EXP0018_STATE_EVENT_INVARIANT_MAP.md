  ---
  id: EXP0018-STATE-EVENT-INVARIANT-MAP-V2
  title: "EXP0018 State Event Invariant Map v2"
  type: architecture
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

# State / Event / Invariant

## State machines

### Signal

```text
NONE → CANDIDATE → CONFIRMED
                 ↘ INVALIDATED_DOUBLE_HUNT
```

### Reference

```text
CANDIDATE → ACTIVE → PROTECTED → CONSUMED/RETIRED
```

### Period

```text
OPEN → BUILDING → CLOSED_COMPLETE
              ↘ CLOSED_INCOMPLETE
```

## Hard invariants

- confirmation only on host closed candle
- equality is hunt
- retired reference cannot return
- historical confirmed line remains immutable
- current and historical paths use same detector
- missing data cannot silently become no-hunt
- Core has no order API
