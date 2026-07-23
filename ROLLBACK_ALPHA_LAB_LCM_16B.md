# Roll back Alpha Lab LCM-16B

Rollback is phase-bounded.

1. Revert the LCM-16B commit as one isolated Git operation.
2. Confirm that all paths listed as `ADDED` in `LCM_16B_PATCH_MANIFEST.json` are removed.
3. Confirm that the three modified roadmap documents return to their parent-commit bytes.
4. Run LCM-16A package verification and Engineering Policy.
5. Confirm that no legacy source, canonical target, redirect, quarantine evidence, Git LFS object or runtime state changed.

Do not use wildcard deletion. Do not delete `registry/legacy_context_migration` broadly. LCM-16B rollback must not undo LCM-15C or LCM-16A evidence.
