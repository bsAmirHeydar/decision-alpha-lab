# Optional Dependency and Environment Governance

Dependency probing records module, distribution, installed version, state, reason, and evidence hash. Optional packages are explicit extras, not hidden imports. Four terminal states are recognized: available, unavailable, incompatible, and disabled.

An unavailable optional trainer produces a typed skip or retained failure according to benchmark policy. It must not crash catalog discovery, mutate the algorithm set, or fall back silently. Environment hashes and package versions belong in artifact evidence.

The baseline pack remains operational without external boosters. Dependency drift is a reproducibility event and requires a new environment and benchmark record.
