# Phase 55 NDS Hook 86.4 Cycle R1 Execution

## Decision

Add `HOOK_864_CYCLE_R1` as an opt-in profile inside the existing `FP_NDSHookTrade*` stack.

```text
Canonical Hook Phase02 identity/family/Terminal/x_count
→ canonical Phase03 Y reference
→ canonical Phase04 50% X closure and alive state
→ no closed-bar 86.4 arrival at or after closure
→ limit at 0.864 Crown→Origin
→ Stop behind Death/Origin
→ attached 1R Target
```

## No parallel canon

The profile may not call market-history APIs, detect pivots, count nodes, reconstruct Hook family, or mutate canonical sequence state. It consumes one `FP_HookPhase02Sequence`, the exact matching `FP_HookPhase04Record`, and the caller-owned canonical closed-rate array. It does not privately call `CopyRates`.

## Compatibility

`TERMINAL_F123` remains default and unchanged. The shared core dispatches position exit by profile. Compatibility wrappers preserve prior public function names.

## Links

- [[../../nds_entry_architecture/phase55_hook_864_cycle_r1_execution/README|Detailed package]]
- [[../08_entry_execution/NDS Hook 86.4 Cycle R1 Entry Contract]]
- [[../08_entry_execution/NDS Hook 86.4 Cycle R1 State Machine]]
- [[../08_entry_execution/NDS Hook 86.4 Cycle R1 Audit Ledger]]
- [[../08_entry_execution/NDS Hook 86.4 Cycle R1 Operator Checklist]]
- [[../08_entry_execution/NDS Hook 86.4 No Trade Diagnostic Funnel]]
- [[../00_mocs/NDS_ENTRY_EXECUTION_MOC]]
