# Rollback Alpha Lab LCM-13C

Reverse only paths listed in `LCM_13C_FILE_INDEX.txt`. Restore the LCM-13B handoff state, compatibility records and phase-owned evidence. Git revert alone is not represented as sufficient for runtime state; live runtime state was not mutated by this reference-only phase.
