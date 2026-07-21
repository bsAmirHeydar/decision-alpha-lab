# Rollback Alpha Lab LCM-12B

Use the authoritative rollback manifest at:

`registry/legacy_context_migration/documentation_reconciliations/DOCRECON_F60803B1B8316F47D966D02CB905ACC8/rollback_manifest.json`

Rollback must remove only LCM-12B-created canonical targets and generated registries, restore redirect-stubbed legacy documents from Git history, preserve all pre-existing documentation, and re-run the direct LCM-12B acceptance test. Do not use broad deletion or reset commands.
