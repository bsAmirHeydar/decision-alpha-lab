# Run Artifacts

A successful run directory contains:

- `source_snapshot.json`
- `activation_config.normalized.json`
- four materialized ledgers under `ledgers/`
- resolved `data_binding.real.v1.json`
- feature and label matrices under `datasets/`
- `batch/immutable_batch_manifest.json`
- task-level trial ledgers, access audits, model manifests, and model cards
- materialization, feature, label, and train reports
- `run_manifest.json`
- `RUN_FILE_HASHES.sha256`
- `RUN_COMPLETE`

The output directory is created through a staging directory and atomically promoted only after a complete run. An existing output directory is never overwritten.
