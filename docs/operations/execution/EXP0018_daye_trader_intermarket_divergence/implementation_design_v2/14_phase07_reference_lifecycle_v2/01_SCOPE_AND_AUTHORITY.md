# Scope and authority

P07 is the first module with **reference-lifecycle authority**. It may activate, preserve, and retire a reference side. It may accept or reject a confirmed use. It may not reinterpret P06 close truth, draw chart objects, infer BUY/SELL, select entries, size risk, or place orders.

### In scope
- exact-opportunity first-use deduplication;
- repeated use across later distinct opportunities while the same protected symbol survives;
- protected-symbol touch retirement;
- double-hunt retirement;
- role-switch retirement;
- immutable historical accepted uses;
- checkpoint, audit, replay-safe identities.

### Out of scope
- object creation;
- target or stop logic;
- statistical ranking;
- optional SSMT variants;
- trade execution.
