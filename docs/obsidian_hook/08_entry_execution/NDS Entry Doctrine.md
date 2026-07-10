# NDS Entry Doctrine

## Canonical separation

```text
Structure ≠ Setup
Setup ≠ Trade Plan
Trade Plan ≠ Command
Command ≠ Risk Authorization
Risk Authorization ≠ Broker Authorization
```

A Hook describes market anatomy. It does not, by itself, issue a buy or sell instruction. The Entry layer must preserve the Hook evidence and attach every downstream interpretation through explicit IDs and policies.

## Current state

Phase 51 implements a transition scaffold:

- reads the post-classification Hook snapshot;
- selects an eligible valid Hook;
- keeps Hook direction separate from trade direction;
- invokes a single Zone adapter seam;
- builds a Setup, Trade Plan, and Command Preview record;
- exports every block and decision;
- never sends an order.

Phase 52 is a separate opt-in executable profile for the newly locked narrow contract: valid HH/F3H Hook terminal limit, one exposure, and same-direction post-entry F123 exit. It does not turn the generic Zone/Command scaffold into a send path.

## Safe default

```text
Profile = PRE_CANON_BLOCKED
Direction = UNRESOLVED
Order = UNRESOLVED
Stop = UNRESOLVED
Target = UNRESOLVED
Zone Canon lock = false
Trade contract lock = false
```

This profile is successful when it captures structure and blocks at the first unresolved authority boundary.

## Related

- [[NDS Authority Boundary]]
- [[NDS Zone Adapter]]
- [[NDS Setup State Machine]]
- [[NDS Hook Limit Entry Contract]]
- [[NDS Same Direction F123 Exit]]
- [[NDS Single Exposure Lock]]
- [[../00_mocs/NDS_ENTRY_EXECUTION_MOC]]
