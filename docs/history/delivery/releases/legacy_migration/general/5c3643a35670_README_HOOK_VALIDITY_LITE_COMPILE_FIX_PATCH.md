# Hook Validity Lite Compile Fix Patch

This patch fixes the following MetaEditor compile error:

```text
undeclared identifier 'cfg' FP_HookPhase02Visual.mqh 600 73
cannot convert parameter 'const unknown' to 'const FP_HookPhase02Config&'
```

## Changed file

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
```

## What changed

`FP_HookP02GetOriginGroupEnvelope(...)` now receives the Phase 02 visual config explicitly:

```mql5
bool FP_HookP02GetOriginGroupEnvelope(const FP_HookPhase02Config &cfg,
                                      const FP_HookPhase02Sequence &seed,
                                      ...)
```

The call site inside `FP_HookP02DrawOriginGroupEnvelopes(...)` now passes `cfg`.

## Scope

Compile fix only. No strategy logic changed.
