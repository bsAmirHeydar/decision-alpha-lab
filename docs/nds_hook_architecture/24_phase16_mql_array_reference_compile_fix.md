# Phase 16 Compile Fix — MQL5 Array Reference Parameters

## Issue

MetaEditor reported:

```text
'scales' - arrays are passed by reference only
'directions' - arrays are passed by reference only
```

The failing helper was:

```mql5
bool FP_HookP02AlreadySelectedScaleDirection(const int scales[],
                                             const int directions[],
                                             ...)
```

## Fix

MQL5 array parameters must use reference syntax. The helper now uses:

```mql5
bool FP_HookP02AlreadySelectedScaleDirection(const int &scales[],
                                             const int &directions[],
                                             ...)
```

No Hook logic changed. This is a compile-only fix for the Phase 16 sequence draw-mode selector.
