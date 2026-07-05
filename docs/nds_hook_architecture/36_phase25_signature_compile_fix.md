# Phase 25 Compile Fix — Duplicate Function Signature

## Issue

MetaEditor reported parse errors around `FP_HookP02GetOriginGroupExtreme` because a text merge in Phase 25 produced a duplicated function name:

```mql5
bool FP_HookP02GetOriginGroupExtremebool FP_HookP02GetOriginGroupExtreme(...)
```

That malformed declaration caused the later `end_time` and `end_price` parameters to be interpreted at global scope, which then cascaded into additional warnings about variable hiding.

## Fix

The malformed declaration was corrected to:

```mql5
bool FP_HookP02GetOriginGroupExtreme(...)
```

No Hook logic, rendering policy, or trading behavior changed.
