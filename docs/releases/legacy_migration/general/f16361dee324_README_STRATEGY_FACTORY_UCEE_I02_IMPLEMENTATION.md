# UCEE-I02 — Context Package SDK, Lifecycle, and Reference Contexts

This patch implements the second delivery phase of the Universal Context Exploitation Engine implementation program.

## Delivered

- exact-version context package manifests and static registries;
- source requirements and runtime availability declarations;
- causal context observations and lifecycle transitions;
- duplicate suppression, supersession, retirement, and bounded lifecycle state;
- feature descriptors, known-time, missingness, staleness, dependencies, and immutable frames;
- tabular, sequence, graph, intermarket, raster, sparse-event, path-signature, execution, portfolio, and fused representation views;
- dependence-aware cluster rules and assignments;
- manual setup/policy references and learning task declarations;
- synthetic causal reference context package;
- SF20 EXP0017 adapter-backed reference context package;
- linting, replay hashing, future perturbation, negative fixtures, and lifecycle chaos coverage;
- Python and MQL5 SDKs, schemas, examples, tests, diagnostics, and English Obsidian documentation.

## Authority Boundary

The phase has no broker order authority and does not implement entry, stop, exit, trailing, capital, training, or model selection. Those concerns remain downstream.

## Validation

Run `tools/strategy_factory/run_uce_i02_tests.ps1`, then run the MetaEditor compile harness on Windows.

## Next Phase

UCE-I03 — Treatment Atom Registries.
