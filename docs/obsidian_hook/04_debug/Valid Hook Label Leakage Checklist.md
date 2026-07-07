# Valid Hook Label Leakage Checklist

Use this when `InpHookPhase02ShowOnlyValidHooks = true` but extra labels still appear.

Check:

- raw/core Hook renderer is disabled in valid-only mode
- Phase 01 raw labels are disabled in valid-only mode
- Phase 03-06 diagnostic overlays are disabled in valid-only mode
- Phase 02 selected indexes include only valid Hook groups and required parent companions
- stale objects from old prefixes are deleted after timeframe change or reattach

Expected:

- labels visible only inside immediate Hook-after-opposing-F3 groups
- labels visible only inside Hook-after-Hook child groups
- parent Hook labels visible only when required by Hook-after-Hook
