# Strict Valid Hook View Debug Checklist

Use this when `InpHookPhase02ShowOnlyValidHooks = true` still appears to show too many objects.

1. Confirm the input is true.
2. Confirm `InpDrawHooks` does not matter in valid-only mode; raw hooks are force-suppressed.
3. Confirm Phase 03-06 overlays are not drawing.
4. Turn on `InpHookPhase02PrintSummary = true` and check:
   - `valid_after_hook`
   - `valid_after_opposing_f3`
   - `valid_hook_family`
   - `invalid_family_filtered`
5. If old objects remain, reattach the expert once. The runtime cleanup should remove the old prefixes on the next run.
