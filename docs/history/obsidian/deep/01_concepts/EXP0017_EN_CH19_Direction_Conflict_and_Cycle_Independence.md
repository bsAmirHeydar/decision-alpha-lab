# EXP0017 EN CH19 — Direction Conflict and Cycle Independence

## Thesis

Buy and sell divergences, same-direction clusters, opposite-direction clusters, CGs, and internal cycles remain independent before statistics.

## Doctrine

- High-hunt asymmetry produces sell divergence.
- Low-hunt asymmetry produces buy divergence.
- Late entry and large stop are not base filters.
- Post-confirmation invalidation is recorded as later invalidation, not proof the original signal was never valid.
- Signal count does not change validity.

## Fields

- `direction_cluster`
- `late_entry_flag`
- `large_stop_flag`
- `post_confirmation_invalidation`
- `signal_density`

## Implementation Note

- Record conflict clusters instead of resolving them manually.
- Do not force non-divergence behavior into the divergence dataset.
