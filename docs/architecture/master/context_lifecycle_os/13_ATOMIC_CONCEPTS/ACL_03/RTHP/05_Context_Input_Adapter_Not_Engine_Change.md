# Context Input Adapter, Not Engine Change

A new Context enters the AI engine by implementing the existing `ContextPackage` interface and registering context-owned descriptors and contracts. Adding a Context must not require mutation of shared dataset, trainer, validation, orchestration, promotion, or runtime kernels.

For RTHP, the adapter maps already-confirmed canonical occurrences to engine observations and features. It does not perform divergence detection or reinterpret the Context.
