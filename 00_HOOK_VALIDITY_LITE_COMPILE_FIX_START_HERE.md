# HOOK VALIDITY LITE COMPILE FIX

This patch fixes a compile error introduced by the practical valid-Hook view update.

## Fixed error

`FP_HookPhase02Visual.mqh` referenced `cfg` inside `FP_HookP02GetOriginGroupEnvelope(...)`, but the function did not receive `cfg` as a parameter.

## Fix

The function signature now accepts:

```mql5
const FP_HookPhase02Config &cfg
```

and the only call site passes the existing visual config into the function.

## Scope

Compile/API fix only.

No Hook counting doctrine, valid-Hook determination, F-counting logic, Rally logic, execution behavior, risk sizing, broker behavior, or order sending is changed.
