# Profile 04 — Auto Trade Entry Only Rehearsal

## Intent

Controlled real-entry rehearsal without real partial or hard-close automation.

This is not the final production profile. It is a bridge between Paper Live and Full Managed Auto Trade.

## Required mode

- Runtime mode: Auto Trade.

## Required real transport

Enable:

- Broker position manager.
- Real auto-entry.

Disable:

- Real partial close.
- Real hard close finalizer.

## Risk recommendation

Use the smallest practical risk while validating live order behavior.

## What to verify

The operator should verify:

1. Real entries occur only on confirmed STC signals.
2. Real entry does not occur after the grace window.
3. Orders are sent only on Symbol1/Symbol2.
4. Orders carry the configured magic number.
5. SL and TP match the paper plan.
6. Split orders are capped and audited.
7. Max three entries per M is respected.
8. Hedging OFF direction lock is respected inside each M only.

## Warning

Because real partial and real hard close are disabled in this profile, manual supervision is required.

