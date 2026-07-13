feat(exp0019): implement FP-I08 weekly WW context engine

- compile previous-week versus current-week WW relations from FP-I05 windows and references
- reuse FP-I06 M1 first-sweep and candidate semantics without a parallel detector
- reuse FP-I07 closed-host-candle confirmation and preserve immutable confirmed evidence
- implement protected-symbol second-touch neutralization and check-week expiry
- resolve newest active confirmed WW while retaining shadowed historical contexts
- publish deterministic downstream directional gates with fail-closed data handling
- retain suppressed signals and keep WW directly tradeable without self-suppression
- add closed schemas, checkpoints, revision impact, MQL5 mirrors, tests, QA evidence, and Obsidian documentation
