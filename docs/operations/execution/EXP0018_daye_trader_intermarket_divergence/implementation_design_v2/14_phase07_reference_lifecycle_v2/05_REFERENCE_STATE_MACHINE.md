# Reference state machine

```text
UNKNOWN
  └─ first immutable confirmation
       → PROTECTED_SURVIVES

PROTECTED_SURVIVES
  ├─ distinct use, same protected still clean
  │    → PROTECTED_SURVIVES
  ├─ protected touches own reference
  │    → RETIRED_PROTECTED_TOUCH
  ├─ both touch
  │    → RETIRED_DOUBLE_HUNT
  └─ previous protected becomes hunter
       → RETIRED_ROLE_SWITCH
```

All retired states are terminal. `RETIRED → PROTECTED_SURVIVES` is forbidden.
