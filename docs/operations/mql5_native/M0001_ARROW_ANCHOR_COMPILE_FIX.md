# M0001 Arrow Anchor Compile Fix

## Problem

MetaEditor can reject `ENUM_ARROW_ANCHOR` defaults when the constant name overlaps
with text/object anchor constants.

Error:

```text
improper enumerator cannot be used
DAL_ChartObjects.mqh
```

## Fix

The arrow helper now accepts the arrow anchor as `int` and passes it directly to
`OBJPROP_ANCHOR`.

This avoids enum-name ambiguity while keeping the same behavior:

```text
HIGH node -> ANCHOR_BOTTOM
LOW node  -> ANCHOR_TOP
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.14`.
