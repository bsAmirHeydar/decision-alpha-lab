# Post F3 Hook Recognition Window

A valid Hook after F3 must belong to the F3 that created its terminal environment.

The F3 does not validate every later Hook forever.

## Window start

The recognition window starts when the F3 reaches or confirms its terminal side.

## Window end

The window must end at the first meaningful supersession event:

- a new F3 terminal context;
- a major opposing structure;
- configured max bar/time limit;
- explicit invalidation boundary;
- chart/range boundary.

## Why this exists

Without this window, the system can attach `F3H` to a later unrelated Hook.

With a window that is too strict, it misses delayed/rebound Hooks that the user wants to study.
