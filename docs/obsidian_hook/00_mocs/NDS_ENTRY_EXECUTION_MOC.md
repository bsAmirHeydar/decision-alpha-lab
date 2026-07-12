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

The Phase 51 general pipeline stops at a **zero-volume, no-send Command Preview**. Phase 52 adds a separate opt-in executable profile restricted to valid HH/F3H Hook-terminal limits and same-direction F123 exits.

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
- [[../08_entry_execution/NDS Hook Limit Entry Contract]]
- [[../08_entry_execution/NDS Single Exposure Lock]]
- [[../08_entry_execution/NDS Same Direction F123 Exit]]
- [[../08_entry_execution/NDS Hook Trade State Machine]]
- [[../08_entry_execution/NDS Hook Trade Audit Ledger]]
- [[../08_entry_execution/NDS Hook Trade Operator Checklist]]
- [[../04_debug/NDS Strategy Tester OnInit License Gate]]

## Implementation

- [[../03_architecture/Phase 51 NDS Entry Transition Architecture]]
- [[../../nds_entry_architecture/README|NDS Entry Transition Architecture package]]
- [[../../nds_hook_architecture/68_phase51_nds_entry_transition_architecture|Phase 51 engineering overlay]]
- [[../03_architecture/Phase 52 NDS Hook Limit F123 Execution]]
- [[../../nds_hook_architecture/69_phase52_hook_limit_f123_execution|Phase 52 engineering overlay]]
- [[../../nds_entry_architecture/phase52_hook_limit_f123_execution/README|Phase 52 detailed package]]

## Operator workflow

1. Run the central Phoenix expert with the default pre-Canon profile.
2. Confirm that the latest eligible valid Hook reaches the structure snapshot.
3. Inspect the explicit Zone block reason.
4. Use diagnostic manual geometry only to test downstream state and CSV contracts.
5. Never interpret a diagnostic Setup or Command Preview as canonical or tradable.
6. Promote the canonical adapter only after the Hook/Zone questionnaire decisions are versioned and tested.

## Review template

- [[../05_templates/NDS Setup Review Template]]

## Authority separation

Phase 51 remains permanently no-send:

```text
volume = 0
send_allowed = false
command_action = PREVIEW_ONLY_NO_SEND
```

Phase 52 is a separate strategy profile and requires both explicit inputs:

```text
InpNDSHookTradeEnabled = true
InpNDSHookTradeSendLiveOrders = true
```

Both default to false, and the single-exposure invariant is mandatory.


## Lightweight Strategy Tester

- [[NDS Lightweight Backtest Runtime]]
- [[NDS Backtest Performance Profiles]]
- [[NDS Backtest Parity Contract]]
## AI / Cycle Group research

- [[NDS_AI_CG_CYCLE_SELECTION_MOC]]

This branch is research-only and has no execution authority.

## F2-only lightweight execution profile

- [[NDS F2 Waist Limit Backtest]]
- [[NDS F2 Fast Exact Backtest Runtime]]

This profile is independent of HH/F3H setup selection. Hook can remain internal detector boundary evidence, but no Hook field authorizes the order.
