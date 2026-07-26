# Determinism, Resource, and Serialization Policy

Native algorithms are deterministic under fixed inputs, ordering, and configuration. Pair construction, action ordering, horizon ordering, quantile ordering, and regime ordering use stable identifiers. Resource limits bound pair counts, rows, outputs, horizons, actions, and wall time.

Every model state is canonical JSON with a state hash. Opaque pickle artifacts remain forbidden. Optional third-party artifacts require explicit environment fingerprints and exportability disclosures.

Repeated-run tests compare state and prediction hashes. Numeric-tolerance algorithms must declare tolerance and platform. Nondeterministic algorithms are retained as research trials but cannot pass the deterministic runtime gate without a documented exception.
