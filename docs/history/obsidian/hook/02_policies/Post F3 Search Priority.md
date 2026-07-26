# Post F3 Search Priority

The system must not randomly select a post-F3 Hook.

Recommended production priority:

1. Direct structural Hook from F3 terminal side.
2. Direct 80% geometric Hook, if geometric mode is enabled.
3. Delayed/rebound structural Hook inside F3 ownership window.
4. Delayed/rebound 80% geometric Hook, if geometric mode is enabled.

Within equal family rank, the implementation should choose by:

1. structural completeness;
2. directness to F3 terminal side;
3. earliest qualification;
4. stronger completion percent.

The priority must be explicit and documented in export/debug output.
