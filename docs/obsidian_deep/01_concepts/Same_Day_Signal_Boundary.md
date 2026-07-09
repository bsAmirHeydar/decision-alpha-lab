# Same-Day Signal Boundary

## Rule

Only current New York trading day signals are checked.

The day is:

```text
18:00 NY to 17:00 NY
```

## Allowed

- Reference previous completed cycle inside the same trading day.
- Confirm divergence inside the same trading day.
- Enter during the same trading day.
- Close at cycle end.

## Forbidden

- Use previous-day cycle levels for new entries.
- Carry unconfirmed divergence across day boundary.
- Search historical days for trade setup formation.

## Practical consequence

At a new 18:00 NY day, the EA resets its signal registry. It may still manage open positions if they exist, but signal formation starts fresh.

