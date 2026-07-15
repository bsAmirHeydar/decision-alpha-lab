feat(strategy-factory): implement SAED V4-08 executable path outcome cube

Implement the governed deterministic bridge from the V4-07 action lattice to the V4-09 execution digital twin.

- freeze known-time context, market-path, outcome-policy and cost-registry contracts
- compile every action node into a bounded executable path specification
- simulate entry, stop, target, partial, trail, time, gap and ambiguity semantics
- preserve Skip and Abstain as explicit non-order counterfactual outcomes
- add side-aware spread, slippage, commission and net-R economics
- add immutable path-event ledgers, MFE/MAE, complete exposure and row Merkle integrity
- add deterministic replay, semantic diff, partitioning, telemetry and quarantine
- add CLI, closed schemas, golden/negative fixtures, conformance vectors and tests
- add diagnostic-only MQL5 mirrors and detailed Obsidian implementation notes
- emit a bounded reference-only V4-09 handoff

Evidence remains reference-only. MetaEditor compilation, broker calibration, external reproduction, prospective performance, real alpha, runtime activation and production authorization remain pending.
