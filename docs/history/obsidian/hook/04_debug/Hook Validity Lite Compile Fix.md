# Hook Validity Lite Compile Fix

## Error

```text
undeclared identifier 'cfg'
FP_HookPhase02Visual.mqh
```

## Cause

`FP_HookP02GetOriginGroupEnvelope()` used `cfg` internally without receiving it as a parameter.

## Fix

The function now accepts `const FP_HookPhase02Config &cfg`, and the draw-envelope caller passes the current config.

## Scope

Compile fix only.
