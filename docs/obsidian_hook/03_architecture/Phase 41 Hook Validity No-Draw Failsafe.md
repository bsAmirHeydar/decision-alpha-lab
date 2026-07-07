# Phase 41 Hook Validity No-Draw Failsafe

The renderer now uses a two-pass selection in valid-only mode:

1. Select practical valid Hook families.
2. If no valid Hook is selected and fallback is enabled, select structural Hook candidates.

The fallback is visual-only and does not change validity labels.
