# NDS Hook Trade State Machine

```text
DISABLED
→ IDLE
→ ELIGIBLE_HOOK
→ LIMIT_PENDING
→ POSITION_OPEN
→ WAITING_FOR_SAME_DIRECTION_F123
→ POSITION_CLOSED_ON_F3
→ IDLE
```

## Blocking states

```text
BLOCKED_HOOK_GEOMETRY
BLOCKED_LIMIT_GEOMETRY
BLOCKED_VOLUME
BLOCKED_ALREADY_USED
BLOCKED_GLOBAL_ENTRY_LOCK
BLOCKED_EXPOSURE_CHANGED_DURING_ENTRY
BLOCKED_FOREIGN_POSITION_ON_SYMBOL
INVARIANT_MULTIPLE_PENDING_ORDERS
INVARIANT_MULTIPLE_MANAGED_POSITIONS
POSITION_CLOSE_FAILED
```

## Pending transitions

- hold while alive and unfilled;
- cancel after death boundary breach when enabled;
- transition to position when broker fills;
- never create a second managed pending.

## Position transitions

- protective SL may terminate the trade;
- opposite F123 does not close it;
- same-direction post-entry F123 closes it;
- while open, no new Setup may submit.

## Related

- [[NDS Hook Limit Entry Contract]]
- [[NDS Single Exposure Lock]]
- [[NDS Same Direction F123 Exit]]
