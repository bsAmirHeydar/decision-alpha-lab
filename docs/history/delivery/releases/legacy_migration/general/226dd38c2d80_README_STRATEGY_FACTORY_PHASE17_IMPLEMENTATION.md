# Strategy Factory Phase 17

Phase 17 implements a deterministic, MQL5-first paper and shadow execution layer. It consumes
Phase 16 execution intents, manages market/limit/stop order lifecycles, bounded partial fills,
position aggregation and stop/target exits, explicit friction, append-only hash-chained transaction
history, reconciliation, and shadow fill comparison. It deliberately contains no broker-send API.

Run `tools/strategy_factory/run_phase17_tests.ps1`, then compile the three Phase 17 Expert Advisors
locally with MetaEditor. Phase 18 may consume these contracts only after paper/shadow soak evidence
and reconciliation quality are accepted.
