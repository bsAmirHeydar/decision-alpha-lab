# M0001 Clean Revisit Labels

## Decision

`InpShowRevisitLabels` now draws only true revisit labels.

It no longer prints full event diagnostics such as:

```text
REV#1 TOUCH_OK len=...
TOUCH_EVENT TOUCH_OK CONSUMED:TOUCH
```

Instead, the revisit layer prints only the revisit identity:

```text
REVISIT#1
REVISIT#2
REVISIT#3
```

## True revisit

In HUNT mode:

```text
REV#0 = first visit
REV#1+ = actual revisit
```

Only `REV#1+` is drawn by the revisit-label layer.

## TOUCH mode

TOUCH mode is one-shot:

```text
first confirmed touch -> CONSUMED:TOUCH
```

So `InpShowRevisitLabels` does not draw TOUCH mode event text.

## Color

Actual revisit labels are drawn with a distinct revisit color:

```text
clrDeepSkyBlue
```

This makes actual revisits visually separate from normal touch, pending, consumed
and hunt labels.

## Recommended debug setup

To see only revisit text:

```text
InpShowRevisitLabels = true
InpShowNodeStateLabels = false
InpShowEvents = false
InpShowRtvLabels = false
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.43`.
