# Restart checkpoint contract

The Common Files checkpoint stores:

- every reference lifecycle record;
- accepted and optionally rejected use records;
- every processed P06 result ID.

This prevents duplicate use creation after reattachment and preserves terminal retirement. Missing checkpoint plus missing historical replay is not sufficient to reconstruct exact past breach order; production recovery must fail closed or use P11 replay.
