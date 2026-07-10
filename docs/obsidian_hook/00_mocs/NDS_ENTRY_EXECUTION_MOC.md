# NDS Entry and Execution MOC

## Purpose

This map connects the existing NDS Hook Canon to a future trading system without allowing structure detection, setup interpretation, risk, and broker execution to collapse into one signal.

```text
Canonical valid Hook
→ Canonical Zone
→ Setup Candidate
→ Trade Plan
→ Command Preview
→ Risk Authorization
→ Broker Authorization
```

The current implementation stops at a **zero-volume, no-send Command Preview**.

## Authority

- [[../08_entry_execution/NDS Entry Doctrine]]
- [[../08_entry_execution/NDS Authority Boundary]]
- [[../08_entry_execution/NDS Structure Snapshot Contract]]
- [[../08_entry_execution/NDS Zone Adapter]]
- [[../08_entry_execution/NDS Setup State Machine]]
- [[../08_entry_execution/NDS Trade Plan Contract]]
- [[../08_entry_execution/NDS Command Preview Contract]]
- [[../08_entry_execution/NDS Risk and Capital Boundary]]
- [[../08_entry_execution/NDS Entry Audit Outputs]]
- [[../08_entry_execution/NDS Entry Canon Backlog]]

## Implementation

- [[../03_architecture/Phase 51 NDS Entry Transition Architecture]]
- [[../../nds_entry_architecture/README|NDS Entry Transition Architecture package]]
- [[../../nds_hook_architecture/68_phase51_nds_entry_transition_architecture|Phase 51 engineering overlay]]

## Operator workflow

1. Run the central Phoenix expert with the default pre-Canon profile.
2. Confirm that the latest eligible valid Hook reaches the structure snapshot.
3. Inspect the explicit Zone block reason.
4. Use diagnostic manual geometry only to test downstream state and CSV contracts.
5. Never interpret a diagnostic Setup or Command Preview as canonical or tradable.
6. Promote the canonical adapter only after the Hook/Zone questionnaire decisions are versioned and tested.

## Review template

- [[../05_templates/NDS Setup Review Template]]

## Non-negotiable safety

```text
volume = 0
send_allowed = false
command_action = PREVIEW_ONLY_NO_SEND
```

No module in Phase 51 may call a broker-send function.
