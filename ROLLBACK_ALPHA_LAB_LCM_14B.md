# Rollback Alpha Lab LCM-14B

Reverse only paths listed in `LCM_14B_FILE_INDEX.txt` and restore the exact LCM-14A handoff state. Remove the generated quarantine evidence package, LCM-14B implementation, schemas, policies, tests and phase-owned documentation. Restore the single bounded locator wording change in `tools/flag_counting/offline_license_keygen.py`.

No legacy redirect, canonical document or active source is removed by LCM-14B. Rollback therefore does not require deletion recovery or runtime-state restoration.
