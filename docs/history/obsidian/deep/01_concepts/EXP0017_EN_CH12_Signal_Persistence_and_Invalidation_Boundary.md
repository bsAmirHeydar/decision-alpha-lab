# EXP0017 EN CH12 — Signal Persistence and Invalidation Boundary

## Thesis

A signal persists unless the divergence itself is invalidated by double hunt; no external filter suppresses it in the base layer.

## Doctrine

- Signals are not removed because another CG exists.
- Signals are not removed because time feels weak.
- Signals are not removed because stop distance is large.
- True invalidation is removal of asymmetry by both-symbol hunt.
- Raw signal validity and trading quality are different concepts.

## Fields

- `signal_status`
- `invalidation_time`
- `double_hunt_after_confirmation`
- `still_tradeable_flag`

## Implementation Note

- Build signal lifecycle states.
- Do not suppress confirmed signals before statistics.
