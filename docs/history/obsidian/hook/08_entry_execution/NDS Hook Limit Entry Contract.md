# NDS Hook Limit Entry Contract

## Source

Only canonical valid `HH`, `F3H`, and dual `F3H+HH` sequences can create a Phase 52 order.

```text
valid Hook family
→ closed Hook
→ terminal price
→ pending limit
```

## Direction and price

- positive Hook → Buy Limit at raw terminal / `resolve_price`;
- negative Hook → Sell Limit at raw terminal / `resolve_price`.

The terminal is the canonical raw-price extreme already used by Hook Phase02, not a compact label coordinate.

## Protection

The stop lies beyond the Hook `death_boundary_price`, or beyond `origin_price` when no separate death field exists. No fixed TP is attached.

## Related

- [[NDS Same Direction F123 Exit]]
- [[NDS Single Exposure Lock]]
- [[NDS Hook Trade State Machine]]
- [[../02_policies/Positive Hook Terminal Is Lowest Valley]]
- [[../02_policies/Negative Hook Terminal Is Highest Peak]]
- [[../00_mocs/NDS_ENTRY_EXECUTION_MOC]]

## Profile separation

This note remains authoritative for the Phase 52 `TERMINAL_F123` profile. The Phase 55 `HOOK_864_CYCLE_R1` profile does not change terminal entry or F123 exit semantics; it is separately specified in [[NDS Hook 86.4 Cycle R1 Entry Contract]]. Both profiles consume the same canonical Hook object and shared exposure/risk/broker stack.
