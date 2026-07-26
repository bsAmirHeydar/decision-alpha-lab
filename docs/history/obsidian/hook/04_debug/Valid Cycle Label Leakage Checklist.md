# Valid Cycle Label Leakage Checklist

Use this checklist when non-valid Hook labels appear in valid-only mode.

## Required inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
```

## Expected rendering

Only these should be visible:

- immediate Hook after opposing F3;
- Hook-2 after Hook-1;
- Hook-1 only as parent companion of Hook-2;
- node/sequence labels belonging to those selected origin groups.

## If invalid labels still appear

Check:

1. stale chart objects from old prefixes;
2. Phase 01 node drawing not disabled by valid-only guard;
3. Phase 03-06 diagnostic overlays;
4. fallback accidentally enabled;
5. `valid_hook_family` incorrectly set on structural candidates.
