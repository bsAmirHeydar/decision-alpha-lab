# Determinism and reproducibility

Wall-clock time and temporary workspace paths do not participate in artifact identity. Snapshot ordering is repository-relative POSIX ascending. Output manifests exclude themselves to avoid recursive hashing.

Re-running the builder against identical repository bytes produces the same machine package bytes and decision state.
