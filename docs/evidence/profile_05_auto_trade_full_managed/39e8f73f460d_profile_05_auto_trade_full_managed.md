# Profile 05 — Auto Trade Full Managed

## Intent

Full automated lifecycle:

- real entry;
- real broker position scan;
- real partial close for M1/M2;
- real hard close finalizer after 15:30 New York.

## Required mode

- Runtime mode: Auto Trade.

## Required real transports

Enable:

- Broker position manager.
- Real auto-entry.
- Real partial close if partial behavior is desired.
- Real hard close finalizer.

## Required safety behavior

- Magic-only management must remain enabled.
- Foreign positions must remain audit-only.
- Duplicate instance lock must remain enabled.
- Validation must run on init.
- Persistence must remain enabled.

## What to verify during first deployment

1. New York time is correct.
2. M/W dashboard is correct.
3. Validation summary is acceptable.
4. Broker scan sees no unintended managed positions.
5. First signal creates exactly one real entry group.
6. SL/TP match paper plan.
7. Partial marker is written only after successful partial close.
8. Hard close finalizer retries only matching magic positions.
9. No position with nonmatching magic is closed.

## Acceptance criteria

This profile is production-ready only after it has behaved correctly on a safe account through at least one full STC trading day.

