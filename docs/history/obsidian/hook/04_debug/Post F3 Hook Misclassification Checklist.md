# Post F3 Hook Misclassification Checklist

Use this when F3 is correct but `F3H` is visually wrong.

## Check F3 ownership

- Is the F3 terminal side correct?
- Is the displayed Hook inside the post-F3 search window?
- Did a newer F3/context supersede this F3 before the displayed Hook?

## Check direct vs delayed

- Did a Hook start directly from the F3 terminal side?
- Did price first reach the F3 side, rebound, and then make a delayed Hook?
- Is the displayed Hook actually a delayed candidate?

## Check structural vs geometric

- Does the candidate have full sequence nodes?
- Does it have a confirmed terminal node?
- If not, is geometric 80% mode enabled?
- Did the cycle reach the 80% threshold?

## Check leakage

- Are raw sequence labels visible without F3H/F3H80 family prefix?
- Are same-origin siblings being shown?
- Is structural fallback enabled by mistake?

## Expected labels

Suggested post-F3 labels:

```text
F3H-DIR
F3H-REB
F3H80-DIR
F3H80-REB
```
