# M0001 Live Past-Only Bridge Compile Fix

## Problem

The previous live past-only bridge snapshot accidentally inserted the `StatusValue`
helper as escaped text (`\n`) on one physical MQL line. MetaEditor then parsed the
whole block as invalid global tokens.

Typical compile errors:

```text
'n' - semicolon expected
StatusFileName - undeclared identifier
OpenTextRead - undeclared identifier
FileClose - ambiguous call
```

## Fix

`StatusValue()` is now emitted as normal MQL source code.  
The missing input `InpBridgeTimerConfigPulse` is also declared.

Version: `6.51`.
