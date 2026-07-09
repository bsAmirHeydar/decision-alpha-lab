# 01 — Alert Contract

The alert engine consumes `GT_NewsStore`, `GT_FilterState`, `GT_Config`, and `GT_AlertState`.

It must not mutate events. It can only mutate:

- `GT_AlertState`
- alert diagnostic fields in `GT_RuntimeState`

## Input authority

`event.time_broker` remains the only timing authority. UTC/source fields are diagnostic only.

## Eligibility chain

```text
config enabled
filters alerts enabled
event in date window
config-level event inclusion
optional runtime filter inclusion
time-stage predicate
key not already sent
cooldown passed
delivery channel active
```
