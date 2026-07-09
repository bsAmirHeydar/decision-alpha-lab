# Valid Cycles Only Means No Structural Fallback

When `InpHookPhase02ShowOnlyValidHooks = true`, production rendering must show only valid Hook cycles and the sequence/node labels that belong to those cycles.

Structural fallback is not production-valid. It is a debug-only mode.

Default:

```text
InpHookPhase02ValidOnlyFallbackToStructural = false
```
