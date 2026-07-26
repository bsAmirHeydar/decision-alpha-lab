# Competing Risk: Target, Stop, and Time Exit

A single opportunity may terminate by target, stop, time exit, invalidation, manual close, or market/session termination. These causes compete. Modeling each as an independent binary label can produce probabilities whose sum exceeds one.

The competing-risk contract therefore emits overall survival and cause-specific cumulative incidence on the same horizon grid. The native implementation uses empirical cause-specific interval hazards. Optional cause-specific Cox and subdistribution adapters are future-compatible.

Cause IDs are stable schema values. Unknown causes are rejected rather than silently merged. Cause probabilities must be monotone, bounded, and coherent with overall survival. Target-first and stop-first probabilities can feed treatment utility, but they never replace side-aware monetary outcome simulation.
