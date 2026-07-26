# Valid Hook Too Few Debug Checklist

If too few valid Hooks appear:

1. Set `InpHookPhase02ValidOnlyRequireNearDeath = false`.
2. Set `InpHookPhase02ValidF3RequireSameScale = false`.
3. Keep `InpHookPhase02ShowOnlyValidHooks = true`.
4. Enable CSV export and check:
   - `valid_after_hook`
   - `valid_after_opposing_f3`
   - `valid_hook_family`
   - `hook_validity_family`
5. If all valid families are zero, turn `InpHookPhase02ShowOnlyValidHooks = false` and verify that structural Hook candidates are being built.
6. If structural candidates exist but F3 validity is zero, inspect whether the immediate next Hook after F3 is same direction instead of opposite.
7. If Hook-after-Hook is zero, inspect whether `previous structural terminal node == next origin node` actually occurs.
