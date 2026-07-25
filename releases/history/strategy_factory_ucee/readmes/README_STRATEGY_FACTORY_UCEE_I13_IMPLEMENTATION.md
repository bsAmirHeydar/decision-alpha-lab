# UCE-I13 — Manual, AI, and Hybrid Policy Graph

UCE-I13 implements a bounded decision-policy layer after UCE-I12 statistical promotion. Personal setups remain exact executable manual policies. Signed promoted models may filter, rank, choose a declared treatment, choose a declared risk tier, or abstain. They cannot create a context occurrence, expand capability, override a hard veto, or gain trading authority.

## Delivered

- 20 Python modules in `strategy_factory_policy_v3`.
- 25 new closed public JSON schemas.
- 14 registered deterministic policy-node kinds.
- 12 MQL5 contract and diagnostic files.
- 37 detailed delivery chapters and 9 atomic Obsidian concepts.
- Golden manual-only and hybrid examples, conformance vectors, negative fixtures, replay, trace, and incremental-value evidence.

## Authority boundary

This package emits policy decisions and evidence only. It contains no broker, order, position, live-network, or external execution authority. Runtime compilation, ONNX export, Python/MQL5 parity, atomic activation, and rollback belong to UCE-I14.
