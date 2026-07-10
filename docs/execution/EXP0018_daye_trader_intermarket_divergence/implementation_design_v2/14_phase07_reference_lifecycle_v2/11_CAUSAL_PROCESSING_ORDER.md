# Causal processing order

For each refresh:

1. P06 refreshes and finalizes host-close outcomes.
2. New P06 results are processed in stored chronological order.
3. Current P05 observations are applied to surviving references.
4. Retirement is evaluated only from evidence newer than the record’s last applied observation availability.
5. Checkpoint and audit are written after state mutation.

A result after an already-known retirement is rejected. Post-retirement evidence cannot reactivate the reference.
