# Run Evidence and Verification

Each run is written through a staging directory and atomically promoted after successful training. It contains source snapshots, four ledgers, a resolved binding, feature and label matrices, an immutable batch manifest, task trial ledgers, access audits, model evidence, reports, a complete SHA-256 ledger, and a completion marker. The `verify-run` command independently checks all recorded hashes.
