# HOOK VALID CYCLES ONLY VIEW — Start Here

This patch locks the production Hook display to valid Hook cycles only.

When `InpHookPhase02ShowOnlyValidHooks = true`, the chart must show only:

1. valid Hook cycles,
2. the sequence labels that belong to those valid cycles,
3. the node labels that belong to those valid cycles,
4. the parent companion Hook only when it is required by a valid Hook-after-Hook chain.

Unqualified structural Hook candidates must not leak into the production chart through fallback rendering, old object prefixes, Phase 01 raw-node display, or later diagnostic overlays.

Default change:

```text
InpHookPhase02ValidOnlyFallbackToStructural = false
```

This means strict valid-only mode is no longer allowed to fall back to all structural hooks by default. If no valid Hook exists in the current visible/history window, the correct production output is no Hook cycle, not a noisy structural fallback.
