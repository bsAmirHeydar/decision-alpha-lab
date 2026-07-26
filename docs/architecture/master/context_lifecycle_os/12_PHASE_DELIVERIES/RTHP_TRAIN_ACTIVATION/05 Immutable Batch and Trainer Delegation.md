# Immutable Batch and Trainer Delegation

The activation freezes source hashes, ledger hashes, feature and label matrices, tasks, split policy, resource policy, and Context identity into an immutable batch manifest. Model fitting, guarded data access, OOF prediction, selection lock, final-test access, metrics, serialization parity, model artifacts, and model cards are delegated to existing Strategy Factory engines.
