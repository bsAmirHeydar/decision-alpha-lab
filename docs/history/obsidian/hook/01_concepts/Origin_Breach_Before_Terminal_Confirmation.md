---
type: concept
domain: hook_lifecycle
status: canonical
aliases:
  - Raw Origin Breach Guard
  - Origin Death Before Resolve Confirmation
---

# Origin Breach Before Terminal Confirmation

A Hook candidate is invalid if its origin boundary is touched or penetrated
before the terminal node has stabilized.

```text
origin breach before terminal confirmation = non-hook candidate
```

This is stricter than saying the Hook failed. A failed Hook first has to exist.
A pre-confirmation origin breach means the structure never earned Hook status.

## Positive Hook

```text
origin = Hook floor
breach = raw candle low <= origin price
```

## Negative Hook

```text
origin = Hook ceiling
breach = raw candle high >= origin price
```

## System consequence

```text
No semantic arc
No primary Hook zone
No zone-quality sample
No valid Hook label
```

## Why this exists

Hook counting is fractal. Without a strict lifecycle guard, the engine can draw
many hook-like semicircles whose origin has already died. This pollutes both the
visual layer and the future learning dataset.
