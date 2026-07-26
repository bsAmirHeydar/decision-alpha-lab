# NDS Hook 86.4 Cycle R1 State Machine

```text
DISABLED
→ NO_ELIGIBLE_SETUP / BLOCKED
→ PAPER_LIMIT or LIMIT_SENT
→ PENDING_HELD
→ POSITION_HELD_BY_FIXED_R1_PROTECTION
→ broker SL/TP outcome
```

## Pending

The shared magic-wide exposure lock prevents a second setup. After Magic ownership is established, the broker comment recovers the lifecycle profile. For `864R1`, broker Entry/SL/TP are verified every cycle. Invalid protection triggers cancellation; failed cancellation blocks the lifecycle for reconciliation. Hook death may also cancel the pending order. x3→x4 does not reprice it.

## Position

The engine reads broker Open/SL/TP and verifies directional order and at-least-1R reward. Missing or invalid protection fails closed. The F123 exit detector is not consulted for this profile.

## Recovery

Broker orders and positions are scanned before Hook selection on every cycle/restart. Persistent setup identity prevents duplicate attempts.

## Related

- [[NDS Hook 86.4 Cycle R1 Entry Contract]]
- [[NDS Single Exposure Lock]]
- [[NDS Hook Trade State Machine]]
