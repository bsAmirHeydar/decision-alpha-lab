# Object Ownership and Idempotency

All owned names start with `EXP0018_P08_`. Names use a deterministic hash of immutable `use_id`, so repeated callbacks and reattachment address the same object.

On refresh:
- absent owned line → create;
- exact line → verify;
- moved or corrupted owned line → repair from immutable evidence;
- foreign line → ignore;
- duplicate exact use → no second object.

The object list is a projection cache, not a state database.
