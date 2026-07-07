# HOOK-VALIDITY-LITE — Practical Valid Hook Determination

This patch replaces the overly restrictive valid-Hook display doctrine with a practical two-layer model:

1. **Hook counting stays complete.** The engine should count structural Hook sequences without turning the detector into a narrow production filter.
2. **Validity is a production-view filter.** A Hook becomes production-valid only when it belongs to one of the accepted families, but visibility should not require extra semantic gates unless explicitly enabled.

Open first:

- `docs/nds_hook_architecture/52_phase39_practical_valid_hook_determination.md`
- `docs/obsidian_hook/00_mocs/HOOK_VALIDITY_CORE_MOC.md`

Core input set for practical valid-only view:

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
InpHookPhase02SeedUsedNodesCannotRestart = true
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

Use stricter mode only when auditing:

```text
InpHookPhase02ValidOnlyRequireNearDeath = true
InpHookPhase02ValidF3RequireSameScale = true
```
